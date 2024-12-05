use std::any::{type_name, TypeId};
use std::fmt::{Display, Formatter};
use pyo3::{pyclass, PyErr, pymethods};
use pyo3::exceptions::{PyBaseException};

use taiao_error::{DynTAIAOError, DynTAIAOErrorSync, TAIAOError};

/// Representation of TAIAO errors in Python.
#[pyclass(extends=PyBaseException, module="taiao_error_py")]
#[derive(Debug)]
pub struct TAIAOPyError {
    /// The error's message content
    #[pyo3(get)]
    message: String,
    /// The type-name of the source Rust error, or None if unknown
    #[pyo3(get)]
    error_type: Option<String>
}

#[pymethods]
impl TAIAOPyError {
    /// Creates a new error.
    /// 
    /// * `message`: The error's message content
    /// * `error_type`: The type-name of the source Rust error, or None if unknown
    #[new]
    #[pyo3(signature = (message, error_type=None))]
    pub fn new(
        message: String,
        error_type: Option<String>
    ) -> Self {
        Self {
            message,
            error_type
        }
    }
    
    pub fn __str__(&self) -> String {
        self.to_string()
    }
}

impl Display for TAIAOPyError {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match &self.error_type {
            None => f.write_str(&self.message),
            Some(error_type) => f.write_fmt(format_args!("{}: {}", error_type, self.message))
        }
    }
}

impl<E: TAIAOError> From<E> for TAIAOPyError {
    fn from(value: E) -> Self {
        let error_type_id = TypeId::of::<E>();

        let error_type = if error_type_id == TypeId::of::<DynTAIAOError>() || error_type_id == TypeId::of::<DynTAIAOErrorSync>() {
            None
        } else {
            Some(type_name::<E>().to_owned())
        };

        Self {
            message: value.to_string(),
            error_type
        }
    }
}

impl From<TAIAOPyError> for PyErr {
    fn from(value: TAIAOPyError) -> Self {
        PyErr::new::<TAIAOPyError, _>((value.message, value.error_type))
    }
}
