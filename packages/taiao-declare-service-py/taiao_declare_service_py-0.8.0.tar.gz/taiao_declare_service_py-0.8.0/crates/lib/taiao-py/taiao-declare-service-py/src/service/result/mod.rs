mod service_completion;
pub use service_completion::ServiceCompletion;

use pyo3::prelude::*;

/// Module containing the [ServiceCompletion] type.
#[pymodule]
pub fn submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ServiceCompletion>()?;
    Ok(())
}
