use std::ops::Deref;
use std::sync::Arc;
use pyo3::{Bound, PyAny, pyclass, PyErr, pymethods, PyResult, Python};
use pyo3::types::PyType;
use pyo3_async_runtimes::TaskLocals;
use taiao_storage::impls::stream::{Stream as StreamRs};
use taiao_storage::record::schema::impls::avro::AvroSchema;
use tokio::sync::RwLock;
use crate::error::TAIAOPyError;
use crate::storage::impls::stream::do_async::{do_async, do_async_pyerr};
use crate::storage::impls::stream::stream_inner::StreamInner;
use crate::storage::record::{PythonRecord, PythonSchemaInitialiser, PythonSchemaRecord};
use crate::types::Storage;

#[pyclass(frozen)]
pub struct Stream {
    inner: Arc<StreamInner>,
    locals: TaskLocals
}

impl Stream {
    pub(crate) fn new(
        inner: StreamRs<PythonSchemaRecord<AvroSchema>>,
        locals: TaskLocals,
        schema_initialiser: PythonSchemaInitialiser
    ) -> Self {
        Self {
            inner: Arc::new(
                StreamInner {
                    inner: RwLock::new(inner),
                    schema_initialiser
                }
            ),
            locals
        }
    }
}

#[pymethods]
impl Stream {
    #[staticmethod]
    pub fn storage_type() -> Storage {
        Storage::Stream
    }
    
    pub fn index<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async(
            &self.locals,
            py,
            async move { inner.inner.read().await.index().await }
        )
    }

    pub fn len<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async(
            &self.locals,
            py,
            async move { inner.inner.read().await.len().await }
        )
    }

    /// Gets the stream element at the given index.
    #[pyo3(text_signature="(index: int)")]
    pub fn get<'py>(&'py self, py: Python<'py>, index: u64) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async_pyerr(
            &self.locals,
            py,
            async move {
                let StreamInner {
                    inner,
                    schema_initialiser
                } = inner.deref();

                let result = inner.write().await
                    .get(index).await
                    .map_err(|error| PyErr::from(TAIAOPyError::from(error)))?;

                let value = match result {
                    Some(PythonSchemaRecord(value)) => value,
                    None => return Ok(None)
                };

                Ok(
                    Some(
                        PythonRecord::try_from_value(
                            value.into_inner(),
                            schema_initialiser
                        )?
                    )
                )
            }
        )
    }

    pub fn next<'py>(&'py self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async_pyerr(
            &self.locals,
            py,
            async move {
                let StreamInner {
                    inner,
                    schema_initialiser
                } = inner.deref();
                
                let result = inner.write().await
                    .next().await
                    .map_err(|error| PyErr::from(TAIAOPyError::from(error)))?;

                let value = match result {
                    Some(PythonSchemaRecord(value)) => value,
                    None => return Ok(None)
                };

                Ok(
                    Some(
                        PythonRecord::try_from_value(
                            value.into_inner(),
                            schema_initialiser
                        )?
                    )
                )
            }
        )
    }

    pub fn seek<'py>(&'py self, py: Python<'py>, index: u64) -> PyResult<Bound<'py, PyAny>>  {
        let inner = self.inner.clone();
        do_async(
            &self.locals,
            py,
            async move { inner.inner.write().await.seek(index).await }
        )
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