mod dataclass;

mod int_schema;

mod python_record;
pub use python_record::PythonRecord;

mod python_schema;
pub use python_schema::PythonSchema;

mod python_schema_initialiser;
pub(crate) use python_schema_initialiser::PythonSchemaInitialiser;

mod python_schema_record;
pub use python_schema_record::PythonSchemaRecord;

use pyo3::prelude::*;

#[pymodule]
pub fn record_submodule(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<PythonSchema>()?;
    Ok(())
}
