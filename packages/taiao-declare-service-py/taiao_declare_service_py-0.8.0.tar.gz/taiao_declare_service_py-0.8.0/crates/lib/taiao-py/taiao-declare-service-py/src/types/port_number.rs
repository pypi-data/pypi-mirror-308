use std::num::NonZeroU16;
use std::str::FromStr;
use pyo3::{Bound, FromPyObject, pyclass, pymethods, PyResult};
use pyo3::exceptions::PyValueError;
use pyo3::types::PyLong;
use taiao_types::{PortNumber as PortNumberRs};
use crate::error::{TAIAOPyError, TAIAOPyResult};

/// The port number a service should listen on.
#[pyclass]
#[derive(Copy, Clone)]
pub struct PortNumber {
    inner: PortNumberRs
}

#[pymethods]
impl PortNumber {
    #[new]
    pub fn new(value: &Bound<PyLong>) -> PyResult<Self> {
        NonZeroU16::extract_bound(value)
            .map(PortNumberRs::from_non_zero_u16)
            .map(From::from)
            .or_else(
                |_| Err(PyValueError::new_err(format!("expected number in [1:{}], received {}", NonZeroU16::MAX, value.to_string())))
            )
    }

    #[staticmethod]
    pub fn none() -> Self {
        PortNumberRs::none().into()
    }

    #[staticmethod]
    pub fn from_string(string: &str) -> TAIAOPyResult<Self> {
        Ok(PortNumberRs::from_str(string)?.into())
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

impl FromStr for PortNumber {
    type Err = TAIAOPyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::from_string(s)
    }
}

impl From<PortNumberRs> for PortNumber {
    fn from(value: PortNumberRs) -> Self {
        Self { inner: value }
    }
}

impl From<PortNumber> for PortNumberRs {
    fn from(value: PortNumber) -> Self {
        value.inner
    }
}
