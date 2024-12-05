mod error;
mod service;
mod storage;
mod types;
mod util;
mod declare_service;
mod get_event_loop;
mod python_service_main;

use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn taiao_declare_service_py(m: &Bound<PyModule>) -> PyResult<()> {
    pub use util::add_package_submodule;
    add_package_submodule::<true, _>(m, "error", error::error_submodule)?;
    add_package_submodule::<true, _>(m, "service", service::service_submodule)?;
    add_package_submodule::<true, _>(m, "storage", storage::storage_submodule)?;
    add_package_submodule::<true, _>(m, "types", types::types_submodule)?;
    m.add_function(wrap_pyfunction!(declare_service::declare_service, m)?)?;
    Ok(())
}
