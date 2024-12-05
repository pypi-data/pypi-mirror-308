use std::ops::Deref;
use std::str::FromStr;
use apache_avro::{Codec};
use apache_avro::schema::{Schema as AvroSchemaInner};
use pyo3::{Bound, PyAny, pyclass, pymethods, PyResult};
use pyo3::exceptions::PyValueError;
use pyo3::types::PyType;
use serde::{Serialize, Serializer};
use taiao_storage::record::schema::impls::avro::{AvroSchema as AvroSchemaRs};
use taiao_storage::record::schema::impls::avro::util::deduplicate;
use crate::error::TAIAOPyError;
use crate::storage::record::python_schema_initialiser::PythonSchemaInitialiser;

#[pyclass(frozen)]
#[derive(Clone, Debug)]
pub struct PythonSchema {
    pub initialiser: PythonSchemaInitialiser,
    pub avro_schema: AvroSchemaRs // TODO: Generic support for other internal schema types (otherwise can't read from services using other schema types)
}

#[pymethods]
impl PythonSchema {
    #[new]
    pub fn new(schema: PythonSchemaInitialiser, codec: &str, fingerprint: bool) -> PyResult<Self> {
        let mut avro_schema_inner = AvroSchemaInner::from(&schema);
        
        deduplicate(&mut avro_schema_inner)
            .map_err(TAIAOPyError::from)?;

        let codec = match Codec::from_str(codec) {
            Ok(parsed) => parsed,
            Err(_error) => return Err(PyValueError::new_err(format!("'{codec}' is not a recognised codec")))
        };

        let avro_schema = AvroSchemaRs::new(avro_schema_inner, codec, fingerprint);
        
        Ok(Self { initialiser: schema, avro_schema })
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

impl Deref for PythonSchema {
    type Target = AvroSchemaRs;

    fn deref(&self) -> &Self::Target {
        &self.avro_schema
    }
}

impl From<PythonSchema> for AvroSchemaRs {
    fn from(value: PythonSchema) -> Self {
        value.avro_schema
    }
}

impl PartialEq for PythonSchema {
    fn eq(&self, other: &Self) -> bool {
        self.initialiser == other.initialiser
    }
}

impl Serialize for PythonSchema {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error> where S: Serializer {
        self.avro_schema.serialize(serializer)
    }
}
