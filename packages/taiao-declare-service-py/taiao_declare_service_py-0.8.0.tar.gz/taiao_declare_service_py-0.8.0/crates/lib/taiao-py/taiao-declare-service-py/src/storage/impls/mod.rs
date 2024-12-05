pub mod stream;

use pyo3::prelude::*;
use crate::util::add_package_submodule;

#[pymodule]
pub fn impls_submodule(m: &Bound<PyModule>) -> PyResult<()> {
    add_package_submodule::<false, _>(m, "stream", stream::stream_submodule)?;
    Ok(())
}
