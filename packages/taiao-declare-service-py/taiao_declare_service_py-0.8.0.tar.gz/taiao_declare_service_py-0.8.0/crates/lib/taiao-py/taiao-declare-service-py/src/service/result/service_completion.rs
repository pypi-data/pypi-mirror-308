use pyo3::{pyclass, pymethods};
use taiao_service_result::{ServiceCompletion as ServiceCompletionRs};

/// The ways a TAIAO service process can terminate successfully.
#[pyclass(eq, eq_int, module="taiao_service_result_py")]
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum ServiceCompletion {
    /// Completed all available work for now, but may have more to do in future
    FinishedForNow,
    /// Completed all available work, and no more incoming
    Finished
}

#[pymethods]
impl ServiceCompletion {
    /// Gets the numerical exit-code which corresponds to the way the service completed.
    pub fn exit_code(&self) -> u8 {
        match ServiceCompletionRs::from(*self) {
            ServiceCompletionRs::FinishedForNow => ServiceCompletionRs::FINISHED_FOR_NOW_EXIT_CODE,
            ServiceCompletionRs::Finished => ServiceCompletionRs::FINISHED_EXIT_CODE
        }
    }
}

impl From<ServiceCompletion> for ServiceCompletionRs {
    fn from(value: ServiceCompletion) -> Self {
        match value {
            ServiceCompletion::FinishedForNow => ServiceCompletionRs::FinishedForNow,
            ServiceCompletion::Finished => ServiceCompletionRs::Finished,
        }
    }
}

impl From<ServiceCompletionRs> for ServiceCompletion {
    fn from(value: ServiceCompletionRs) -> Self {
        match value {
            ServiceCompletionRs::FinishedForNow => ServiceCompletion::FinishedForNow,
            ServiceCompletionRs::Finished => ServiceCompletion::Finished,
        }
    }
}