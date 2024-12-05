use std::cmp::max;
use std::collections::HashMap;
use std::ops::Deref;
use apache_avro::types::Value;
use exactly_n::ExactlyN;
use pyo3::{Bound, DowncastError, FromPyObject, IntoPy, Py, PyAny, PyErr, PyObject, PyResult, Python, PyTypeInfo, ToPyObject};
use pyo3::exceptions::{PyNotImplementedError, PyTypeError, PyValueError};
use pyo3::types::{PyAnyMethods, PyBool, PyBoolMethods, PyByteArray, PyByteArrayMethods, PyBytes, PyBytesMethods, PyDateTime, PyDict, PyDictMethods, PyFloat, PyFloatMethods, PyInt, PyList, PyListMethods, PyNone, PyString, PyStringMethods, PyType};
use taiao_storage::record::schema::impls::avro::util::DateTime;
use crate::storage::record::{dataclass};
use crate::storage::record::python_schema_initialiser::PythonSchemaInitialiser;

/// New-type struct for converting Python arguments to Rust.
#[derive(Debug, Clone)]
pub enum PythonRecord {
    None,
    Bool(bool),
    Int(Vec<u8>), // Big-endian 2's-complement representation as required by Avro Decimal
    Float(f64),
    Bytes(Vec<u8>),
    String(String),
    DateTime(DateTime),
    Dict(HashMap<String, PythonRecord>),
    List(Vec<PythonRecord>),
    Dataclass { 
        reference: Py<PyType>,
        fields: HashMap<String, PythonRecord>
    }
}

impl PythonRecord {
    fn int_from_bytes<'py>(py: Python<'py>, bytes: &[u8]) -> Bound<'py, PyInt> {
        let from_bytes = PyInt::type_object_bound(py).getattr("from_bytes")
            .expect("'int' type has 'from_bytes' attribute");
        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("signed", true)
            .expect("str -> bool can be set in kwargs");
        let int = from_bytes.call((PyBytes::new_bound(py, bytes), "big"), Some(&kwargs))
            .expect("'from_bytes' call succeeds");
        int.downcast_into::<PyInt>()
            .expect("'from_bytes' returns an int")
    }

    pub fn try_from_value(
        value: Value,
        python_schema: &PythonSchemaInitialiser
    ) -> Result<Self, PyErr> {
        let record = match value {
            Value::Null => PythonRecord::None,
            Value::Boolean(value) => PythonRecord::Bool(value),
            Value::Int(value) => PythonRecord::Int(value.to_be_bytes().to_vec()),
            Value::Long(value) => PythonRecord::Int(value.to_be_bytes().to_vec()),
            Value::Float(value) => PythonRecord::Float(value as f64),
            Value::Double(value) => PythonRecord::Float(value),
            Value::Bytes(value) => PythonRecord::Bytes(value),
            Value::String(value) => PythonRecord::String(value),
            Value::Fixed(_, value) => PythonRecord::Bytes(value),
            Value::Enum(_, value) => PythonRecord::String(value),
            Value::Union(_, value) => Self::try_from_value(*value, python_schema)?,
            Value::Array(value) => {
                let element_python_schema = match python_schema {
                    PythonSchemaInitialiser::List { element_schema: element_python_schema }
                        => element_python_schema.deref(),
                    _ => return Err(PyValueError::new_err("schema mismatch"))
                };
                let mut list = Vec::with_capacity(value.len());
                for element in value.into_iter() {
                    list.push(Self::try_from_value(element, element_python_schema)?);
                }
                PythonRecord::List(list)
            },
            Value::Map(value) => {
                let value_python_schema = match python_schema {
                    PythonSchemaInitialiser::Dict { value_schema: value_python_schema }
                        => value_python_schema.deref(),
                    _ => return Err(PyValueError::new_err("schema mismatch"))
                };
                let mut dict = HashMap::with_capacity(value.len());
                for (key, value) in value.into_iter() {
                    dict.insert(key, Self::try_from_value(value, value_python_schema)?);
                }
                PythonRecord::Dict(dict)
            },
            Value::Record(value) => {
                match python_schema {
                    PythonSchemaInitialiser::Int => {
                        if let Ok([(_, value)]) = value.into_iter().exactly_n::<1>() {
                            match value {
                                | Value::Bytes(bytes)
                                | Value::Fixed(_, bytes) => return Ok(PythonRecord::Int(bytes)),
                                Value::Decimal(decimal) => match decimal.try_into() {
                                    Ok(vec) => return Ok(PythonRecord::Int(vec)),
                                    Err(error) => return Err(PyValueError::new_err(error.to_string()))
                                },
                                _ => { /* Fall through to error case */ }
                            }
                        }
                    },
                    PythonSchemaInitialiser::Dataclass { reference, fields: python_schema_fields, .. } => {
                        let mut fields = HashMap::new();
                        for (field_name, field_value) in value.into_iter() {
                            let python_field_schema = python_schema_fields.get(&field_name)
                                .ok_or_else(|| PyTypeError::new_err(format!("Unrecognised field '{field_name}'")))?;
                            let field_record = Self::try_from_value(field_value, python_field_schema)?;
                            fields.insert(field_name, field_record);
                        }
                        return Ok(PythonRecord::Dataclass { reference: reference.clone(), fields })
                    },
                    _ => { /* Fall through to error case */ }
                }

                return Err(PyValueError::new_err("unrecognised record type"))
            },
            Value::Date(_) => return Err(PyNotImplementedError::new_err("date")),
            Value::Decimal(_) => return Err(PyNotImplementedError::new_err("decimal")),
            Value::TimeMillis(_) => return Err(PyNotImplementedError::new_err("time millis")),
            Value::TimeMicros(_) => return Err(PyNotImplementedError::new_err("time micros")),
            Value::TimestampMillis(value) => PythonRecord::DateTime(
                DateTime::from_millis(value)
                    .ok_or_else(|| PyValueError::new_err(format!("{value} out-of-range")))?
            ),
            Value::TimestampMicros(_) => return Err(PyNotImplementedError::new_err("timestamp micros")),
            Value::LocalTimestampMillis(_) => return Err(PyNotImplementedError::new_err("local timestamp millis")),
            Value::LocalTimestampMicros(_) => return Err(PyNotImplementedError::new_err("local timestamp micros")),
            Value::Duration(_) => return Err(PyNotImplementedError::new_err("duration")),
            Value::Uuid(_) => return Err(PyNotImplementedError::new_err("uuid")),
        };

        Ok(record)
    }

    fn get_int_bytes(int: &Bound<PyInt>) -> PyResult<Vec<u8>> {
        let to_bytes = int.getattr("to_bytes")?;
        let bit_length = int.getattr("bit_length")?;
        let bit_length = <usize as FromPyObject>::extract_bound(&bit_length.call0()?)?
            + 1; // For the sign bit, may not be needed, but probably faster than working it out
        let byte_length = max(bit_length.div_ceil(8), 1);
        let kwargs = PyDict::new_bound(int.py());
        kwargs.set_item("signed", true)?;
        let bytes = to_bytes.call((byte_length, "big"), Some(&kwargs))?;
        let bytes = bytes.downcast::<PyBytes>()?;
        Ok(bytes.as_bytes().to_vec())
    }

    fn extract_dataclass(ob: &Bound<PyAny>) -> PyResult<Option<Self>> {
        let py_type = ob.get_type();
        
        let fields = match dataclass::fields(&py_type)? {
            Some(fields) => fields,
            None => return Ok(None)
        };
        
        let mut result = HashMap::new();
        for field in fields.iter()? {
            let field = field?;
            let field_name = field.getattr("name")?
                .str()?
                .to_str()?
                .to_owned();
            let field_value = ob.getattr(field_name.deref())?;
            let field_record = FromPyObject::extract_bound(&field_value)?;
            result.insert(field_name, field_record);
        }
        
        Ok(Some(Self::Dataclass { reference: py_type.unbind(), fields: result }))
    }
}

impl<'source> FromPyObject<'source> for PythonRecord {
    fn extract_bound(ob: &Bound<'source, PyAny>) -> PyResult<Self> {
        if ob.is_none() {
            Ok(Self::None)
        } else if let Ok(bool) = ob.downcast::<PyBool>() {
            Ok(Self::Bool(bool.is_true()))
        } else if let Ok(int) = ob.downcast::<PyInt>() {
            Ok(Self::Int(Self::get_int_bytes(int)?))
        } else if let Ok(float) = ob.downcast::<PyFloat>() {
            Ok(Self::Float(float.value()))
        } else if let Ok(bytes) = ob.downcast::<PyBytes>() {
            Ok(Self::Bytes(bytes.as_bytes().to_vec()))
        } else if let Ok(byte_array) = ob.downcast::<PyByteArray>() {
            Ok(Self::Bytes(byte_array.to_vec()))
        } else if let Ok(string) = ob.downcast::<PyString>() {
            Ok(Self::String(string.to_str()?.to_owned()))
        } else if let Ok(datetime) = ob.downcast::<PyDateTime>() {
            Ok(Self::DateTime(DateTime(FromPyObject::extract_bound(datetime)?)))
        } else if let Ok(dict) = ob.downcast::<PyDict>() { 
            let mut hash_map = HashMap::with_capacity(dict.len());
            for (key, value) in dict.iter() {
                hash_map.insert(key.extract()?, value.extract()?);
            }
            Ok(Self::Dict(hash_map))
        } else if let Ok(list) = ob.downcast::<PyList>() {
            let mut vec = Vec::with_capacity(list.len());
            for item in list.iter() {
                vec.push(item.extract()?);
            }
            Ok(Self::List(vec))
        } else if let Some(record) = Self::extract_dataclass(ob)? {
            Ok(record)
        } else {
            Err(DowncastError::new(ob, "Record").into())
        }
    }
}

impl From<&PythonRecord> for Value {
    fn from(value: &PythonRecord) -> Self {
        match value {
            PythonRecord::None => Self::Null,
            PythonRecord::Bool(value) => Self::Boolean(*value),
            PythonRecord::Int(value) => Self::Record(vec![("bytes".to_owned(), Self::Bytes(value.clone()))]),
            PythonRecord::Float(value) => Self::Double(*value),
            PythonRecord::Bytes(value) => Self::Bytes(value.clone()),
            PythonRecord::String(value) => Self::String(value.clone()),
            PythonRecord::DateTime(value) => Self::TimestampMillis(value.as_millis()),
            PythonRecord::Dict(value) => Self::Map(
                value.into_iter()
                    .map(|(key, value)| (key.to_owned(), value.into()))
                    .collect()
            ),
            PythonRecord::List(value) => Self::Array(
                value.into_iter()
                    .map(From::from)
                    .collect()
            ),
            PythonRecord::Dataclass { fields, .. } => Self::Record(
                fields.into_iter()
                    .map(|(name, value)| (name.clone(), Self::from(value)))
                    .collect()
            )
        }
    }
}

impl From<PythonRecord> for Value {
    fn from(value: PythonRecord) -> Self {
        match value {
            PythonRecord::None => Self::Null,
            PythonRecord::Bool(value) => Self::Boolean(value),
            PythonRecord::Int(value) => Self::Record(vec![("bytes".to_owned(), Self::Bytes(value))]),
            PythonRecord::Float(value) => Self::Double(value),
            PythonRecord::Bytes(value) => Self::Bytes(value),
            PythonRecord::String(value) => Self::String(value),
            PythonRecord::DateTime(value) => Self::TimestampMillis(value.as_millis()),
            PythonRecord::Dict(value) => Self::Map(
                value.into_iter()
                    .map(|(key, value)| (key, value.into()))
                    .collect()
            ),
            PythonRecord::List(value) => Self::Array(
                value.into_iter()
                    .map(From::from)
                    .collect()
            ),
            PythonRecord::Dataclass { fields, .. } => Self::Record(
                fields.into_iter()
                    .map(|(name, value)| (name, Self::from(value)))
                    .collect()
            )
        }
    }
}

impl IntoPy<PyObject> for PythonRecord {
    fn into_py(self, py: Python<'_>) -> PyObject {
        macro_rules! tri {
            ($expr:expr) => {{
                let maybe_error = ($expr).into_py(py);
                if maybe_error.bind(py).is_instance_of::<pyo3::exceptions::PyBaseException>() {
                    return maybe_error
                }
                maybe_error
            }};
        }
        
        match self {
            PythonRecord::None => PyNone::get_bound(py).to_owned().into_any().into_py(py),
            PythonRecord::Bool(value) => value.to_object(py),
            PythonRecord::Int(value) => Self::int_from_bytes(py, &value).into(),
            PythonRecord::Float(value) => value.to_object(py),
            PythonRecord::Bytes(value) => PyBytes::new_bound(py, &value).into(),
            PythonRecord::String(value) => value.to_object(py),
            PythonRecord::DateTime(value) => value.0.into_py(py),
            PythonRecord::Dict(value) => {
                let dict = PyDict::new_bound(py);
                for (key, value) in value.into_iter() {
                    let value = tri!(value);
                    if let Err(error) = dict.set_item(key, value) {
                        return error.into_py(py)
                    }
                }
                dict.into_py(py)
            },
            PythonRecord::List(value) => {
                let mut vec = Vec::with_capacity(value.len());
                for element in value.into_iter() {
                    let element = tri!(element);
                    vec.push(element);
                }
                vec.into_py(py)
            },
            PythonRecord::Dataclass { reference, fields } => {
                let kwargs = PyDict::new_bound(py);
                for (field_name, field_value) in fields.into_iter() {
                    let field_value = tri!(field_value);
                    if let Err(error) = kwargs.set_item(field_name, field_value) {
                        return error.into_py(py)
                    }
                }
                
                match reference.bind(py).call((), Some(&kwargs)) {
                    Ok(instance) => instance.into_py(py),
                    Err(error) => error.into_py(py)
                }
            }
        }
    }
}
