use std::ops::Deref;
use pyo3::{Bound, Py, PyAny, pyclass, pymethods, PyResult};
use pyo3::types::PyType;
use taiao_types::Storage;
use crate::storage::record::PythonSchema;

#[pyclass(frozen)]
#[derive(Clone, Debug)]
pub struct StorageType {
    inner: StorageTypeInner
}

#[pymethods]
impl StorageType {
    #[staticmethod]
    pub fn no_storage() -> Self {
        StorageTypeInner::NoStorage.into()
    }

    #[staticmethod]
    pub fn stream(output_schema: Py<PythonSchema>) -> PyResult<Self> {
        Ok(StorageTypeInner::Stream(output_schema).into())
    }

    #[classmethod]
    fn __class_getitem__<'cls, 'bound>(
        cls: &'cls Bound<'bound, PyType>,
        _types: &Bound<'_, PyAny>
    ) -> &'cls Bound<'bound, PyType> {
        // Dummy implementation to pretend that this class extends typing.Generic
        cls
    }
}

impl Deref for StorageType {
    type Target = StorageTypeInner;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl From<StorageTypeInner> for StorageType {
    fn from(value: StorageTypeInner) -> Self {
        Self { inner: value }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum StorageTypeInner<S = Py<PythonSchema>> {
    NoStorage,
    Stream(S)
}

impl<S> StorageTypeInner<S> {
    pub fn as_storage(&self) -> Storage {
        match self {
            StorageTypeInner::NoStorage => Storage::None,
            StorageTypeInner::Stream(_) => Storage::Stream
        }
    }

    #[inline]
    pub fn map<S2, F: Fn(S) -> S2>(self, f: F) -> StorageTypeInner<S2> {
        match self {
            StorageTypeInner::NoStorage => StorageTypeInner::NoStorage,
            StorageTypeInner::Stream(value) => StorageTypeInner::Stream(f(value))
        }
    }

    #[inline]
    pub fn map_ref<S2, F: Fn(&S) -> S2>(&self, f: F) -> StorageTypeInner<S2> {
        match self {
            StorageTypeInner::NoStorage => StorageTypeInner::NoStorage,
            StorageTypeInner::Stream(value) => StorageTypeInner::Stream(f(value))
        }
    }
}

impl From<StorageType> for StorageTypeInner {
    fn from(value: StorageType) -> Self {
        value.inner
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct OwnedStorageType {
    inner: OwnedStorageTypeInner
}

#[pymethods]
impl OwnedStorageType {
    #[staticmethod]
    pub fn no_storage() -> Self {
        OwnedStorageTypeInner::NoStorage.into()
    }

    #[staticmethod]
    pub fn stream(state_schema: Py<PythonSchema>, output_schema: Py<PythonSchema>) -> Self {
        OwnedStorageTypeInner::Stream {
            state_schema,
            output_schema 
        }.into()
    }

    #[classmethod]
    fn __class_getitem__<'cls, 'bound>(
        cls: &'cls Bound<'bound, PyType>,
        _types: &Bound<'_, PyAny>
    ) -> &'cls Bound<'bound, PyType> {
        // Dummy implementation to pretend that this class extends typing.Generic
        cls
    }
}

impl Deref for OwnedStorageType {
    type Target = OwnedStorageTypeInner;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl From<OwnedStorageTypeInner> for OwnedStorageType {
    fn from(value: OwnedStorageTypeInner) -> Self {
        Self { inner: value }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum OwnedStorageTypeInner<S = Py<PythonSchema>> {
    NoStorage,
    Stream {
        state_schema: S,
        output_schema: S
    }
}

impl<S> OwnedStorageTypeInner<S> {
    pub fn as_storage(&self) -> Storage {
        match self {
            OwnedStorageTypeInner::NoStorage => Storage::None,
            OwnedStorageTypeInner::Stream { .. } => Storage::Stream
        }
    }

    #[inline]
    pub fn map<S2, F: Fn(S) -> S2>(self, f: F) -> OwnedStorageTypeInner<S2> {
        match self {
            OwnedStorageTypeInner::NoStorage => OwnedStorageTypeInner::NoStorage,
            OwnedStorageTypeInner::Stream {
                state_schema,
                output_schema
            } => OwnedStorageTypeInner::Stream {
                state_schema: f(state_schema),
                output_schema: f(output_schema)
            }
        }
    }

    #[inline]
    pub fn map_ref<S2, F: Fn(&S) -> S2>(&self, f: F) -> OwnedStorageTypeInner<S2> {
        match self {
            OwnedStorageTypeInner::NoStorage => OwnedStorageTypeInner::NoStorage,
            OwnedStorageTypeInner::Stream {
                state_schema,
                output_schema
            } => OwnedStorageTypeInner::Stream {
                state_schema: f(state_schema),
                output_schema: f(output_schema)
            }
        }
    }
}

impl From<OwnedStorageType> for OwnedStorageTypeInner {
    fn from(value: OwnedStorageType) -> Self {
        value.inner
    }
}
