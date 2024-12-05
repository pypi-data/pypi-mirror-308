pub mod result;

mod python_service;
pub use python_service::PythonService;

mod platform_context;
pub use platform_context::PlatformContext;


use pyo3::prelude::*;
use crate::util::add_package_submodule;

#[pymodule]
pub fn service_submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    add_package_submodule::<false, _>(m, "result", result::submodule)?;
    m.add_class::<PlatformContext>()?;
    Ok(())
}
