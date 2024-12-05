use std::str::FromStr;
use pyo3::prelude::*;
use taiao_types::{Privacy as PrivacyRs};
use crate::error::{TAIAOPyError, TAIAOPyResult};

/// How visible the service's dataset should be to external requesters.
#[pyclass(eq, eq_int)]
#[derive(Copy, Clone, PartialEq)]
pub enum Privacy {
    /// Anyone can read the service's dataset
    Public,
    /// Services of other projects of the same client can read the service's dataset
    Client,
    /// Services of the same project can read the service's dataset
    Project
}

#[pymethods]
impl Privacy {
    #[staticmethod]
    pub fn from_string(string: &str) -> TAIAOPyResult<Self> {
        Ok(PrivacyRs::from_str(string)?.into())
    }

    pub fn __str__(&self) -> String {
        PrivacyRs::from(*self).to_string()
    }
}

impl FromStr for Privacy {
    type Err = TAIAOPyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::from_string(s)
    }
}

impl From<PrivacyRs> for Privacy {
    fn from(value: PrivacyRs) -> Self {
        match value {
            PrivacyRs::Public => Privacy::Public,
            PrivacyRs::Client => Privacy::Client,
            PrivacyRs::Project => Privacy::Project,
        }
    }
}

impl From<Privacy> for PrivacyRs {
    fn from(value: Privacy) -> Self {
        match value {
            Privacy::Public => PrivacyRs::Public,
            Privacy::Client => PrivacyRs::Client,
            Privacy::Project => PrivacyRs::Project,
        }
    }
}

