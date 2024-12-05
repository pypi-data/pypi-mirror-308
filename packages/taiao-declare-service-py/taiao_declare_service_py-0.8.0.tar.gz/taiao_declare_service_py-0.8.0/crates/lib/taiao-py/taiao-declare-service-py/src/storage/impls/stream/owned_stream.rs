use std::ops::Deref;
use std::sync::Arc;
use pyo3::{Bound, PyAny, pyclass, PyErr, pymethods, PyResult, Python};
use pyo3::types::PyType;
use pyo3_async_runtimes::TaskLocals;
use taiao_storage::impls::stream::{OwnedStream as OwnedStreamRs};
use taiao_storage::record::schema::impls::avro::{AvroSchema, AvroValue};
use tokio::sync::RwLock;
use crate::error::TAIAOPyError;
use crate::storage::impls::stream::do_async::{do_async, do_async_pyerr};
use crate::storage::impls::stream::owned_stream_inner::OwnedStreamInner;
use crate::storage::record::{PythonRecord, PythonSchemaInitialiser, PythonSchemaRecord};
use crate::types::Storage;

#[pyclass(frozen)]
pub struct OwnedStream {
    inner: Arc<OwnedStreamInner>,
    locals: TaskLocals
}

impl OwnedStream {
    pub(crate) fn new(
        inner: OwnedStreamRs<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>>, 
        locals: TaskLocals,
        state_schema_initialiser: PythonSchemaInitialiser,
        output_schema_initialiser: PythonSchemaInitialiser
    ) -> Self {
        Self {
            inner: Arc::new(
                OwnedStreamInner {
                    inner: RwLock::new(inner),
                    state_schema_initialiser,
                    output_schema_initialiser
                }
            ),
            locals
        }
    }
    
    pub(crate) fn state_schema(&self) -> &PythonSchemaInitialiser {
        &self.inner.state_schema_initialiser
    }
}

#[pymethods]
impl OwnedStream {
    #[staticmethod]
    fn storage_type() -> Storage {
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

    pub fn get<'py>(&'py self, py: Python<'py>, index: u64) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async_pyerr(
            &self.locals,
            py,
            async move {
                let OwnedStreamInner {
                    inner,
                    output_schema_initialiser,
                    ..
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
                            output_schema_initialiser
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
                let OwnedStreamInner {
                    inner,
                    output_schema_initialiser,
                    ..
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
                            output_schema_initialiser
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

    pub fn push<'py>(
        &'py self,
        py: Python<'py>,
        state: PythonRecord,
        output: PythonRecord
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        do_async(
            &self.locals,
            py,
            async move {
                let state = PythonSchemaRecord(AvroValue::from(state));
                let output = PythonSchemaRecord(AvroValue::from(output));
                inner.inner.write().await
                    .push(&state, &output).await 
            }
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