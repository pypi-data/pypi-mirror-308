use std::collections::{BTreeMap, HashMap};
use std::mem::discriminant;
use std::ops::Deref;
use apache_avro::Schema as AvroSchema;
use apache_avro::schema::{Name, RecordField, RecordFieldOrder, RecordSchema};
use exactly_n::{ExactlyN, ExactlyNError};
use pyo3::{Bound, DowncastError, FromPyObject, Py, PyAny, PyResult, PyTypeInfo};
use pyo3::exceptions::{PyTypeError};
use pyo3::types::{PyAnyMethods, PyBool, PyBytes, PyDateTime, PyDict, PyFloat, PyInt, PyList, PyString, PyStringMethods, PyType, PyTypeMethods};
use crate::storage::record::dataclass;
use crate::storage::record::int_schema::int_schema;

#[derive(Clone, Debug)]
pub enum PythonSchemaInitialiser {
    None,
    Bool,
    Int,
    Float,
    Bytes,
    String,
    DateTime,
    /// A dictionary of string keys to values of a given type
    Dict { 
        value_schema: Box<PythonSchemaInitialiser> 
    },
    List { 
        element_schema: Box<PythonSchemaInitialiser> 
    },
    Dataclass {
        reference: Py<PyType>,
        name: String,
        doc: String,
        fields: HashMap<String, PythonSchemaInitialiser> 
    }
}

impl PythonSchemaInitialiser {
    fn extract_dataclass(
        py_type: &Bound<PyType>,
        fields: &Bound<PyAny>
    ) -> PyResult<Self> {
        let name = py_type.name()?.to_str()?.to_owned();
        let doc = py_type.getattr("__doc__")?
            .str()?
            .to_str()?
            .to_owned();
        let mut result_fields = HashMap::new();
        for field in fields.iter()? {
            let field = field?;
            let field_name = field.getattr("name")?
                .str()?
                .to_str()?
                .to_owned();
            let field_type = PythonSchemaInitialiser::extract_bound(&field.getattr("type")?)?;
            result_fields.insert(field_name, field_type);
        }
        Ok(Self::Dataclass {
            reference: Py::from(py_type.clone()),
            name,
            doc,
            fields: result_fields
        })
    }


    fn avro_record_schema_from_dataclass(
        name: &String,
        doc: &String,
        fields: &HashMap<String, PythonSchemaInitialiser>
    ) -> AvroSchema {
        let name = Name::from(name.deref());

        let mut record_fields = Vec::new();
        let mut lookup = BTreeMap::new();

        for (field_name, field_initialiser) in fields.into_iter() {
            let position = record_fields.len();
            let record_field = RecordField {
                name: field_name.clone(),
                doc: None,
                aliases: None,
                default: None,
                schema: From::from(field_initialiser),
                order: RecordFieldOrder::Ignore,
                position,
                custom_attributes: Default::default(),
            };

            record_fields.push(record_field);
            lookup.insert(field_name.clone(), position);
        }

        let avro_schema = AvroSchema::Record(
            RecordSchema {
                name,
                aliases: None,
                doc: Some(doc.clone()),
                fields: record_fields,
                lookup,
                attributes: Default::default(),
            }
        );

        avro_schema
    }
    
    fn get_generics<'py>(ob: &Bound<'py, PyAny>) -> PyResult<Option<(Bound<'py, PyAny>, Bound<'py, PyAny>)>> {
        let py = ob.py();
        let typing = py.import_bound("typing")?;
        let get_origin = typing.getattr("get_origin")?;
        let origin = get_origin.call1((ob,))?;
        if origin.is_none() {
            return Ok(None)
        }
        let get_args = typing.getattr("get_args")?;
        let args = get_args.call1((ob,))?;
        Ok(Some((origin, args)))
    }

    fn get_list_element_type(origin: &Bound<PyAny>, args: &Bound<PyAny>) -> PyResult<Option<PythonSchemaInitialiser>> {
        let origin = match origin.downcast::<PyType>() {
            Ok(py_type) => py_type,
            Err(_) => return Ok(None)
        };

        if !origin.is(&PyList::type_object_bound(origin.py())) {
            return Ok(None)
        }

        let first_arg = match args.iter()?.exactly_n::<1>() {
            Ok([first]) => first?,
            Err(error) => return match error {
                ExactlyNError::TooFew(_) => Err(PyTypeError::new_err("list type missing element type")),
                ExactlyNError::TooMany { .. } => Err(PyTypeError::new_err("list type has more than 1 element type")),
            }
        };

        Ok(Some(FromPyObject::extract_bound(&first_arg)?))
    }

    fn get_dict_value_type(origin: &Bound<PyAny>, args: &Bound<PyAny>) -> PyResult<Option<PythonSchemaInitialiser>> {
        let origin = match origin.downcast::<PyType>() {
            Ok(py_type) => py_type,
            Err(_) => return Ok(None)
        };

        if !origin.is(&PyDict::type_object_bound(origin.py())) {
            return Ok(None)
        }

        let second_arg = match args.iter()?.exactly_n::<2>() {
            Ok([first, second]) => { 
                if !first?.is(&PyString::type_object_bound(origin.py())) {
                    return Err(PyTypeError::new_err("dict type has non-string key-type"))
                }
                
                second?
            },
            Err(error) => return match error {
                ExactlyNError::TooFew(args) => match args.len() {
                    0 => Err(PyTypeError::new_err("dict type missing key and value types")),
                    1 => Err(PyTypeError::new_err("dict type missing value type")),
                    _ => unreachable!("fewer than 2 implies 0 or 1")
                }
                ExactlyNError::TooMany { .. } => Err(PyTypeError::new_err("dict type has too many type arguments (should be 2)")),
            }
        };

        Ok(Some(FromPyObject::extract_bound(&second_arg)?))
    }
}

impl<'source> FromPyObject<'source> for PythonSchemaInitialiser {
    fn extract_bound(ob: &Bound<'source, PyAny>) -> PyResult<Self> {
        if ob.is_none() {
            return Ok(Self::None)
        }
        
        if let Some((origin, args)) = Self::get_generics(ob)? {
            if let Some(element_type) = Self::get_list_element_type(&origin, &args)? {
                return Ok(Self::List { element_schema: Box::new(element_type) })
            } else if let Some(value_type) = Self::get_dict_value_type(&origin, &args)? {
                return Ok(Self::Dict { value_schema: Box::new(value_type) })
            }
        }
        
        if let Ok(py_type) =  ob.downcast::<PyType>() {
            if py_type.is_subclass_of::<PyBool>()? {
                return Ok(Self::Bool)
            } else if py_type.is_subclass_of::<PyInt>()? {
                return Ok(Self::Int)
            } else if py_type.is_subclass_of::<PyFloat>()? {
                return Ok(Self::Float)
            } else if py_type.is_subclass_of::<PyBytes>()? {
                return Ok(Self::Bytes)
            } else if py_type.is_subclass_of::<PyString>()? {
                return Ok(Self::String)
            } else if py_type.is_subclass_of::<PyDateTime>()? {
                return Ok(Self::DateTime)
            } else if let Some(fields) = dataclass::fields(py_type)? {
                return Ok(Self::extract_dataclass(py_type, &fields)?)
            }
        }
        
        Err(DowncastError::new(ob, "Schema").into())
    }
}

impl From<&PythonSchemaInitialiser> for AvroSchema {
    fn from(value: &PythonSchemaInitialiser) -> Self {
        match value {
            PythonSchemaInitialiser::None => AvroSchema::Null,
            PythonSchemaInitialiser::Bool => AvroSchema::Boolean,
            PythonSchemaInitialiser::Int => int_schema(false).clone(),
            PythonSchemaInitialiser::Float => AvroSchema::Double,
            PythonSchemaInitialiser::Bytes => AvroSchema::Bytes,
            PythonSchemaInitialiser::String => AvroSchema::String,
            PythonSchemaInitialiser::DateTime => AvroSchema::TimestampMillis,
            PythonSchemaInitialiser::Dict { value_schema } => AvroSchema::Map(Box::new(AvroSchema::from(value_schema.deref()))),
            PythonSchemaInitialiser::List { element_schema } => AvroSchema::Array(Box::new(AvroSchema::from(element_schema.deref()))),
            PythonSchemaInitialiser::Dataclass {
                name,
                doc,
                fields ,
                ..
            } => PythonSchemaInitialiser::avro_record_schema_from_dataclass(name, doc, fields)
        }
    }
}

impl PartialEq for PythonSchemaInitialiser {
    fn eq(&self, other: &Self) -> bool {
        match self {
            | PythonSchemaInitialiser::None 
            | PythonSchemaInitialiser::Bool
            | PythonSchemaInitialiser::Int
            | PythonSchemaInitialiser::Float
            | PythonSchemaInitialiser::Bytes
            | PythonSchemaInitialiser::String
            | PythonSchemaInitialiser::DateTime => discriminant(self) == discriminant(other),
            PythonSchemaInitialiser::Dict { value_schema } => 
                if let PythonSchemaInitialiser::Dict { value_schema: other_value_schema} = other {
                    value_schema == other_value_schema
                } else {
                    false
                },
            PythonSchemaInitialiser::List { element_schema } =>
                if let PythonSchemaInitialiser::List { element_schema: other_element_schema} = other {
                    element_schema == other_element_schema
                } else {
                    false
                },
            PythonSchemaInitialiser::Dataclass {
                reference,
                ..
            } =>
                if let PythonSchemaInitialiser::Dataclass { reference: other_reference, .. } = other {
                    reference.is(other_reference)
                } else {
                    false
                }
        }
    }
}