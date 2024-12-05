// Copyright (c) 2015 Daniel Grunwald
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this
// software and associated documentation files (the "Software"), to deal in the Software
// without restriction, including without limitation the rights to use, copy, modify, merge,
// publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
// to whom the Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all copies or
// substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
// FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

use std::ptr;
use std::result::Result;

use crate::conversion::ToPyObject;
use crate::ffi;
use crate::objects::{PyObject, PyType, SystemError, TypeError};
use crate::python::{
    PyClone, Python, PythonObject, PythonObjectDowncastError, PythonObjectWithTypeObject,
    ToPythonPointer,
};

/**
Defines a new exception type.

# Syntax
`py_exception!(module, MyError)`

* `module` is the name of the containing module.
* `MyError` is the name of the new exception type.

# Example
```
use cpython::{Python, PyDict, py_exception};

py_exception!(mymodule, CustomError);

fn main() {
    let gil = Python::acquire_gil();
    let py = gil.python();
    let ctx = PyDict::new(py);

    ctx.set_item(py, "CustomError", py.get_type::<CustomError>()).unwrap();

    py.run("assert str(CustomError) == \"<class 'mymodule.CustomError'>\"", None, Some(&ctx)).unwrap();
    py.run("assert CustomError('oops').args == ('oops',)", None, Some(&ctx)).unwrap();
}
```
*/
#[macro_export]
macro_rules! py_exception {
    ($module: ident, $name: ident, $base: ty) => {
        pub struct $name($crate::PyObject);

        $crate::pyobject_newtype!($name);

        impl $name {
            pub fn new<'p, T: $crate::ToPyObject>(
                py: $crate::Python<'p>,
                args: T,
            ) -> $crate::PyErr {
                $crate::PyErr::new::<$name, T>(py, args)
            }
        }

        impl $crate::PythonObjectWithCheckedDowncast for $name {
            #[inline]
            fn downcast_from<'p>(
                py: $crate::Python<'p>,
                obj: $crate::PyObject,
            ) -> Result<$name, $crate::PythonObjectDowncastError<'p>> {
                if <$name as $crate::PythonObjectWithTypeObject>::type_object(py)
                    .is_instance(py, &obj)
                {
                    Ok(unsafe { $crate::PythonObject::unchecked_downcast_from(obj) })
                } else {
                    Err($crate::PythonObjectDowncastError::new(
                        py,
                        stringify!($name),
                        <$name as $crate::PythonObjectWithTypeObject>::type_object(py),
                    ))
                }
            }

            #[inline]
            fn downcast_borrow_from<'a, 'p>(
                py: $crate::Python<'p>,
                obj: &'a $crate::PyObject,
            ) -> Result<&'a $name, $crate::PythonObjectDowncastError<'p>> {
                if <$name as $crate::PythonObjectWithTypeObject>::type_object(py)
                    .is_instance(py, obj)
                {
                    Ok(obj)
                } else {
                    Err($crate::PythonObjectDowncastError::new(
                        py,
                        stringify!($name),
                        <$name as $crate::PythonObjectWithTypeObject>::type_object(py),
                    ))
                }
            }
        }

        impl $crate::PythonObjectWithTypeObject for $name {
            #[inline]
            fn type_object(py: $crate::Python) -> $crate::PyType {
                unsafe {
                    static mut type_object: *mut PyTypeObject =
                        0 as *mut ffi::PyTypeObject;

                    if type_object.is_null() {
                        type_object = $crate::PyErr::new_type(
                            py,
                            concat!(stringify!($module), ".", stringify!($name)),
                            Some($crate::PythonObject::into_object(py.get_type::<$base>())),
                            None,
                        )
                        .as_type_ptr();
                    }

                    $crate::PyType::from_type_ptr(py, type_object)
                }
            }
        }
    };
    ($module: ident, $name: ident) => {
        $crate::py_exception!($module, $name, Exception);
    };
}

/// Represents a Python exception that was raised.
#[derive(Debug)]
pub struct PyErr {
    /// The type of the exception. This should be either a `PyClass` or a `PyType`.
    pub ptype: PyObject,
    /// The value of the exception.
    ///
    /// This can be either an instance of `ptype`,
    /// a tuple of arguments to be passed to `ptype`'s constructor,
    /// or a single argument to be passed to `ptype`'s constructor.
    /// Call `PyErr::instance()` to get the exception instance in all cases.
    pub pvalue: Option<PyObject>,
    /// The `PyTraceBack` object associated with the error.
    pub ptraceback: Option<PyObject>,
}

/// Represents the result of a Python call.
pub type PyResult<T> = Result<T, PyErr>;

impl PyErr {
    /// Creates a new PyErr of type `T`.
    ///
    /// `value` can be:
    ///  * `NoArgs`: the exception instance will be created using python `T()`
    ///  * a tuple: the exception instance will be created using python `T(*tuple)`
    ///  * any other value: the exception instance will be created using python `T(value)`
    ///
    /// Panics if `T` is not a python class derived from `BaseException`.
    ///
    /// Example:
    ///  `return Err(PyErr::new::<TypeError, _>(py, "Error message"));`
    pub fn new<T, V>(py: Python, value: V) -> PyErr
    where
        T: PythonObjectWithTypeObject,
        V: ToPyObject,
    {
        PyErr::new_helper(py, py.get_type::<T>(), value.to_py_object(py).into_object())
    }

    /// Gets whether an error is present in the Python interpreter's global state.
    #[inline]
    pub fn occurred(_: Python) -> bool {
        unsafe { !ffi::PyErr_Occurred().is_null() }
    }

    /// Retrieves the current error from the Python interpreter's global state.
    /// The error is cleared from the Python interpreter.
    /// If no error is set, returns a `SystemError`.
    pub fn fetch(py: Python) -> PyErr {
        let mut ptype: *mut ffi::PyObject = ptr::null_mut();
        let mut pvalue: *mut ffi::PyObject = ptr::null_mut();
        let mut ptraceback: *mut ffi::PyObject = ptr::null_mut();
        unsafe {
            #[allow(deprecated)]
            ffi::PyErr_Fetch(&mut ptype, &mut pvalue, &mut ptraceback);
            PyErr::new_from_ffi_tuple(py, ptype, pvalue, ptraceback)
        }
    }

    unsafe fn new_from_ffi_tuple(
        py: Python,
        ptype: *mut ffi::PyObject,
        pvalue: *mut ffi::PyObject,
        ptraceback: *mut ffi::PyObject,
    ) -> PyErr {
        // Note: must not panic to ensure all owned pointers get acquired correctly,
        // and because we mustn't panic in normalize().
        PyErr {
            ptype: if ptype.is_null() {
                py.get_type::<SystemError>().into_object()
            } else {
                PyObject::from_owned_ptr(py, ptype)
            },
            pvalue: PyObject::from_owned_ptr_opt(py, pvalue),
            ptraceback: PyObject::from_owned_ptr_opt(py, ptraceback),
        }
    }

    fn new_helper(_py: Python, ty: PyType, value: PyObject) -> PyErr {
        assert!(unsafe { ffi::PyExceptionClass_Check(ty.as_object().as_ptr()) } != 0);
        PyErr {
            ptype: ty.into_object(),
            pvalue: Some(value),
            ptraceback: None,
        }
    }

    /// Construct a new error, with the usual lazy initialization of Python exceptions.
    /// `exc` is the exception type; usually one of the standard exceptions like `py.get_type::<RuntimeError>()`.
    /// `value` is the exception instance, or a tuple of arguments to pass to the exception constructor.
    #[inline]
    pub fn new_lazy_init(exc: PyType, value: Option<PyObject>) -> PyErr {
        PyErr {
            ptype: exc.into_object(),
            pvalue: value,
            ptraceback: None,
        }
    }

    /// Print a standard traceback to sys.stderr.
    pub fn print_and_set_sys_last_vars(self, py: Python) {
        self.restore(py);
        unsafe { ffi::PyErr_PrintEx(1) }
    }

    /// Normalizes the error. This ensures that the exception value is an instance of the exception type.
    pub fn normalize(&mut self, py: Python) {
        // The normalization helper function involves temporarily moving out of the &mut self,
        // which requires some unsafe trickery:
        unsafe {
            std::ptr::write(self, std::ptr::read(self).into_normalized(py));
        }
        // This is safe as long as normalized() doesn't unwind due to a panic.
    }

    /// Helper function for normalizing the error by deconstructing and reconstructing the PyErr.
    /// Must not panic for safety in normalize()
    fn into_normalized(self, py: Python) -> PyErr {
        let PyErr {
            ptype,
            pvalue,
            ptraceback,
        } = self;
        let mut ptype = ptype.steal_ptr();
        let mut pvalue = pvalue.steal_ptr(py);
        let mut ptraceback = ptraceback.steal_ptr(py);
        unsafe {
            #[allow(deprecated)]
            ffi::PyErr_NormalizeException(&mut ptype, &mut pvalue, &mut ptraceback);
            PyErr::new_from_ffi_tuple(py, ptype, pvalue, ptraceback)
        }
    }

    /// Retrieves the exception type.
    pub fn get_type(&self, py: Python) -> PyType {
        match self.ptype.cast_as::<PyType>(py) {
            Ok(t) => t.clone_ref(py),
            Err(_) => py.None().get_type(py),
        }
    }

    /// Retrieves the exception instance for this error.
    /// This method takes `&mut self` because the error might need
    /// to be normalized in order to create the exception instance.
    pub fn instance(&mut self, py: Python) -> PyObject {
        self.normalize(py);
        match self.pvalue {
            Some(ref instance) => instance.clone_ref(py),
            None => py.None(),
        }
    }

    /// Writes the error back to the Python interpreter's global state.
    /// This is the opposite of `PyErr::fetch()`.
    #[inline]
    pub fn restore(self, py: Python) {
        let PyErr {
            ptype,
            pvalue,
            ptraceback,
        } = self;
        unsafe {
            #[allow(deprecated)]
            ffi::PyErr_Restore(
                ptype.steal_ptr(),
                pvalue.steal_ptr(py),
                ptraceback.steal_ptr(py),
            )
        }
    }
}

/// Converts `PythonObjectDowncastError` to Python `TypeError`.
impl<'p> std::convert::From<PythonObjectDowncastError<'p>> for PyErr {
    fn from(err: PythonObjectDowncastError<'p>) -> PyErr {
        let msg = format!(
            "Expected type that converts to {} but received {}",
            err.expected_type_name,
            err.received_type.name(err.py),
        )
        .to_py_object(err.py)
        .into_object();
        PyErr::new_lazy_init(err.py.get_type::<TypeError>(), Some(msg))
    }
}

/// Construct PyObject from the result of a Python FFI call that returns a new reference (owned pointer).
/// Returns `Err(PyErr)` if the pointer is `null`.
/// Unsafe because the pointer might be invalid.
#[inline]
pub unsafe fn result_from_owned_ptr(py: Python, p: *mut ffi::PyObject) -> PyResult<PyObject> {
    if p.is_null() {
        Err(PyErr::fetch(py))
    } else {
        Ok(PyObject::from_owned_ptr(py, p))
    }
}

fn panic_after_error(_py: Python) -> ! {
    unsafe {
        ffi::PyErr_Print();
    }
    panic!("Python API called failed");
}

pub unsafe fn result_cast_from_owned_ptr<T>(py: Python, p: *mut ffi::PyObject) -> PyResult<T>
where
    T: crate::python::PythonObjectWithCheckedDowncast,
{
    if p.is_null() {
        Err(PyErr::fetch(py))
    } else {
        Ok(PyObject::from_owned_ptr(py, p).cast_into(py)?)
    }
}

pub unsafe fn cast_from_owned_ptr_or_panic<T>(py: Python, p: *mut ffi::PyObject) -> T
where
    T: crate::python::PythonObjectWithCheckedDowncast,
{
    if p.is_null() {
        panic_after_error(py);
    } else {
        PyObject::from_owned_ptr(py, p).cast_into(py).unwrap()
    }
}

/// Returns Ok if the error code is not -1.
#[inline]
pub fn error_on_minusone(py: Python, result: libc::c_int) -> PyResult<()> {
    if result != -1 {
        Ok(())
    } else {
        Err(PyErr::fetch(py))
    }
}
