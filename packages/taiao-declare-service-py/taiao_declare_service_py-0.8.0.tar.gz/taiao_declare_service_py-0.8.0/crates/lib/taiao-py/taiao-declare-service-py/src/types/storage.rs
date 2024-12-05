use std::str::FromStr;
use pyo3::{pyclass, pymethods};
use taiao_types::{Storage as StorageRs};
use crate::error::{TAIAOPyError, TAIAOPyResult};

/// The type of dataset the service will produce.
#[pyclass(eq, eq_int)]
#[derive(Eq, PartialEq, Copy, Clone)]
#[repr(u16)]
pub enum Storage {
    /// The service does not produce a dataset
    NoStorage, // None is a reserved keyword in Python
    /// An append-only linear dataset
    Stream
}

#[pymethods]
impl Storage {
    #[staticmethod]
    pub fn from_string(string: &str) -> TAIAOPyResult<Self> {
        Ok(StorageRs::from_str(string)?.into())
    }

    pub fn __str__(&self) -> String {
        StorageRs::from(*self).to_string()
    }
}

impl FromStr for Storage {
    type Err = TAIAOPyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::from_string(s)
    }
}

impl From<StorageRs> for Storage {
    fn from(value: StorageRs) -> Self {
        match value {
            StorageRs::None => Storage::NoStorage,
            StorageRs::Stream => Storage::Stream,
        }
    }
}

impl From<Storage> for StorageRs {
    fn from(value: Storage) -> Self {
        match value {
            Storage::NoStorage => StorageRs::None,
            Storage::Stream => StorageRs::Stream,
        }
    }
}
