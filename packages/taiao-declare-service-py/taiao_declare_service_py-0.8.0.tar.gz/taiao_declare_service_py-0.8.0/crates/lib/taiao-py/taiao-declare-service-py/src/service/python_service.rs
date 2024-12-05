use pyo3::{Bound, PyAny, PyObject, PyResult, Python};
use pyo3::exceptions::PyTypeError;
use pyo3::types::PyAnyMethods;
use pyo3_async_runtimes::{into_future_with_locals, TaskLocals};
use taiao_service::{PlatformContext as PlatformContextRsTrait, Service};
use taiao_service_result::ServiceResult;
use taiao_storage::OwnedStorage;
use taiao_types::ServiceConfiguration;
use crate::service::PlatformContext;
use crate::service::result::ServiceCompletion;
use crate::storage::IntoOwnedPythonStorage;
use crate::types::{ServiceConfiguration as ServiceConfigurationPy};

pub struct PythonService<S: IntoOwnedPythonStorage> {
    callable: PyObject,
    locals: TaskLocals,
    storage_initialiser: S::StorageInitialiser
}

impl<S: IntoOwnedPythonStorage> PythonService<S> {
    pub fn new(callable: PyObject, locals: TaskLocals, storage_initialiser: S::StorageInitialiser) -> Self {
        Self {
            callable,
            locals,
            storage_initialiser
        }
    }
    
    fn is_awaitable(obj: &Bound<PyAny>) -> PyResult<bool> {
        let py = obj.py();
        let inspect = py.import_bound("inspect")?;
        let isawaitable = inspect.getattr("isawaitable")?;
        isawaitable.call1((obj,))?.extract::<bool>()
    }
}

macro_rules! tri {
    ($expression:expr) => {
        ($expression).map_err(taiao_error::TAIAOErrorExt::boxed_dyn)?
    };
}

impl<S: IntoOwnedPythonStorage> Service for PythonService<S> {
    type Storage = S;

    async fn main(
        self,
        configuration: ServiceConfiguration,
        storage: Self::Storage,
        latest_state: Option<<Self::Storage as OwnedStorage>::StateType>,
        platform_context: impl PlatformContextRsTrait
    ) -> ServiceResult {
        let future = tri!(
            Python::with_gil(|py| {
                let configuration = ServiceConfigurationPy::from(configuration);
                
                let storage = storage.into_python_storage(py, &self.locals, self.storage_initialiser);
                
                let latest_state = match latest_state {
                    Some(state) => Some(S::try_map_state(&storage, state)?),
                    None => None
                };
                
                let coroutine = self.callable.call_bound(
                    py,
                    (
                        configuration,
                        storage,
                        latest_state,
                        PlatformContext::new(platform_context, self.locals.clone_ref(py))
                    ),
                    None
                )?;
                
                let coroutine = coroutine.into_bound(py);
                
                if !Self::is_awaitable(&coroutine)? {
                    return Err(PyTypeError::new_err("service is not a coroutine (did you forget async def?)"))
                }
                
                Ok(into_future_with_locals(&self.locals, coroutine)?)
            })
        );
        
        let result = tri!(future.await);

        let completion = tri!(
            Python::with_gil(|py| {
                result.extract::<ServiceCompletion>(py)
            })
        );

        Ok(completion.into())
    }
}
