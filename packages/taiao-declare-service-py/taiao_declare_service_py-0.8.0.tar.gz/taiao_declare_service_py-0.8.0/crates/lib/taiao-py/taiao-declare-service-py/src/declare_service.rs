use std::panic::panic_any;
use std::sync::{Mutex, PoisonError};
use pyo3::{Bound, PyAny, pyfunction, PyResult};
use pyo3::exceptions::PySystemExit;
use taiao_service_result::ServiceCompletion;
use crate::get_event_loop::get_event_loop;
use crate::python_service_main::python_service_main;
use crate::storage::OwnedStorageType;
use crate::types::{ClientName, Periodicity, PortNumber, Privacy, ProjectName, ServiceName};
use crate::util::FromStrParameter;

type OrStringRepr<T> = FromStrParameter<false, T>;

/// Main entry point for a Python service.
#[pyfunction]
#[pyo3(text_signature = "(client: ClientName | str, project: ClientName | str, service: ClientName | str, storage: OwnedStorageType, body, privacy: Privacy, periodicity: Periodicity, listen: PortNumber | str)")]
pub fn declare_service(
    client: OrStringRepr<ClientName>,
    project: OrStringRepr<ProjectName>,
    service: OrStringRepr<ServiceName>,
    storage: &OwnedStorageType,
    body: Bound<PyAny>,
    privacy: Privacy,
    periodicity: Periodicity,
    listen: OrStringRepr<PortNumber>
) -> PyResult<()> {
    
    let event_loop = get_event_loop(body.py())?;
    
    let service_main = python_service_main(
        event_loop.clone(),
        client.value,
        project.value,
        service.value,
        storage,
        body,
        privacy,
        periodicity,
        listen.value
    )?;
    
    let async_main = move || async { 
        let handle = std::thread::spawn(service_main);
        match handle.join() {
            Ok(result) => Ok(result.map_err(Mutex::new)), // pyo3_asyncio::tokio::run has unnecessary Sync bound
            Err(error) => panic_any(error)
        }
    };

    let result = pyo3_async_runtimes::tokio::run_until_complete(event_loop, async_main())?;

    let exit = match result {
        Ok(completion) => PySystemExit::new_err(
            match completion {
                ServiceCompletion::Finished => ServiceCompletion::FINISHED_EXIT_CODE,
                ServiceCompletion::FinishedForNow => ServiceCompletion::FINISHED_FOR_NOW_EXIT_CODE
            }
        ),
        Err(error) => { 
            let error = error.into_inner().unwrap_or_else(PoisonError::into_inner);
            PySystemExit::new_err(error.to_string()) 
        }
    };
    
    Err(exit)
}