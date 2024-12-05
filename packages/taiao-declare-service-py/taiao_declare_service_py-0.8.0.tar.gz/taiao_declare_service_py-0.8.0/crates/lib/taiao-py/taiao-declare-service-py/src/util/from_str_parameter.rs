use std::str::FromStr;
use pyo3::{Bound, FromPyObject, PyAny, PyErr, PyResult};
use pyo3::conversion::FromPyObjectBound;
use crate::error::TAIAOPyError;

pub struct FromStrParameter<const ONLY: bool, T> {
    pub value: T
}

impl<const ONLY: bool, T> From<T> for FromStrParameter<ONLY, T> {
    fn from(value: T) -> Self {
        Self { value }
    }
}

impl<
    'source,
    T: FromStr + FromPyObject<'source>
> FromPyObject<'source> for FromStrParameter<false, T>
    where PyErr: From<<T as FromStr>::Err>
{
    fn extract_bound(ob: &Bound<'source, PyAny>) -> PyResult<Self> {
        let t_error= match T::extract_bound(ob) {
            Ok(value) => return Ok(value.into()),
            Err(error) => error
        };

        let string = <&str as FromPyObjectBound>::from_py_object_bound(ob.as_borrowed()).map_err(|_| t_error)?;

        let value = T::from_str(string)?;

        Ok(value.into())
    }
}

impl<
    'source,
    T: FromStr
> FromPyObject<'source> for FromStrParameter<true, T>
    where TAIAOPyError: From<<T as FromStr>::Err>
{
    fn extract_bound(ob: &Bound<'source, PyAny>) -> PyResult<Self> {
        let string = <&str as FromPyObjectBound>::from_py_object_bound(ob.as_borrowed())?;

        let value = T::from_str(string).map_err(TAIAOPyError::from)?;

        Ok(value.into())
    }
}
