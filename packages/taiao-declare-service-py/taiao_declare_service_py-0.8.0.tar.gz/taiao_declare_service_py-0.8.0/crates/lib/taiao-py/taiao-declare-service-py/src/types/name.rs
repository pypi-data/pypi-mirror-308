use std::str::FromStr;
use pyo3::{pyclass, pymethods};
use taiao_types::{Name as NameRs};
use crate::error::{TAIAOPyError, TAIAOPyResult};

/// A name for a client, project or service. Must be between 1 and [MAX_LENGTH](Name::MAX_LENGTH)
/// characters, consisting of a-z, 0-9.
#[pyclass(module = "taiao_types_py")]
#[derive(Copy, Clone, Ord, PartialOrd, Eq, PartialEq)]
pub struct Name {
    inner: NameRs
}

#[pymethods]
impl Name {
    /// The maximum length of a name
    #[classattr]
    const MAX_LENGTH: usize = NameRs::MAX_LENGTH;
    
    /// Checks if `string` is a valid [name](Name).
    #[staticmethod]
    pub fn validate_string(string: &str) -> TAIAOPyResult<()> {
        NameRs::validate_string(string)?;
        Ok(())
    }

    /// Creates a new [Name] from a `string`, returning an error if the `string` is not [valid](Self::validate_string).
    #[new]
    pub fn new(string: &str) -> TAIAOPyResult<Self> {
        Ok(NameRs::from_str(string)?.into())
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

impl Name {
    pub fn into_rust(self) -> NameRs {
        self.inner
    }
}

impl FromStr for Name {
    type Err = TAIAOPyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::new(s)
    }
}

impl From<NameRs> for Name {
    fn from(value: NameRs) -> Self {
        Self { inner: value }
    }
}

impl From<Name> for NameRs {
    fn from(value: Name) -> Self {
        value.inner
    }
}

macro_rules! typed_name {
    ($type_name:ident) => {
        #[pyclass]
        #[derive(Copy, Clone, Ord, PartialOrd, Eq, PartialEq)]
        pub struct $type_name {
            inner: ::taiao_types::$type_name
        }

        #[pymethods]
        impl $type_name {
            #[new]
            pub fn new(string: &str) -> TAIAOPyResult<Self> {
                Ok(::taiao_types::$type_name::try_from(string)?.into())
            }

            pub fn __str__(&self) -> String {
                self.inner.to_string()
            }
        }
        
        impl $type_name {
            pub fn into_rust(self) -> ::taiao_types::$type_name {
                self.inner
            }
        }

        impl FromStr for $type_name {
            type Err = TAIAOPyError;

            fn from_str(s: &str) -> Result<Self, Self::Err> {
                Self::new(s)
            }
        }

        impl From<::taiao_types::$type_name> for $type_name {
            fn from(value: ::taiao_types::$type_name) -> Self {
                Self { inner: value }
            }
        }

        impl From<$type_name> for ::taiao_types::$type_name {
            fn from(value: $type_name) -> Self {
                value.inner
            }
        }
    };
}

typed_name!(ClientName);
typed_name!(ProjectName);
typed_name!(ServiceName);
