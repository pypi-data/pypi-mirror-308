#![allow(clippy::transmute_ptr_to_ptr, clippy::zero_ptr)] // suppress warnings in py_class invocation
use cpython::{
    py_class, PyClone, PyDict, PyDrop, PyErr, PyList, PyObject, PyResult, PyTuple, PyType, Python,
    PythonObject, PythonObjectDowncastError, PythonObjectWithCheckedDowncast,
    PythonObjectWithTypeObject,
};
use log::error;
use pyo3_ffi as ffi;
use std::boxed::Box;
use std::cell::{Cell, RefCell};
use std::ptr::addr_of_mut;
use std::{cmp, ptr};

use crate::pyutils::PyTypeObject_INIT;
use crate::request::CONTENT_LENGTH_HEADER;

type WSGIHeaders = Vec<(String, Vec<(String, String)>)>;

pub struct StartResponse {
    _unsafe_inner: PyObject,
}
impl PythonObject for StartResponse {
    #[inline]
    fn as_object(&self) -> &PyObject {
        &self._unsafe_inner
    }
    #[inline]
    fn into_object(self) -> PyObject {
        self._unsafe_inner
    }
    /// Unchecked downcast from PyObject to Self.
    /// Undefined behavior if the input object does not have the expected type.
    #[inline]
    unsafe fn unchecked_downcast_from(obj: PyObject) -> Self {
        StartResponse { _unsafe_inner: obj }
    }
}
impl PythonObjectWithCheckedDowncast for StartResponse {
    #[inline]
    fn downcast_from(
        py: Python<'_>,
        obj: PyObject,
    ) -> Result<StartResponse, PythonObjectDowncastError<'_>> {
        if py.get_type::<StartResponse>().is_instance(py, &obj) {
            Ok(StartResponse { _unsafe_inner: obj })
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "StartResponse",
                obj.get_type(py),
            ))
        }
    }
    #[inline]
    fn downcast_borrow_from<'a, 'p>(
        py: Python<'p>,
        obj: &'a PyObject,
    ) -> Result<&'a StartResponse, PythonObjectDowncastError<'p>> {
        if py.get_type::<StartResponse>().is_instance(py, obj) {
            unsafe { Ok(std::mem::transmute::<&PyObject, &StartResponse>(obj)) }
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "StartResponse",
                obj.get_type(py),
            ))
        }
    }
}
impl py_class::BaseObject for StartResponse {
    type InitType = (
        PyDict,
        RefCell<WSGIHeaders>,
        RefCell<WSGIHeaders>,
        Cell<Option<usize>>,
        Cell<usize>,
    );
    #[inline]
    fn size() -> usize {
        py_class::data_new_size::<Cell<usize>>(py_class::data_new_size::<Cell<Option<usize>>>(
            py_class::data_new_size::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(
                py_class::data_new_size::<
                PyDict,
            >(
                <PyObject as py_class::BaseObject>::size(),
            )
            )),
        ))
    }
    unsafe fn alloc(
        py: Python,
        ty: &PyType,
        (environ, headers_set, headers_sent, content_length, content_bytes_written): Self::InitType,
    ) -> PyResult<PyObject> {
        let obj = <PyObject as py_class::BaseObject>::alloc(py, ty, ())?;
        py_class::data_init::<PyDict>(
            py,
            &obj,
            py_class::data_offset::<PyDict>(<PyObject as py_class::BaseObject>::size()),
            environ,
        );
        py_class::data_init::<RefCell<WSGIHeaders>>(
            py,
            &obj,
            py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<PyDict>(
                <PyObject as py_class::BaseObject>::size(),
            )),
            headers_set,
        );
        py_class::data_init::<RefCell<WSGIHeaders>>(
            py,
            &obj,
            py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(py_class::data_new_size::<
                PyDict,
            >(
                <PyObject as py_class::BaseObject>::size(),
            ))),
            headers_sent,
        );
        py_class::data_init::<Cell<Option<usize>>>(
            py,
            &obj,
            py_class::data_offset::<Cell<Option<usize>>>(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(
                py_class::data_new_size::<PyDict>(<PyObject as py_class::BaseObject>::size()),
            ))),
            content_length,
        );
        py_class::data_init::<Cell<usize>>(
            py,
            &obj,
            py_class::data_offset::<Cell<usize>>(py_class::data_new_size::<Cell<Option<usize>>>(
                py_class::data_new_size::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                    RefCell<WSGIHeaders>,
                >(
                    py_class::data_new_size::<PyDict>(<PyObject as py_class::BaseObject>::size()),
                )),
            )),
            content_bytes_written,
        );
        Ok(obj)
    }
    unsafe fn dealloc(py: Python, obj: *mut ffi::PyObject) {
        py_class::data_drop::<PyDict>(
            py,
            obj,
            py_class::data_offset::<PyDict>(<PyObject as py_class::BaseObject>::size()),
        );
        py_class::data_drop::<RefCell<WSGIHeaders>>(
            py,
            obj,
            py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<PyDict>(
                <PyObject as py_class::BaseObject>::size(),
            )),
        );
        py_class::data_drop::<RefCell<WSGIHeaders>>(
            py,
            obj,
            py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(py_class::data_new_size::<
                PyDict,
            >(
                <PyObject as py_class::BaseObject>::size(),
            ))),
        );
        py_class::data_drop::<Cell<Option<usize>>>(
            py,
            obj,
            py_class::data_offset::<Cell<Option<usize>>>(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(py_class::data_new_size::<
                RefCell<WSGIHeaders>,
            >(
                py_class::data_new_size::<PyDict>(<PyObject as py_class::BaseObject>::size()),
            ))),
        );
        py_class::data_drop::<Cell<usize>>(
            py,
            obj,
            py_class::data_offset::<Cell<usize>>(py_class::data_new_size::<Cell<Option<usize>>>(
                py_class::data_new_size::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                    RefCell<WSGIHeaders>,
                >(
                    py_class::data_new_size::<PyDict>(<PyObject as py_class::BaseObject>::size()),
                )),
            )),
        );
        <PyObject as py_class::BaseObject>::dealloc(py, obj)
    }
}
impl StartResponse {
    fn environ<'a>(&'a self, py: Python<'a>) -> &'a PyDict {
        unsafe {
            py_class::data_get::<PyDict>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<PyDict>(<PyObject as py_class::BaseObject>::size()),
            )
        }
    }

    fn headers_set<'a>(&'a self, py: Python<'a>) -> &'a RefCell<WSGIHeaders> {
        unsafe {
            py_class::data_get::<RefCell<WSGIHeaders>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<PyDict>(
                    <PyObject as py_class::BaseObject>::size(),
                )),
            )
        }
    }

    fn headers_sent<'a>(&'a self, py: Python<'a>) -> &'a RefCell<WSGIHeaders> {
        unsafe {
            py_class::data_get::<RefCell<WSGIHeaders>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                    RefCell<WSGIHeaders>,
                >(
                    py_class::data_new_size::<PyDict>(<PyObject as py_class::BaseObject>::size()),
                )),
            )
        }
    }

    fn content_length<'a>(&'a self, py: Python<'a>) -> &'a Cell<Option<usize>> {
        unsafe {
            py_class::data_get::<Cell<Option<usize>>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<Cell<Option<usize>>>(py_class::data_new_size::<
                    RefCell<WSGIHeaders>,
                >(
                    py_class::data_new_size::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                        PyDict,
                    >(
                        <PyObject as py_class::BaseObject>::size(),
                    )),
                )),
            )
        }
    }

    fn content_bytes_written<'a>(&'a self, py: Python<'a>) -> &'a Cell<usize> {
        unsafe {
            py_class::data_get::<Cell<usize>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<Cell<usize>>(
                    py_class::data_new_size::<Cell<Option<usize>>>(py_class::data_new_size::<
                        RefCell<WSGIHeaders>,
                    >(
                        py_class::data_new_size::<RefCell<WSGIHeaders>>(py_class::data_new_size::<
                            PyDict,
                        >(
                            <PyObject as py_class::BaseObject>::size(),
                        )),
                    )),
                ),
            )
        }
    }

    pub fn __call__(
        &self,
        py: Python,
        status: PyObject,
        headers: PyObject,
        exc_info: Option<PyObject>,
    ) -> PyResult<PyObject> {
        let _ = py;
        let response_headers: &PyList = headers.extract(py)?;
        if exc_info.is_some() {
            {
                let lvl = ::log::Level::Error;
                if lvl <= ::log::STATIC_MAX_LEVEL && lvl <= ::log::max_level() {
                    ::log::__private_api::log(
                        format_args!("exc_info from application: {0:?}", exc_info),
                        lvl,
                        &(
                            "pyruvate::startresponse",
                            "pyruvate::startresponse",
                            ::log::__private_api::loc(),
                        ),
                        (),
                    );
                }
            };
        }
        let mut rh = Vec::<(String, String)>::new();
        for ob in response_headers.iter(py) {
            let tp = ob.extract::<PyTuple>(py)?;
            rh.push((
                tp.get_item(py, 0).to_string(),
                tp.get_item(py, 1).to_string(),
            ));
        }
        self.headers_set(py)
            .replace(<[_]>::into_vec(Box::new([(status.to_string(), rh)])));
        Ok(py.None())
    }

    pub fn create_instance(
        py: Python,
        environ: PyDict,
        headers_set: RefCell<WSGIHeaders>,
        headers_sent: RefCell<WSGIHeaders>,
        content_length: Cell<Option<usize>>,
        content_bytes_written: Cell<usize>,
    ) -> PyResult<StartResponse> {
        let obj = unsafe {
            <StartResponse as py_class::BaseObject>::alloc(
                py,
                &py.get_type::<StartResponse>(),
                (
                    environ,
                    headers_set,
                    headers_sent,
                    content_length,
                    content_bytes_written,
                ),
            )
        }?;
        Ok(StartResponse { _unsafe_inner: obj })
    }
}
static mut TYPE_OBJECT: ffi::PyTypeObject = ffi::PyTypeObject {
    tp_call: {
        unsafe extern "C" fn wrap_call(
            slf: *mut ffi::PyObject,
            args: *mut ffi::PyObject,
            kwargs: *mut ffi::PyObject,
        ) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            // Defaults
            let mut status: PyObject = py.None();
            let mut headers: PyObject = py.None();
            let mut exc_info: Option<PyObject> = None;

            let nargs = ffi::PyTuple_Size(args);
            if !ffi::PyErr_Occurred().is_null() {
                return ptr::null_mut();
            }
            if !(2..=3).contains(&nargs) {
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("__call__ expects at least 2 and at most 3 positional arguments")
                        .as_ptr(),
                );
                return std::ptr::null_mut();
            }
            // Positional parameters
            for idx in 0..nargs {
                let val = ffi::PyTuple_GetItem(args, idx);
                if !ffi::PyErr_Occurred().is_null() {
                    return ptr::null_mut();
                }
                match idx {
                    0 => {
                        status = PyObject::from_borrowed_ptr(py, val);
                    }
                    1 => {
                        headers = PyObject::from_borrowed_ptr(py, val);
                    }
                    2 => {
                        if ffi::Py_IsNone(val) != 0 {
                            exc_info = Some(PyObject::from_borrowed_ptr(py, val));
                        }
                    }
                    _ => {}
                }
            }
            // Keyword parameters
            if !kwargs.is_null() {
                // See https://peps.python.org/pep-3333/#the-start-response-callable:
                // "As with all WSGI callables, the arguments must be supplied positionally, not by
                // keyword."
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("__call__ expects only positional arguments").as_ptr(),
                );
                return std::ptr::null_mut();
            }
            let slf = PyObject::from_borrowed_ptr(py, slf).unchecked_cast_into::<StartResponse>();
            let ret = slf.__call__(py, status, headers, exc_info);
            PyDrop::release_ref(slf, py);
            match ret {
                Ok(obj) => obj.as_ptr(),
                Err(_) => ptr::null_mut(),
            }
        }
        Some(wrap_call)
    },
    tp_dealloc: Some(py_class::tp_dealloc_callback::<StartResponse>),
    tp_flags: py_class::TPFLAGS_DEFAULT,
    tp_traverse: None,
    ..PyTypeObject_INIT
};
static mut INIT_ACTIVE: bool = false;

impl PythonObjectWithTypeObject for StartResponse {
    fn type_object(py: Python) -> PyType {
        <StartResponse as py_class::PythonObjectFromPyClassMacro>::initialize(py, None)
            .expect("An error occurred while initializing class StartResponse")
    }
}

impl py_class::PythonObjectFromPyClassMacro for StartResponse {
    fn initialize(py: Python, module_name: Option<&str>) -> PyResult<PyType> {
        unsafe {
            if (TYPE_OBJECT.tp_flags & ffi::Py_TPFLAGS_READY) != 0 {
                return Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)));
            }
            if INIT_ACTIVE {
                {
                    panic!("Reentrancy detected: already initializing class StartResponse",);
                }
            }
            INIT_ACTIVE = true;

            TYPE_OBJECT.ob_base.ob_base.ob_type = addr_of_mut!(ffi::PyType_Type);
            TYPE_OBJECT.tp_name = py_class::build_tp_name(module_name, "StartResponse");
            TYPE_OBJECT.tp_basicsize =
                <StartResponse as py_class::BaseObject>::size() as ffi::Py_ssize_t;
            TYPE_OBJECT.tp_as_sequence = 0 as *mut ffi::PySequenceMethods;
            TYPE_OBJECT.tp_as_number = 0 as *mut ffi::PyNumberMethods;
            TYPE_OBJECT.tp_getset = 0 as *mut ffi::PyGetSetDef;

            let res = if ffi::PyType_Ready(addr_of_mut!(TYPE_OBJECT)) == 0 {
                Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)))
            } else {
                Err(PyErr::fetch(py))
            };

            INIT_ACTIVE = false;
            res
        }
    }
}

pub trait WriteResponse {
    // Put this in a trait for more flexibility.
    // rust-cpython can't handle some types we are using here.
    #[allow(clippy::new_ret_no_self)]
    fn new(environ: PyDict, headers_set: WSGIHeaders, py: Python) -> PyResult<StartResponse>;
    fn content_complete(&self, py: Python) -> bool;
    fn write(
        &mut self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_tranfer: bool,
        py: Python,
    );
    fn environ(&self, py: Python) -> PyDict;
    fn content_length(&self, py: Python) -> Option<usize>;
    fn content_bytes_written(&self, py: Python) -> usize;
    fn headers_not_sent(&self, py: Python) -> bool;
}

impl WriteResponse for StartResponse {
    fn new(environ: PyDict, headers_set: WSGIHeaders, py: Python) -> PyResult<StartResponse> {
        StartResponse::create_instance(
            py,
            environ,
            RefCell::new(headers_set),
            RefCell::new(Vec::new()),
            Cell::new(None),
            Cell::new(0),
        )
    }

    fn content_complete(&self, py: Python) -> bool {
        if let Some(length) = self.content_length(py).get() {
            self.content_bytes_written(py).get() >= length
        } else {
            false
        }
    }

    fn write(
        &mut self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_transfer: bool,
        py: Python,
    ) {
        if self.headers_sent(py).borrow().is_empty() {
            if self.headers_set(py).borrow().is_empty() {
                error!("write() before start_response()")
            }
            // Before the first output, send the stored headers
            self.headers_sent(py)
                .replace(self.headers_set(py).borrow().clone());
            let respinfo = self.headers_set(py).borrow_mut().pop(); // headers_sent|set should have only one element
            match respinfo {
                Some(respinfo) => {
                    let response_headers: Vec<(String, String)> = respinfo.1;
                    let status: String = respinfo.0;
                    output.extend(b"HTTP/1.1 ");
                    output.extend(status.as_bytes());
                    output.extend(b"\r\n");
                    let mut maybe_chunked = true;
                    for header in response_headers.iter() {
                        let headername = &header.0;
                        output.extend(headername.as_bytes());
                        output.extend(b": ");
                        output.extend(header.1.as_bytes());
                        output.extend(b"\r\n");
                        if headername.to_ascii_uppercase() == CONTENT_LENGTH_HEADER {
                            match header.1.parse::<usize>() {
                                Ok(length) => {
                                    self.content_length(py).set(Some(length));
                                    // no need to use chunked transfer encoding if we have a valid content length header,
                                    // see e.g. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding#Chunked_encoding
                                    maybe_chunked = false;
                                }
                                Err(e) => error!("Could not parse Content-Length header: {:?}", e),
                            }
                        }
                    }
                    output.extend(b"Via: pyruvate\r\n");
                    if close_connection {
                        output.extend(b"Connection: close\r\n");
                    } else {
                        output.extend(b"Connection: keep-alive\r\n");
                    }
                    if maybe_chunked && chunked_transfer {
                        output.extend(b"Transfer-Encoding: chunked\r\n");
                    }
                }
                None => {
                    error!("write(): No respinfo!");
                }
            }
            output.extend(b"\r\n");
        }
        match self.content_length(py).get() {
            Some(length) => {
                let cbw = self.content_bytes_written(py).get();
                if length > cbw {
                    let num = cmp::min(length - cbw, data.len());
                    if num > 0 {
                        output.extend(&data[..num]);
                        self.content_bytes_written(py).set(cbw + num);
                    }
                }
            }
            None => {
                // no content length header, use
                // chunked transfer encoding if specified
                let cbw = self.content_bytes_written(py).get();
                let length = data.len();
                if length > 0 {
                    if chunked_transfer {
                        output.extend(format!("{length:X}").as_bytes());
                        output.extend(b"\r\n");
                        output.extend(data);
                        output.extend(b"\r\n");
                    } else {
                        output.extend(data);
                    }
                    self.content_bytes_written(py).set(cbw + length);
                }
            }
        }
    }

    fn environ(&self, py: Python) -> PyDict {
        self.environ(py).clone_ref(py)
    }

    fn content_length(&self, py: Python) -> Option<usize> {
        self.content_length(py).get()
    }

    fn content_bytes_written(&self, py: Python) -> usize {
        self.content_bytes_written(py).get()
    }

    fn headers_not_sent(&self, py: Python) -> bool {
        self.headers_sent(py).borrow().is_empty()
    }
}

#[cfg(test)]
mod tests {
    use cpython::{ObjectProtocol, PyClone, PyDict, PyTuple, Python, PythonObject, ToPyObject};
    use log::LevelFilter;
    use simplelog::{Config, WriteLogger};
    use std::env::temp_dir;
    use std::fs::File;
    use std::io::Read;

    use crate::startresponse::{StartResponse, WriteResponse};

    #[test]
    fn test_write() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let data = b"Hello world!\n";
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        assert_eq!(sr.content_length(py).get(), None);
        assert_eq!(WriteResponse::content_length(&sr, py), None);
        assert!(!sr.content_complete(py));
        let mut output: Vec<u8> = Vec::new();
        sr.write(data, &mut output, true, false, py);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello world!\n";
        assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
        assert!(!sr.content_complete(py));
        // chunked transfer requested and no content length header
        // The final chunk will be missing; it's written in WSGIResponse::write_chunk
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n\r\nD\r\nHello world!\n";
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        assert!(!sr.content_complete(py));
        sr.write(data, &mut output, true, true, py);
        assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
        assert!(!sr.content_complete(py));
    }

    #[test]
    fn test_honour_content_length_header() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete(py));
        sr.write(data, &mut output, true, false, py);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
        assert_eq!(sr.content_length(py).get(), Some(5));
        assert_eq!(WriteResponse::content_length(&sr, py), Some(5));
        assert_eq!(sr.content_bytes_written(py).get(), 5);
        assert!(sr.content_complete(py));
        assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
        // chunked transfer set - ignored if content length header available
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        assert!(!sr.content_complete(py));
        sr.write(data, &mut output, true, true, py);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
        assert_eq!(sr.content_length(py).get(), Some(5));
        assert_eq!(sr.content_bytes_written(py).get(), 5);
        assert!(sr.content_complete(py));
        assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_exc_info_is_none() {
        // do not display an error message when exc_info passed
        // by application is None
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let pycode = py.run(
            r#"
status = '200 OK'
response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
exc_info = 'Foo'
"#,
            None,
            Some(&locals),
        );
        match pycode {
            Ok(_) => {
                let status = locals.get_item(py, "status").unwrap();
                let headers = locals.get_item(py, "response_headers").unwrap();
                let exc_info = locals.get_item(py, "exc_info").unwrap();
                let environ = PyDict::new(py);
                // create logger
                let mut path = temp_dir();
                path.push("foo42.log");
                let path = path.into_os_string();
                WriteLogger::init(
                    LevelFilter::Info,
                    Config::default(),
                    File::create(&path).unwrap(),
                )
                .unwrap();

                let sr = StartResponse::new(environ, Vec::new(), py).unwrap();
                match sr.__call__(py, status.clone_ref(py), headers.clone_ref(py), None) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(!got.contains("exc_info"));
                        assert!(!got.contains("Foo"));
                    }
                    _ => assert!(false),
                }
                match sr.__call__(py, status, headers, Some(exc_info)) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(got.len() > 0);
                        assert!(got.contains("exc_info"));
                        assert!(got.contains("Foo"));
                    }
                    _ => assert!(false),
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_call_nargs_headers_missing() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let sr = StartResponse::new(environ, headers, py).unwrap();
        match sr.as_object().call(
            py,
            PyTuple::new(py, &["200 OK".to_py_object(py).into_object()]),
            None,
        ) {
            Ok(_) => assert!(false),
            Err(_) => (),
        }
    }

    #[test]
    fn test_call_with_kwargs() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let sr = StartResponse::new(environ, headers, py).unwrap();
        let kwargs = PyDict::new(py);
        kwargs.set_item(py, "environ", PyDict::new(py)).unwrap();
        kwargs
            .set_item(py, "headers", PyTuple::new(py, &[]))
            .unwrap();
        match sr
            .as_object()
            .call(py, PyTuple::new(py, &[]), Some(&kwargs))
        {
            Ok(_) => assert!(false),
            Err(_) => (),
        }
    }
}
