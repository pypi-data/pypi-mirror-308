use std::marker::PhantomData;
use std::str::FromStr;
use pyo3::{FromPyObject, PyAny, PyErr, PyNativeType, PyResult, PyTypeInfo};
use pyo3::types::PyString;

pub struct FromPrimitiveParameter<
    T,
    D
> {
    pub value: T,
    marker: PhantomData<fn(D)>
}

impl<T, D> From<T> for FromPrimitiveParameter<T, D> {
    fn from(value: T) -> Self {
        Self {
            value,
            marker: PhantomData
        }
    }
}

impl<
    'source,
    T,
    D
> FromPyObject<'source> for FromPrimitiveParameter<T, D>
    where T: FromPyObject<'source>
{
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        if let Ok(obj) = <T as FromPyObject<'source>>::extract(ob) {
            return Ok(obj.into())
        }


        todo!()
    }
}

pub trait TryFromPyNative<T: PyNativeType>: Sized {
    fn decode(value: &T) -> PyResult<Self>;
}

impl<T: FromStr> TryFromPyNative<PyString> for T
    where PyErr: From<<T as FromStr>::Err>
{
    fn decode(value: &PyString) -> PyResult<Self> {
        let string = value.to_str()?;

        Ok(T::from_str(string)?)
    }
}

pub trait TryDecode<T>: Sized {
    fn decode(value: &PyAny) -> PyResult<T>;
}

impl<
    T: TryFromPyNative<P>,
    P: PyNativeType + PyTypeInfo
> TryDecode<T> for P {
    fn decode(value: &PyAny) -> PyResult<T> {
        let as_P: &P = value.downcast()?;


    }
}

macro_rules! try_decode {
    ($value:expr => $t:ty) => {
        match <$t>::decode($value) {
            Ok(obj) => return Ok(obj),
            Err(error) => error
        }
    };
}

impl<
    T,
    A: TryDecode<T>,
    B: TryDecode<T>
> TryDecode<T> for (A, B) {
    fn decode(value: &PyAny) -> PyResult<T> {
        let A_error = try_decode!(value => A);
        
        let B_error = match B::decode(value) {
            Ok(obj) => return Ok(obj),
            Err(error) => error,
        };
        
        
    }
}

