mod taiao_py_error;
pub use taiao_py_error::TAIAOPyError;

mod taiao_py_result;
pub use taiao_py_result::TAIAOPyResult;

use pyo3::prelude::*;

/// Module for working with TAIAO errors in Python.
#[pymodule]
pub fn error_submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TAIAOPyError>()?;
    Ok(())
}
