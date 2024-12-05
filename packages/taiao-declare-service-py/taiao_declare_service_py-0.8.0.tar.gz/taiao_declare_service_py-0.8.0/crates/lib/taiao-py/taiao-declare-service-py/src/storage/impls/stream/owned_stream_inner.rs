use taiao_storage::impls::stream::{OwnedStream as OwnedStreamRs};
use taiao_storage::record::schema::impls::avro::AvroSchema;
use tokio::sync::RwLock;
use crate::storage::record::{PythonSchemaInitialiser, PythonSchemaRecord};

pub(super) struct OwnedStreamInner {
    pub inner: RwLock<OwnedStreamRs<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>>>,
    pub state_schema_initialiser: PythonSchemaInitialiser,
    pub output_schema_initialiser: PythonSchemaInitialiser,
}
