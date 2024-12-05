use std::future::Future;
use pyo3::{Bound, IntoPy, PyAny, PyErr, PyObject, PyResult, Python};
use pyo3::exceptions::PyBaseException;
use pyo3::types::PyAnyMethods;
use pyo3_async_runtimes::TaskLocals;
use crate::error::TAIAOPyError;
use crate::util::{PythonFuture};


pub(super) fn do_async<
    'py,
    T: IntoPy<PyObject> + Send + Sync + 'static,
    E: Into<TAIAOPyError>,
    F: Future<Output=Result<T, E>> + Send + 'static
>(
    locals: &'py TaskLocals,
    py: Python<'py>,
    future: F,
) -> PyResult<Bound<'py, PyAny>> {
    do_async_pyerr(
        locals,
        py,
        async move {
            future.await
                .map_err(|error| PyErr::from(<E as Into<TAIAOPyError>>::into(error)))
        }
    )
}

pub(super) fn do_async_pyerr<
    'py,
    T: IntoPy<PyObject> + Send + Sync + 'static,
    F: Future<Output=Result<T, PyErr>> + Send + 'static
>(
    locals: &'py TaskLocals,
    py: Python<'py>,
    future: F,
) -> PyResult<Bound<'py, PyAny>> {
    PythonFuture::new(
        async move {
            let result = future.await?;
            
            Python::with_gil(|py| {
                let any = result.into_py(py).into_bound(py);
                
                if any.is_instance_of::<PyBaseException>() {
                    Err(PyErr::from_value_bound(any))
                } else {
                    Ok(any.unbind())
                }
            })
        },
        locals.clone_ref(py),
    ).into_bound(py)
}