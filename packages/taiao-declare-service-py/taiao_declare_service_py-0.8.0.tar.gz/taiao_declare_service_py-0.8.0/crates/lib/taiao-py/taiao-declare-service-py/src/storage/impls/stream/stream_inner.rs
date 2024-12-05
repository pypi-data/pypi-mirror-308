use taiao_storage::impls::stream::{Stream as StreamRs};
use taiao_storage::record::schema::impls::avro::AvroSchema;
use tokio::sync::RwLock;
use crate::storage::record::{PythonSchemaInitialiser, PythonSchemaRecord};

pub(super) struct StreamInner {
    pub inner: RwLock<StreamRs<PythonSchemaRecord<AvroSchema>>>,
    pub schema_initialiser: PythonSchemaInitialiser
}
