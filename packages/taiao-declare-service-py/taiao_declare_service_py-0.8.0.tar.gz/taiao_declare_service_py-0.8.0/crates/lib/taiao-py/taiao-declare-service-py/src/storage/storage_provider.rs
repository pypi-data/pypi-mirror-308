use std::ops::DerefMut;
use std::sync::Arc;
use pyo3::{Bound, PyAny, pyclass, PyErr, pymethods, PyResult, Python};
use pyo3_async_runtimes::TaskLocals;
use taiao_storage::provider::TypedStorageProvider;
use taiao_storage::provider::dynamic::DynamicStorageProvider;
use taiao_storage::record::schema::impls::avro::AvroSchema;
use tokio::sync::RwLock;
use crate::error::TAIAOPyError;
use crate::storage::impls::stream::{Stream, OwnedStream};
use crate::storage::record::{PythonSchema, PythonSchemaRecord};
use crate::util::PythonFuture;

#[pyclass]
pub struct StorageProvider {
    inner: Arc<RwLock<DynamicStorageProvider>>,
    locals: TaskLocals
}

impl StorageProvider {
    pub fn from_dynamic(
        provider: DynamicStorageProvider,
        locals: TaskLocals
    ) -> Self {
        Self {
            inner: Arc::new(RwLock::new(provider)),
            locals
        }
    }
}

#[pymethods]
impl StorageProvider {
    pub fn try_provide_stream<'py>(
        &mut self,
        py: Python<'py>,
        schema: PythonSchema
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        let locals = self.locals.clone_ref(py);
        let PythonSchema {
            initialiser,
            avro_schema
        } = schema;
        
        let future = async move {
            let mut provider = inner.write().await;
            match TypedStorageProvider::try_provide_stream::<PythonSchemaRecord<AvroSchema>>(provider.deref_mut(), avro_schema).await {
                Ok(Some(stream)) => Ok(Some(Stream::new(stream, locals, initialiser))),
                Ok(None) => Ok(None),
                Err(error) => Err(PyErr::from(TAIAOPyError::from(error)))
            }
        };
        
        PythonFuture::new(future, self.locals.clone_ref(py)).into_bound(py)
    }
    
    pub fn try_provide_owned_stream<'py>(
        &mut self,
        py: Python<'py>,
        state_schema: PythonSchema,
        output_schema: PythonSchema
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        let locals = self.locals.clone_ref(py);
        let PythonSchema {
            initialiser: state_initialiser,
            avro_schema: state_avro_schema
        } = state_schema;
        let PythonSchema {
            initialiser: output_initialiser,
            avro_schema: output_avro_schema
        } = output_schema;
        
        
        let future = async move {
            let mut provider = inner.write().await;
            match TypedStorageProvider::try_provide_owned_stream::<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>>(provider.deref_mut(), state_avro_schema, output_avro_schema).await {
                Ok(Some(stream)) => Ok(Some(OwnedStream::new(stream, locals, state_initialiser, output_initialiser))),
                Ok(None) => Ok(None),
                Err(error) => Err(PyErr::from(TAIAOPyError::from(error)))
            }
        };

        PythonFuture::new(future, self.locals.clone_ref(py)).into_bound(py)
    }
}