use std::future::Future;
use pyo3::{Bound, IntoPy, Py, PyAny, pyclass, pymethods, PyObject, PyResult, Python};
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::PyAnyMethods;
use pyo3_async_runtimes::{TaskLocals};

/// [pyo3_async_runtimes::tokio::future_into_py_with_locals] immediately runs the given future,
/// this class only dispatches the future once it has been awaited
#[pyclass]
pub struct PythonFuture {
    future_and_locals: Option<(
        Box<dyn Future<Output=PyResult<PyObject>> + Send + 'static>,
        TaskLocals
    )>
}

impl PythonFuture {
    pub fn new<
        T: IntoPy<PyObject>,
        F: Future<Output=PyResult<T>> + Send + 'static
    >(
        future: F,
        locals: TaskLocals
    ) -> Self {
        let future = async move {
            let result = future.await?;
            Python::with_gil(|py| {
                Ok(result.into_py(py))
            })
        };
        Self {
            future_and_locals: Some((Box::new(future), locals))
        }
    }
    
    pub fn into_bound(self, py: Python<'_>) -> PyResult<Bound<'_, PyAny>> {
        let in_python = Py::new(py, self)?;
        Ok(in_python.into_bound(py).into_any())
    }
}

#[pymethods]
impl PythonFuture {
    pub fn __await__<'py>(&mut self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let (future, locals) = match self.future_and_locals.take() {
            Some(future_and_locals) => future_and_locals,
            None => return Err(PyRuntimeError::new_err("already awaited"))
        };
        
        let coroutine = pyo3_async_runtimes::tokio::future_into_py_with_locals(py, locals, Box::into_pin(future))?;
        
        let object = coroutine.getattr("__await__")?.call0()?;
        
        Ok(object)
    }
}
