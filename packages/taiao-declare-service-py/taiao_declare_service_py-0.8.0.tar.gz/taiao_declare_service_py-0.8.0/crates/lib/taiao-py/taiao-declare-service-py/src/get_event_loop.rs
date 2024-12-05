use pyo3::{Bound, PyAny, PyResult, Python};
use pyo3::types::PyAnyMethods;

pub fn get_event_loop(py: Python) -> PyResult<Bound<PyAny>> {
    let asyncio = py.import_bound("asyncio")?;
    let get_event_loop = asyncio.getattr("get_event_loop")?;
    get_event_loop.call0()
}
