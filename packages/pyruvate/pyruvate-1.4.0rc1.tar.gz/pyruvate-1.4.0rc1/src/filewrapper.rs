#![allow(
    clippy::transmute_ptr_to_ptr,
    clippy::zero_ptr,
    clippy::manual_strip,
    unused_variables
)] // suppress warnings in py_class invocation
use cpython::{
    py_class, NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyDrop, PyErr, PyObject, PyResult,
    PyTuple, PyType, Python, PythonObject, PythonObjectDowncastError,
    PythonObjectWithCheckedDowncast, PythonObjectWithTypeObject, ToPyObject,
};
use errno::errno;
use log::{debug, error};
use pyo3_ffi as ffi;
use std::cell::RefCell;
use std::cmp;
use std::io::Error;
use std::os::unix::io::{AsRawFd, RawFd};
use std::ptr::{self, addr_of_mut};
use std::result::Result;

use crate::pyutils::{close_pyobject, with_released_gil, PyTypeObject_INIT};
use crate::transport::would_block;

// This is the maximum the Linux kernel will write in a single sendfile call.
#[cfg(target_os = "linux")]
const SENDFILE_MAXSIZE: isize = 0x7fff_f000;

pub struct SendFileInfo {
    pub content_length: isize,
    pub blocksize: isize,
    pub offset: libc::off_t,
    pub fd: RawFd,
    pub done: bool,
}

impl SendFileInfo {
    pub fn new(fd: RawFd, blocksize: isize) -> Self {
        Self {
            content_length: -1,
            blocksize,
            offset: 0,
            fd,
            done: false,
        }
    }

    // true: chunk written completely, false: there's more
    #[cfg(target_os = "linux")]
    pub fn send_file(&mut self, out: &mut dyn AsRawFd) -> (bool, usize) {
        debug!("Sending file");
        let mut count = if self.blocksize < 0 {
            SENDFILE_MAXSIZE
        } else {
            self.blocksize
        };
        if self.content_length >= 0 {
            count = cmp::min(self.content_length - self.offset as isize, count);
        }
        self.done = (count == 0) || {
            match unsafe {
                libc::sendfile(out.as_raw_fd(), self.fd, &mut self.offset, count as usize)
            } {
                -1 => {
                    // will cover the case where count is too large as EOVERFLOW
                    // s. sendfile(2)
                    let err = Error::from(errno());
                    if !would_block(&err) {
                        error!("Could not sendfile(): {:?}", err);
                        true
                    } else {
                        false
                    }
                }
                // 0 bytes written, assuming we're done
                0 => true,
                _ if (self.content_length > 0) => self.content_length == self.offset as isize,
                // If no content length is given, num_written might be less than count.
                // However the subsequent call will write 0 bytes -> done.
                _ => false,
            }
        };
        (self.done, self.offset as usize)
    }

    #[cfg(target_os = "macos")]
    pub fn send_file(&mut self, out: &mut dyn AsRawFd) -> (bool, usize) {
        debug!("Sending file");
        let mut count: i64 = cmp::max(0, self.blocksize as i64);
        if (self.content_length > 0) && (count > 0) {
            count = cmp::min(self.content_length as i64 - self.offset, count);
        }
        self.done = {
            let res = unsafe {
                libc::sendfile(
                    self.fd,
                    out.as_raw_fd(),
                    self.offset,
                    &mut count,
                    std::ptr::null_mut(),
                    0,
                )
            };
            if count == 0 {
                true
            } else {
                self.offset += count;
                if res == -1 {
                    let err = Error::from(errno());
                    if !would_block(&err) {
                        error!("Could not sendfile(): {:?}", err);
                        true
                    } else {
                        false
                    }
                } else {
                    if self.content_length > 0 {
                        self.content_length <= self.offset as isize
                    } else {
                        false
                    }
                }
            }
        };
        (self.done, self.offset as usize)
    }

    fn update_content_length(&mut self, content_length: isize) {
        self.content_length = content_length;
        if self.blocksize > content_length {
            self.blocksize = content_length;
        }
    }
}

pub struct FileWrapper {
    _unsafe_inner: PyObject,
}
impl PythonObject for FileWrapper {
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
        FileWrapper { _unsafe_inner: obj }
    }
}
impl PythonObjectWithCheckedDowncast for FileWrapper {
    #[inline]
    fn downcast_from(
        py: Python<'_>,
        obj: PyObject,
    ) -> Result<FileWrapper, PythonObjectDowncastError<'_>> {
        if py.get_type::<FileWrapper>().is_instance(py, &obj) {
            Ok(FileWrapper { _unsafe_inner: obj })
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "FileWrapper",
                obj.get_type(py),
            ))
        }
    }
    #[inline]
    fn downcast_borrow_from<'a, 'p>(
        py: Python<'p>,
        obj: &'a PyObject,
    ) -> Result<&'a FileWrapper, PythonObjectDowncastError<'p>> {
        if py.get_type::<FileWrapper>().is_instance(py, obj) {
            unsafe { Ok(std::mem::transmute::<&PyObject, &FileWrapper>(obj)) }
        } else {
            Err(PythonObjectDowncastError::new(
                py,
                "FileWrapper",
                obj.get_type(py),
            ))
        }
    }
}
impl py_class::BaseObject for FileWrapper {
    type InitType = (RefCell<PyObject>, RefCell<SendFileInfo>);
    #[inline]
    fn size() -> usize {
        py_class::data_new_size::<RefCell<SendFileInfo>>(
            py_class::data_new_size::<RefCell<PyObject>>(<PyObject as py_class::BaseObject>::size()),
        )
    }
    unsafe fn alloc(
        py: Python,
        ty: &PyType,
        (filelike, sendfileinfo): Self::InitType,
    ) -> PyResult<PyObject> {
        let obj = <PyObject as py_class::BaseObject>::alloc(py, ty, ())?;
        py_class::data_init::<RefCell<PyObject>>(
            py,
            &obj,
            py_class::data_offset::<RefCell<PyObject>>(<PyObject as py_class::BaseObject>::size()),
            filelike,
        );
        py_class::data_init::<RefCell<SendFileInfo>>(
            py,
            &obj,
            py_class::data_offset::<RefCell<SendFileInfo>>(py_class::data_new_size::<
                RefCell<PyObject>,
            >(
                <PyObject as py_class::BaseObject>::size(),
            )),
            sendfileinfo,
        );
        Ok(obj)
    }
    unsafe fn dealloc(py: Python, obj: *mut ffi::PyObject) {
        py_class::data_drop::<RefCell<PyObject>>(
            py,
            obj,
            py_class::data_offset::<RefCell<PyObject>>(<PyObject as py_class::BaseObject>::size()),
        );
        py_class::data_drop::<RefCell<SendFileInfo>>(
            py,
            obj,
            py_class::data_offset::<RefCell<SendFileInfo>>(py_class::data_new_size::<
                RefCell<PyObject>,
            >(
                <PyObject as py_class::BaseObject>::size(),
            )),
        );
        <PyObject as py_class::BaseObject>::dealloc(py, obj)
    }
}
impl FileWrapper {
    fn filelike<'a>(&'a self, py: Python<'a>) -> &'a RefCell<PyObject> {
        unsafe {
            py_class::data_get::<RefCell<PyObject>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<RefCell<PyObject>>(
                    <PyObject as py_class::BaseObject>::size(),
                ),
            )
        }
    }

    fn sendfileinfo<'a>(&'a self, py: Python<'a>) -> &'a RefCell<SendFileInfo> {
        unsafe {
            py_class::data_get::<RefCell<SendFileInfo>>(
                py,
                &self._unsafe_inner,
                py_class::data_offset::<RefCell<SendFileInfo>>(py_class::data_new_size::<
                    RefCell<PyObject>,
                >(
                    <PyObject as py_class::BaseObject>::size(),
                )),
            )
        }
    }

    pub fn __new__(
        _cls: &PyType,
        py: Python,
        filelike: PyObject,
        blocksize: Option<isize>,
    ) -> PyResult<Self> {
        let _ = py;
        let mut filelike = RefCell::new(filelike);
        let blocksize = blocksize.unwrap_or(-1);
        let mut fd: RawFd = -1;
        if let Ok(fdpyob) = filelike.get_mut().call_method(py, "fileno", NoArgs, None) {
            if let Ok(pyfd) = fdpyob.extract(py) {
                fd = pyfd;
            }
        }
        let sendfileinfo = RefCell::new(SendFileInfo::new(fd, blocksize));
        FileWrapper::create_instance(py, filelike, sendfileinfo)
    }

    pub fn __iter__(&self, py: Python) -> PyResult<Self> {
        let _ = py;
        Ok(self.clone_ref(py))
    }

    pub fn __next__(&self, py: Python) -> PyResult<Option<PyObject>> {
        let _ = py;
        let py = unsafe { Python::assume_gil_acquired() };
        let sfi = self.sendfileinfo(py).borrow();
        if sfi.fd != -1 {
            return if sfi.done {
                Ok(None)
            } else {
                Ok(Some(PyBytes::new(py, b"").into_object()))
            };
        }
        let bytes = self.filelike(py).borrow_mut().call_method(
            py,
            "read",
            PyTuple::new(
                py,
                &[self
                    .sendfileinfo(py)
                    .borrow()
                    .blocksize
                    .to_py_object(py)
                    .into_object()],
            ),
            None,
        )?;
        if !bytes.is_none(py) && (bytes.get_type(py) == py.get_type::<PyBytes>()) {
            if bytes.cast_as::<PyBytes>(py)?.data(py).is_empty() {
                Ok(None)
            } else {
                Ok(Some(bytes))
            }
        } else {
            match close_pyobject(self.as_object(), py) {
                Err(e) => e.print_and_set_sys_last_vars(py),
                Ok(_) => {
                    let lvl = ::log::Level::Debug;
                    if lvl <= ::log::STATIC_MAX_LEVEL && lvl <= ::log::max_level() {
                        ::log::__private_api::log(
                            format_args!("WSGIResponse dropped successfully"),
                            lvl,
                            &(
                                "pyruvate::filewrapper",
                                "pyruvate::filewrapper",
                                ::log::__private_api::loc(),
                            ),
                            (),
                        );
                    }
                }
            }
            Ok(None)
        }
    }

    pub fn close(&self, py: Python) -> PyResult<PyObject> {
        let _ = py;
        match close_pyobject(&self.filelike(py).borrow_mut(), py) {
            Ok(_) => Ok(py.None()),
            Err(e) => Err(e),
        }
    }

    pub fn create_instance(
        py: Python,
        filelike: RefCell<PyObject>,
        sendfileinfo: RefCell<SendFileInfo>,
    ) -> PyResult<FileWrapper> {
        let obj = unsafe {
            <FileWrapper as py_class::BaseObject>::alloc(
                py,
                &py.get_type::<FileWrapper>(),
                (filelike, sendfileinfo),
            )
        }?;
        Ok(FileWrapper { _unsafe_inner: obj })
    }
}
static mut TYPE_OBJECT: ffi::PyTypeObject = ffi::PyTypeObject {
    tp_new: {
        unsafe extern "C" fn wrap_newfunc(
            cls: *mut ffi::PyTypeObject,
            args: *mut ffi::PyObject,
            kwargs: *mut ffi::PyObject,
        ) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            // Defaults
            let mut filelike: PyObject = py.None();
            let mut blocksize = None;

            let nargs = ffi::PyTuple_Size(args);
            if !ffi::PyErr_Occurred().is_null() {
                return ptr::null_mut();
            }
            if nargs > 2 {
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("__new__ expects at most 2 positional argument").as_ptr(),
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
                        filelike = PyObject::from_borrowed_ptr(py, val);
                    }
                    1 => {
                        if ffi::PyLong_Check(val) == 0 {
                            ffi::PyErr_SetString(
                                ffi::PyExc_TypeError,
                                ffi::c_str!("integer argument expected for 'blocksize'").as_ptr(),
                            );
                            return ptr::null_mut();
                        }
                        blocksize = Some(ffi::PyLong_AsLong(val) as isize);
                        if !ffi::PyErr_Occurred().is_null() {
                            return ptr::null_mut();
                        }
                    }
                    _ => {}
                }
            }
            // Keyword parameters
            if !kwargs.is_null() {
                // See https://peps.python.org/pep-3333/#optional-platform-specific-file-handling:
                // "...must be a callable that accepts one required positional parameter, and one optional positional parameter."
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("FileWrapper expects only positional arguments").as_ptr(),
                );
                return std::ptr::null_mut();
            }
            if filelike.is_none(py) {
                ffi::PyErr_SetString(
                    ffi::PyExc_TypeError,
                    ffi::c_str!("Invalid type for filelike").as_ptr(),
                );
                return ptr::null_mut();
            }
            let cls = PyType::from_type_ptr(py, cls);
            let ret = FileWrapper::__new__(&cls, py, filelike, blocksize);
            PyDrop::release_ref(cls, py);
            match ret {
                Ok(obj) => {
                    let p = obj.as_object().as_ptr();
                    ffi::Py_INCREF(p);
                    p
                }
                Err(_) => ptr::null_mut(),
            }
        }
        Some(wrap_newfunc)
    },
    tp_iter: {
        unsafe extern "C" fn wrap_unary(slf: *mut ffi::PyObject) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            let slf = PyObject::from_borrowed_ptr(py, slf).unchecked_cast_into::<FileWrapper>();
            let ret = slf.__iter__(py);
            PyDrop::release_ref(slf, py);
            match ret {
                Ok(obj) => {
                    let p = obj.as_object().as_ptr();
                    ffi::Py_INCREF(p);
                    p
                }
                Err(_) => ptr::null_mut(),
            }
        }
        Some(wrap_unary)
    },
    tp_iternext: {
        unsafe extern "C" fn wrap_unary(slf: *mut ffi::PyObject) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            let slf = PyObject::from_borrowed_ptr(py, slf).unchecked_cast_into::<FileWrapper>();
            let ret = slf.__next__(py);
            PyDrop::release_ref(slf, py);
            match ret {
                Ok(obj) => match obj {
                    Some(val) => val.steal_ptr(),
                    None => unsafe {
                        ffi::PyErr_SetNone(ffi::PyExc_StopIteration);
                        ptr::null_mut()
                    },
                },
                Err(_) => ptr::null_mut(),
            }
        }
        Some(wrap_unary)
    },
    tp_dealloc: Some(py_class::tp_dealloc_callback::<FileWrapper>),
    tp_flags: py_class::TPFLAGS_DEFAULT,
    tp_traverse: None,
    ..PyTypeObject_INIT
};
static mut INIT_ACTIVE: bool = false;

impl PythonObjectWithTypeObject for FileWrapper {
    fn type_object(py: Python) -> PyType {
        <FileWrapper as py_class::PythonObjectFromPyClassMacro>::initialize(py, None)
            .expect("An error occurred while initializing class FileWrapper")
    }
}

impl py_class::PythonObjectFromPyClassMacro for FileWrapper {
    fn initialize(py: Python, module_name: Option<&str>) -> PyResult<PyType> {
        unsafe {
            if (TYPE_OBJECT.tp_flags & ffi::Py_TPFLAGS_READY) != 0 {
                return Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)));
            }
            if INIT_ACTIVE {
                {
                    panic!("Reentrancy detected: already initializing class FileWrapper",);
                }
            }
            INIT_ACTIVE = true;
            let res = init(py, module_name);
            INIT_ACTIVE = false;
            res
        }
    }
}
fn init(py: Python, module_name: Option<&str>) -> PyResult<PyType> {
    unsafe {
        TYPE_OBJECT.ob_base.ob_base.ob_type = addr_of_mut!(ffi::PyType_Type);
        TYPE_OBJECT.tp_name = py_class::build_tp_name(module_name, "FileWrapper");
        TYPE_OBJECT.tp_basicsize = <FileWrapper as py_class::BaseObject>::size() as ffi::Py_ssize_t;
        TYPE_OBJECT.tp_as_sequence = 0 as *mut ffi::PySequenceMethods;
        TYPE_OBJECT.tp_as_number = 0 as *mut ffi::PyNumberMethods;
        TYPE_OBJECT.tp_getset = 0 as *mut ffi::PyGetSetDef;
    }
    let dict = PyDict::new(py);
    let init = {
        unsafe extern "C" fn wrap_instance_method(
            slf: *mut ffi::PyObject,
            args: *mut ffi::PyObject,
            kwargs: *mut ffi::PyObject,
        ) -> *mut ffi::PyObject {
            let py = Python::assume_gil_acquired();
            let slf = PyObject::from_borrowed_ptr(py, slf).unchecked_cast_into::<FileWrapper>();
            let ret = slf.close(py);
            PyDrop::release_ref(slf, py);
            match ret {
                Ok(obj) => obj.as_ptr(),
                Err(_) => ptr::null_mut(),
            }
        }
        unsafe {
            static mut METHOD_DEF: ffi::PyMethodDef = ffi::PyMethodDef {
                ml_name: 0 as *const libc::c_char,
                ml_meth: ffi::PyMethodDefPointer {
                    PyCFunctionWithKeywords: wrap_instance_method,
                },
                ml_flags: ffi::METH_VARARGS | ffi::METH_KEYWORDS, // | 0,
                ml_doc: 0 as *const libc::c_char,
            };
            METHOD_DEF.ml_name = "close\u{0}".as_ptr() as *const _;
            METHOD_DEF.ml_doc = "\u{0}".as_ptr() as *const _;
            addr_of_mut!(METHOD_DEF)
        }
    };
    let descriptor = unsafe {
        let p = ffi::PyDescr_NewMethod(addr_of_mut!(TYPE_OBJECT), init);
        if p.is_null() {
            Err(PyErr::fetch(py))
        } else {
            Ok(PyObject::from_owned_ptr(py, p))
        }
    }?;
    dict.set_item(py, "close", descriptor)?;
    unsafe {
        if !TYPE_OBJECT.tp_dict.is_null() {
            panic!("assertion failed: TYPE_OBJECT.tp_dict.is_null()",)
        }
        TYPE_OBJECT.tp_dict = PythonObject::into_object(dict).steal_ptr();
    }
    unsafe {
        if ffi::PyType_Ready(addr_of_mut!(TYPE_OBJECT)) == 0 {
            Ok(PyType::from_type_ptr(py, addr_of_mut!(TYPE_OBJECT)))
        } else {
            Err(PyErr::fetch(py))
        }
    }
}

pub trait SendFile {
    // Put this in a trait for more flexibility.
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo>;
    fn send_file(&mut self, out: &mut dyn AsRawFd, py: Python) -> (bool, usize);
    fn update_content_length(&mut self, content_length: usize, py: Python);
    // XXX used only for testing
    #[allow(clippy::new_ret_no_self, dead_code)]
    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper>;
}

impl SendFile for FileWrapper {
    // public getter
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo> {
        self.sendfileinfo(py)
    }

    fn send_file(&mut self, out: &mut dyn AsRawFd, py: Python) -> (bool, usize) {
        with_released_gil(|_threadstate| self.sendfileinfo(py).borrow_mut().send_file(out))
    }

    fn update_content_length(&mut self, content_length: usize, py: Python) {
        self.sendfileinfo(py)
            .borrow_mut()
            .update_content_length(content_length as isize);
    }

    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper> {
        FileWrapper::create_instance(
            py,
            RefCell::new(py.None()),
            RefCell::new(SendFileInfo::new(fd, bs)),
        )
    }
}

#[cfg(test)]
mod tests {

    use cpython::{
        NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyErr, PyIterator, PyTuple, Python,
        PythonObject, ToPyObject, TypeError,
    };
    use std::io::{Read, Seek, Write};
    use std::net::{SocketAddr, TcpListener, TcpStream};
    use std::os::unix::io::{AsRawFd, RawFd};
    use std::sync::mpsc::channel;
    use std::thread;
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFile};

    #[test]
    fn test_no_fileno() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                if let Ok(fw) = fwany.clone_ref(py).cast_into::<FileWrapper>(py) {
                    assert_eq!(fw.sendfileinfo(py).borrow().fd, fd);
                    match PyIterator::from_object(py, fwany) {
                        Ok(mut fwiter) => {
                            for chunk in vec![b"Fo", b"o ", b"42"] {
                                match fwiter.next() {
                                    Some(got) => {
                                        assert_eq!(
                                            chunk,
                                            got.unwrap().extract::<PyBytes>(py).unwrap().data(py)
                                        );
                                    }
                                    None => {
                                        assert!(false);
                                    }
                                }
                            }
                        }
                        Err(_) => assert!(false),
                    }
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_no_read_method() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                match PyIterator::from_object(py, fwany) {
                    Ok(mut fw) => match fw.next() {
                        Some(pyresult) => match pyresult {
                            Ok(_) => assert!(false),
                            Err(_) => assert!(true),
                        },
                        None => {
                            assert!(true);
                        }
                    },
                    Err(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_bytes_not_convertible() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def read(self, blocksize):
        result = 'öäü'
        self.offset += blocksize
        return result

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                match PyIterator::from_object(py, fwany) {
                    Ok(mut fw) => match fw.next() {
                        None => {
                            assert!(true);
                        }
                        Some(_) => {
                            assert!(false);
                        }
                    },
                    Err(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_send_file() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o Wo\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 8);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"rld!\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 12);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"\n\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 13);
        // no content length + blocksize > number bytes written, next should yield some
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
        drop(f);
        // connection is closed now
        let (done, offset) = sfi.send_file(&mut connection);
        assert!(done);
        assert!(offset == 13);
    }

    #[test]
    fn test_send_file_updated_content_length() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        fw.update_content_length(5, py);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_send_file_content_length_lt_blocksize() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 7).unwrap();
        fw.update_content_length(5, py);
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        assert_eq!(sfi.blocksize, 5);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        sfi.send_file(&mut connection);
        let b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hello\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_file_wrapper_new_noint_bs_arg() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                match fwtype.call(py, PyTuple::new(py, &[filelike, py.None()]), None) {
                    Err(e) => {
                        assert!(py.get_type::<TypeError>() == e.get_type(py));
                        // clear error from Python
                        PyErr::fetch(py);
                    }
                    Ok(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }
    #[test]
    fn test_file_wrapper_new_no_args() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let fwtype = py.get_type::<FileWrapper>();
        match fwtype.call(py, PyTuple::new(py, &[]), None) {
            Err(e) => {
                assert!(py.get_type::<TypeError>() == e.get_type(py));
                // clear error from Python
                PyErr::fetch(py);
            }
            Ok(_) => assert!(false),
        }
    }

    #[test]
    fn test_file_wrapper_new_nargs_gt_2() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                match fwtype.call(
                    py,
                    PyTuple::new(
                        py,
                        &[
                            filelike,
                            bs.to_py_object(py).as_object().clone_ref(py),
                            py.None(),
                        ],
                    ),
                    None,
                ) {
                    Err(e) => {
                        assert!(py.get_type::<TypeError>() == e.get_type(py));
                        // clear error from Python
                        PyErr::fetch(py);
                    }
                    Ok(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_file_wrapper_new_kwargs() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let kwargs = PyDict::new(py);
                kwargs.set_item(py, "filelike", filelike).unwrap();
                kwargs
                    .set_item(
                        py,
                        "blocksize",
                        bs.to_py_object(py).as_object().clone_ref(py),
                    )
                    .unwrap();
                match fwtype.call(py, PyTuple::new(py, &[]), Some(&kwargs)) {
                    Ok(_) => assert!(false),
                    Err(_) => (),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }
}
