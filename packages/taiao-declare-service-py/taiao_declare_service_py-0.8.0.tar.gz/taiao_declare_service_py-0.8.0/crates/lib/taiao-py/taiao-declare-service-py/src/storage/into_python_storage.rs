use pyo3::{IntoPy, PyErr, PyObject, Python};
use pyo3_async_runtimes::TaskLocals;
use taiao_storage::impls::{NeverRecord, NoStorage};
use taiao_storage::impls::stream::{Stream as StreamRs, OwnedStream as OwnedStreamRs};
use taiao_storage::{OwnedStorage, Storage};
use taiao_storage::record::schema::impls::avro::AvroSchema;
use crate::storage::impls::stream::{Stream, OwnedStream};
use crate::storage::record::{PythonRecord, PythonSchemaInitialiser, PythonSchemaRecord};


pub trait IntoPythonStorage: Storage {
    type PythonStorage: IntoPy<PyObject>;
    
    type StorageInitialiser: Send + 'static;

    fn into_python_storage(self, py: Python, locals: &TaskLocals, initialiser: Self::StorageInitialiser) -> Self::PythonStorage;
}

pub trait IntoOwnedPythonStorage: IntoPythonStorage + OwnedStorage {
    fn try_map_state(
        storage: &Self::PythonStorage,
        state: <Self as OwnedStorage>::StateType
    ) -> Result<PythonRecord, PyErr>;
}

impl IntoPythonStorage for NoStorage {
    type PythonStorage = ();
    
    type StorageInitialiser = ();

    fn into_python_storage(self, _py: Python, _locals: &TaskLocals, _initialiser: Self::StorageInitialiser) -> Self::PythonStorage {
        ()
    }
}

impl IntoOwnedPythonStorage for NoStorage {
    fn try_map_state(_storage: &Self::PythonStorage, _state: NeverRecord) -> Result<PythonRecord, PyErr> {
        unreachable!("NeverRecord can't exist")
    }
}

impl IntoPythonStorage for StreamRs<PythonSchemaRecord<AvroSchema>> {
    type PythonStorage = Stream;
    
    type StorageInitialiser = PythonSchemaInitialiser;

    fn into_python_storage(self, py: Python, locals: &TaskLocals, initialiser: Self::StorageInitialiser) -> Self::PythonStorage {
        Stream::new(self, locals.clone_ref(py), initialiser)
    }
}

impl IntoPythonStorage for OwnedStreamRs<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>> {
    type PythonStorage = OwnedStream;

    type StorageInitialiser = (PythonSchemaInitialiser, PythonSchemaInitialiser);
    
    fn into_python_storage(
        self,
        py: Python,
        locals: &TaskLocals,
        (state_initialiser, output_initialiser): Self::StorageInitialiser
    ) -> Self::PythonStorage {
        OwnedStream::new(self, locals.clone_ref(py), state_initialiser, output_initialiser)
    }
}

impl IntoOwnedPythonStorage for OwnedStreamRs<PythonSchemaRecord<AvroSchema>, PythonSchemaRecord<AvroSchema>> {
    fn try_map_state(
        storage: &Self::PythonStorage, 
        state: PythonSchemaRecord<AvroSchema>
    ) -> Result<PythonRecord, PyErr> {
        PythonRecord::try_from_value(
            state.0.into_inner(),
            storage.state_schema()
        )
    }
}
