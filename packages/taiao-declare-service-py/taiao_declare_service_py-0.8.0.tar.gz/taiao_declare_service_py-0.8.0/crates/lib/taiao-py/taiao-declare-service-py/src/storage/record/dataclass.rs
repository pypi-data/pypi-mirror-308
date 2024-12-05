use pyo3::{Bound, PyAny, PyResult, PyTypeInfo};
use pyo3::exceptions::PyTypeError;
use pyo3::types::{PyAnyMethods, PyType};

/// Gets the fields of a dataclass-type. If [py_type] is not a dataclass-type,
/// returns Ok(None).
pub fn fields<'py>(py_type: &Bound<'py, PyType>) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py = py_type.py();
    let dataclasses = py.import_bound("dataclasses")?;
    let fields = dataclasses.getattr("fields")?;
    match fields.call1((py_type,)) {
        Ok(fields) => Ok(Some(fields)),
        Err(error) => if PyTypeError::is_type_of_bound(error.value_bound(py)) { // TypeError indicates py_type is not a data-class
            Ok(None)
        } else {
            Err(error)
        }
    }
}
