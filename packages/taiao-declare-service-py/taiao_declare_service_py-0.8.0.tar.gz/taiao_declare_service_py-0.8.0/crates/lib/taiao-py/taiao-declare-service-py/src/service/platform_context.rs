use std::sync::{Arc};
use pyo3::{Bound, PyAny, pyclass, PyErr, pymethods, PyResult, Python};
use pyo3_async_runtimes::TaskLocals;
use taiao_service::{DynPlatformContext, PlatformContext as PlatformContextRsTrait};
use tokio::sync::{Mutex};
use crate::error::TAIAOPyError;
use crate::storage::StorageProvider;
use crate::types::FullyQualifiedName;
use crate::util::{PythonFuture};

#[pyclass]
pub struct PlatformContext {
    inner: Arc<Mutex<DynPlatformContext>>,
    locals: TaskLocals
}

impl PlatformContext {
    pub(crate) fn new<P: PlatformContextRsTrait>(
        inner: P,
        locals: TaskLocals
    ) -> Self {
        Self {
            inner: Arc::new(Mutex::new(DynPlatformContext::new(inner))),
            locals
        }
    }
}

#[pymethods]
impl PlatformContext {
    pub fn get_storage_provider<'py>(
        &self,
        py: Python<'py>,
        service: FullyQualifiedName
    ) -> PyResult<Bound<'py, PyAny>> {
        let context = self.inner.clone();
        let locals = self.locals.clone_ref(py);
        let future = async move {
            match context.lock().await.get_storage_provider(service.into()).await {
                Ok(provider) => Ok(StorageProvider::from_dynamic(provider, locals)),
                Err(error) => Err(PyErr::from(TAIAOPyError::from(error)))
            } 
        };
        PythonFuture::new(future, self.locals.clone_ref(py)).into_bound(py)
    }
}

