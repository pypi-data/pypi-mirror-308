mod do_async;

mod owned_stream;
pub use owned_stream::OwnedStream;

mod owned_stream_inner;

mod stream;
pub use stream::Stream;

mod stream_inner;

use pyo3::prelude::*;

#[pymodule]
pub fn stream_submodule(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<Stream>()?;
    m.add_class::<OwnedStream>()?;
    Ok(())
}