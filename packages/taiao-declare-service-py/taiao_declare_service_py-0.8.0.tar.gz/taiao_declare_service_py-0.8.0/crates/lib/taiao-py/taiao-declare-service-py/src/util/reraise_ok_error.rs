use pyo3::exceptions::PyBaseException;
use pyo3::{Bound, PyAny};
use pyo3::types::PyAnyMethods;

pub fn reraise_ok_error<
    T,
    F: FnOnce(&T) -> &Bound<PyAny>
>(
    maybe_error: T,
    as_any: F
) -> Result<T, T> {
    let any = as_any(&maybe_error);
    match any {
        error if error.is_instance_of::<PyBaseException>() => Err(maybe_error),
        _ => Ok(maybe_error),
    }
}
