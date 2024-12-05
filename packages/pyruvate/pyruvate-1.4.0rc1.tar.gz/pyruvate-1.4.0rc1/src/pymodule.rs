#![allow(clippy::manual_strip, clippy::unnecessary_wraps)] // suppress warnings in py_fn! macro
use cfg_if::cfg_if;
use cpython::{py_class, IOError, PyErr, PyObject, PyResult, Python, PythonObject, ValueError};
use mio::net::{TcpListener, UnixListener};
use pyo3_ffi::{self as ffi, METH_KEYWORDS};
use std::ffi::CStr;
use std::ffi::CString;
use std::ptr;
use std::time::Duration;

use crate::filewrapper::FileWrapper;
use crate::globals::{shared_wsgi_options, ServerOptions};
use crate::pyutils::{async_logger, sync_logger};
use crate::server::Server;
use crate::startresponse::StartResponse;
use crate::transport::{parse_server_info, shared_connection_options};

#[cfg(target_os = "linux")]
use crate::transport::SocketActivation;

macro_rules! server_loop {
    ($L:ty, $application: ident, $listener: ident, $server_options: ident, $async_logging: ident, $py: ident) => {
        match Server::<$L>::new($application, $listener, $server_options, $py) {
            Ok(mut server) => {
                let res = if $async_logging {
                    async_logger($py, "pyruvate")
                } else {
                    sync_logger($py, "pyruvate")
                };
                match res {
                    Ok(_) => match server.serve() {
                        Ok(_) => Ok($py.None()),
                        Err(_) => Err(PyErr::new::<IOError, _>(
                            $py,
                            "Error encountered during event loop",
                        )),
                    },
                    Err(_) => Err(PyErr::new::<IOError, _>($py, "Could not setup logging")),
                }
            }
            Err(e) => Err(PyErr::new::<IOError, _>(
                $py,
                format!("Could not create server: {e:?}"),
            )),
        }
    };
}

#[allow(clippy::too_many_arguments, clippy::not_unsafe_ptr_arg_deref)]
pub fn serve(
    py: Python,
    application: *mut ffi::PyObject,
    addr: Option<String>,
    num_workers: usize,
    max_number_headers: usize,
    async_logging: bool,
    chunked_transfer: bool,
    max_reuse_count: u8,
    keepalive_timeout: u8,
    qmon_warn_threshold: Option<usize>,
    send_timeout: u8,
) -> PyResult<PyObject> {
    let application = unsafe { PyObject::from_borrowed_ptr(py, application) };
    if num_workers < 1 {
        return Err(PyErr::new::<ValueError, _>(py, "Need at least 1 worker"));
    }
    // addr can be a TCP or Unix domain socket address
    // or None when using a systemd socket.
    let (sockaddr, server_name, server_port) = parse_server_info(addr.clone());
    let server_options = ServerOptions {
        num_workers,
        max_number_headers,
        connection_options: shared_connection_options(
            max_reuse_count,
            Duration::from_secs(keepalive_timeout.into()),
        ),
        wsgi_options: shared_wsgi_options(
            server_name.clone(),
            server_port,
            String::new(),
            chunked_transfer,
            qmon_warn_threshold,
            Duration::from_secs(send_timeout.into()),
            py,
        ),
    };
    match addr {
        Some(_) => {
            match sockaddr {
                Some(sockaddr) => match TcpListener::bind(sockaddr) {
                    Ok(listener) => server_loop!(
                        TcpListener,
                        application,
                        listener,
                        server_options,
                        async_logging,
                        py
                    ),
                    Err(e) => Err(PyErr::new::<IOError, _>(
                        py,
                        format!("Could not bind socket: {e:?}"),
                    )),
                },
                None => {
                    // fallback to UnixListener
                    match UnixListener::bind(server_name) {
                        Ok(listener) => server_loop!(
                            UnixListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(e) => Err(PyErr::new::<IOError, _>(
                            py,
                            format!("Could not bind unix domain socket: {e:?}"),
                        )),
                    }
                }
            }
        }
        None => {
            cfg_if! {
                if #[cfg(target_os = "linux")] {
                    // try systemd socket activation
                    match TcpListener::from_active_socket() {
                        Ok(listener) => server_loop!(
                            TcpListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(_) => {
                            // fall back to UnixListener
                            match UnixListener::from_active_socket() {
                                Ok(listener) => server_loop!(
                                    UnixListener,
                                    application,
                                    listener,
                                    server_options,
                                    async_logging,
                                    py
                                ),
                                Err(e) => Err(PyErr::new::<IOError, _>(
                                    py,
                                    format!("Socket activation: {e}"),
                                )),
                            }
                        }
                    }
                } else {
                    Err(PyErr::new::<IOError, _>(
                        py,
                        "Could not bind socket.",
                    ))
                }
            }
        }
    }
}

// begin plain pyo3-ffi
static mut MODULE_DEF: ffi::PyModuleDef = ffi::PyModuleDef {
    m_base: ffi::PyModuleDef_HEAD_INIT,
    m_name: ffi::c_str!("pyruvate").as_ptr(),
    m_doc: ffi::c_str!("Pyruvate WSGI server").as_ptr(),
    m_size: 0,
    #[allow(static_mut_refs)]
    m_methods: unsafe { METHODS.as_mut_ptr().cast() },
    m_slots: std::ptr::null_mut(),
    m_traverse: None,
    m_clear: None,
    m_free: None,
};

static mut METHODS: [ffi::PyMethodDef; 2] = [
    ffi::PyMethodDef {
        ml_name: ffi::c_str!("serve").as_ptr(),
        ml_meth: ffi::PyMethodDefPointer {
            _PyCFunctionFastWithKeywords: wrap,
        },
        ml_flags: ffi::METH_FASTCALL | METH_KEYWORDS,
        ml_doc: ffi::c_str!("Serve WSGI application").as_ptr(),
    },
    // A zeroed PyMethodDef to mark the end of the array.
    ffi::PyMethodDef::zeroed(),
];

// The module initialization function, which must be named `PyInit_<your_module>`.
#[allow(non_snake_case)]
#[no_mangle]
pub unsafe extern "C" fn PyInit_pyruvate() -> *mut ffi::PyObject {
    let py = Python::assume_gil_acquired();
    let pymod = ffi::PyModule_Create(ptr::addr_of_mut!(MODULE_DEF));
    let ty =
        <StartResponse as py_class::PythonObjectFromPyClassMacro>::initialize(py, Some("pyruvate"))
            .unwrap();
    let di = ffi::PyModule_GetDict(pymod);
    ffi::PyDict_SetItemString(
        di,
        ffi::c_str!("StartResponse").as_ptr(),
        ty.as_object().as_ptr(),
    );
    let ty =
        <FileWrapper as py_class::PythonObjectFromPyClassMacro>::initialize(py, Some("pyruvate"))
            .unwrap();
    ffi::PyDict_SetItemString(
        di,
        ffi::c_str!("FileWrapper").as_ptr(),
        ty.as_object().as_ptr(),
    );
    pymod
}

unsafe extern "C" fn wrap(
    slf: *mut ffi::PyObject,
    args: *const *mut ffi::PyObject,
    nargs: ffi::Py_ssize_t,
    kwnames: *mut ffi::PyObject,
) -> *mut ffi::PyObject {
    const APPLICATION: &str = "application";
    const ADDR: &str = "addr";
    const NUM_WORKERS: &str = "num_workers";
    const MAX_NUMBER_HEADERS: &str = "max_number_headers";
    const ASYNC_LOGGING: &str = "async_logging";
    const CHUNKED_TRANSFER: &str = "chunked_transfer";
    const MAX_REUSE_COUNT: &str = "max_reuse_count";
    const KEEPALIVE_TIMEOUT: &str = "keepalive_timeout";
    const QMON_WARN_THRESHOLD: &str = "qmon_warn_threshold";
    const SEND_TIMEOUT: &str = "send_timeout";
    const PARAMS: &[&str] = &[
        APPLICATION,
        ADDR,
        NUM_WORKERS,
        MAX_NUMBER_HEADERS,
        ASYNC_LOGGING,
        CHUNKED_TRANSFER,
        MAX_REUSE_COUNT,
        KEEPALIVE_TIMEOUT,
        QMON_WARN_THRESHOLD,
        SEND_TIMEOUT,
    ];

    // Defaults
    let mut application: *mut ffi::PyObject = std::ptr::null_mut();
    let mut addr: Option<String> = None;
    let mut num_workers: usize = 2;
    let mut max_number_headers: usize = 32;
    let mut async_logging = true;
    let mut chunked_transfer = false;
    let mut max_reuse_count: u8 = 0;
    let mut keepalive_timeout: u8 = 60;
    let mut qmon_warn_threshold: Option<usize> = None;
    let mut send_timeout: u8 = 60;

    if nargs > 10 {
        ffi::PyErr_SetString(
            ffi::PyExc_TypeError,
            ffi::c_str!("serve() expects at most 10 positional argument").as_ptr(),
        );
        return std::ptr::null_mut();
    }

    // Positional parameters
    for (idx, prm) in PARAMS.iter().enumerate().take(nargs as usize) {
        let val = *args.add(idx);
        match *prm {
            APPLICATION => {
                application = val;
            }
            ADDR => {
                if ffi::PyUnicode_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("string argument expected for 'addr'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                let utf8addr = ffi::PyUnicode_AsUTF8(val);
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
                match CStr::from_ptr(utf8addr).to_str() {
                    Ok(addrstr) => {
                        addr = Some(String::from(addrstr));
                    }
                    Err(_) => {
                        ffi::PyErr_SetString(
                            ffi::PyExc_TypeError,
                            ffi::c_str!("string argument expected for 'addr'").as_ptr(),
                        );
                        return ptr::null_mut();
                    }
                }
            }
            NUM_WORKERS => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'num_workers'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                num_workers = ffi::PyLong_AsLong(val) as usize;
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            MAX_NUMBER_HEADERS => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'max_number_headers'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                max_number_headers = ffi::PyLong_AsLong(val) as usize;
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            ASYNC_LOGGING => {
                if ffi::PyBool_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("bool argument expected for 'async_logging'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                async_logging = val == ffi::Py_True();
            }
            CHUNKED_TRANSFER => {
                if ffi::PyBool_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("bool argument expected for 'chunked_transfer'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                chunked_transfer = val == ffi::Py_True();
            }
            MAX_REUSE_COUNT => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'max_reuse_count'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                max_reuse_count = ffi::PyLong_AsLong(val) as u8;
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            KEEPALIVE_TIMEOUT => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'keepalive_timeout'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                keepalive_timeout = ffi::PyLong_AsLong(val) as u8;
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            QMON_WARN_THRESHOLD => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'qmon_warn_threshold'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                qmon_warn_threshold = Some(ffi::PyLong_AsLong(val) as usize);
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            SEND_TIMEOUT => {
                if ffi::PyLong_Check(val) == 0 {
                    ffi::PyErr_SetString(
                        ffi::PyExc_TypeError,
                        ffi::c_str!("integer argument expected for 'send_timeout'").as_ptr(),
                    );
                    return ptr::null_mut();
                }
                send_timeout = ffi::PyLong_AsLong(val) as u8;
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
            }
            _ => {}
        }
    }

    // Keyword parameters
    if !kwnames.is_null() {
        let nkw = ffi::PyTuple_Size(kwnames);
        if nkw == -1 {
            return ptr::null_mut();
        }
        for idx in 0..nkw {
            let kw = ffi::PyTuple_GetItem(kwnames, idx);
            for prm in PARAMS {
                let cstrprm = CString::new(*prm).expect("Invalid parameter code");
                if ffi::PyUnicode_CompareWithASCIIString(kw, cstrprm.as_ptr()) == 0 {
                    let val = *args.add((nargs + idx) as usize);
                    match *prm {
                        APPLICATION => {
                            application = val;
                            break;
                        }
                        ADDR => {
                            if ffi::PyUnicode_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("string argument expected for 'addr'").as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            let utf8addr = ffi::PyUnicode_AsUTF8(val);
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            match CStr::from_ptr(utf8addr).to_str() {
                                Ok(addrstr) => {
                                    addr = Some(String::from(addrstr));
                                }
                                Err(_) => {
                                    ffi::PyErr_SetString(
                                        ffi::PyExc_TypeError,
                                        ffi::c_str!("string argument expected for 'addr'").as_ptr(),
                                    );
                                    return ptr::null_mut();
                                }
                            }
                            break;
                        }
                        NUM_WORKERS => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("integer argument expected for 'num_workers'")
                                        .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            num_workers = ffi::PyLong_AsLong(val) as usize;
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        MAX_NUMBER_HEADERS => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!(
                                        "integer argument expected for 'max_number_headers'"
                                    )
                                    .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            max_number_headers = ffi::PyLong_AsLong(val) as usize;
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        ASYNC_LOGGING => {
                            if ffi::PyBool_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("bool argument expected for 'async_logging'")
                                        .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            async_logging = val == ffi::Py_True();
                            break;
                        }
                        CHUNKED_TRANSFER => {
                            if ffi::PyBool_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("bool argument expected for 'chunked_transfer'")
                                        .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            chunked_transfer = val == ffi::Py_True();
                            break;
                        }
                        MAX_REUSE_COUNT => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("integer argument expected for 'max_reuse_count'")
                                        .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            max_reuse_count = ffi::PyLong_AsLong(val) as u8;
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        KEEPALIVE_TIMEOUT => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!(
                                        "integer argument expected for 'keepalive_timeout'"
                                    )
                                    .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            keepalive_timeout = ffi::PyLong_AsLong(val) as u8;
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        QMON_WARN_THRESHOLD => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!(
                                        "integer argument expected for 'qmon_warn_threshold'"
                                    )
                                    .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            qmon_warn_threshold = Some(ffi::PyLong_AsLong(val) as usize);
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        SEND_TIMEOUT => {
                            if ffi::PyLong_Check(val) == 0 {
                                ffi::PyErr_SetString(
                                    ffi::PyExc_TypeError,
                                    ffi::c_str!("integer argument expected for 'send_timeout'")
                                        .as_ptr(),
                                );
                                return ptr::null_mut();
                            }
                            send_timeout = ffi::PyLong_AsLong(val) as u8;
                            if !ffi::PyErr_Occurred().is_null() {
                                return ptr::null_mut();
                            }
                            break;
                        }
                        _ => {}
                    }
                }
            }
        }
    }

    let py = Python::assume_gil_acquired();
    match serve(
        py,
        application,
        addr,
        num_workers,
        max_number_headers,
        async_logging,
        chunked_transfer,
        max_reuse_count,
        keepalive_timeout,
        qmon_warn_threshold,
        send_timeout,
    ) {
        Ok(_) => slf,
        Err(_) => ptr::null_mut(),
    }
}
