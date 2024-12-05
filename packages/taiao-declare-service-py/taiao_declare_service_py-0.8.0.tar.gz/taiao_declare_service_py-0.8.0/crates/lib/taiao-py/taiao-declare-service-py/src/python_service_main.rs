use std::ops::Deref;
use pyo3::{Bound, IntoPy, PyAny, PyResult};
use pyo3_async_runtimes::TaskLocals;
use taiao_declare_service_macro::reexport::taiao_error::DynTAIAOError;
use taiao_storage::impls::NoStorage;
use taiao_service_result::ServiceCompletion;
use taiao_storage::impls::stream::OwnedStream;
use taiao_storage::record::schema::impls::avro::AvroSchema;
use crate::service::PythonService;
use crate::storage::{OwnedStorageType, OwnedStorageTypeInner};
use crate::storage::record::{PythonSchema, PythonSchemaRecord};
use crate::types::{ClientName, Periodicity, PortNumber, Privacy, ProjectName, ServiceName};

#[inline]
pub fn python_service_main(
    event_loop: Bound<PyAny>,
    client: ClientName,
    project: ProjectName,
    service: ServiceName,
    storage: &OwnedStorageType,
    body: Bound<PyAny>,
    privacy: Privacy,
    periodicity: Periodicity,
    listen: PortNumber
) -> PyResult<impl FnOnce() -> Result<ServiceCompletion, DynTAIAOError>> {
    let py = body.py();

    let locals = TaskLocals::new(event_loop);
    
    let storage = storage.deref().map_ref(|schema| 
        schema.get().clone()
    );
    
    let body = body.into_py(py);

    let service_main = move || {
        let storage_type = storage.as_storage();
        match storage {
            OwnedStorageTypeInner::NoStorage => taiao_declare_service_macro::declare_service!(
                    @service_main_impl
                    client=client,
                    project=project,
                    service=service,
                    storage=storage_type,
                    body=PythonService::<NoStorage>::new(body, locals, ()),
                    privacy=privacy,
                    interval=periodicity,
                    listen=listen
                ),
            OwnedStorageTypeInner::Stream { state_schema, output_schema } => {
                let PythonSchema {
                    initialiser: state_initialiser,
                    avro_schema: state_avro_schema
                } = state_schema;

                let PythonSchema {
                    initialiser: output_initialiser,
                    avro_schema: output_avro_schema
                } = output_schema;
                
                taiao_declare_service_macro::declare_service!(
                    @service_main_impl
                    client=client,
                    project=project,
                    service=service,
                    storage=storage_type,
                    body=PythonService::<OwnedStream<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>>>::new(body, locals, (state_initialiser, output_initialiser)),
                    privacy=privacy,
                    interval=periodicity,
                    listen=listen,
                    storage-init=(state_avro_schema, output_avro_schema)
                )
            }
        }
    };
    
    Ok(service_main)
}