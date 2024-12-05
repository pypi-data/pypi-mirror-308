mod fully_qualified_name;
pub use fully_qualified_name::FullyQualifiedName;

mod name;
pub use name::{Name, ClientName, ProjectName, ServiceName};

mod periodicity;
pub use periodicity::Periodicity;

mod port_number;
pub use port_number::PortNumber;

mod privacy;
pub use privacy::Privacy;

mod service_configuration;
pub use service_configuration::ServiceConfiguration;

mod storage;
pub use storage::Storage;

use pyo3::prelude::*;

/// Types used by the TAIAO API and the service library.
#[pymodule]
pub fn types_submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FullyQualifiedName>()?;
    m.add_class::<Name>()?;
    m.add_class::<ClientName>()?;
    m.add_class::<ProjectName>()?;
    m.add_class::<ServiceName>()?;
    m.add_class::<Periodicity>()?;
    m.add_class::<PortNumber>()?;
    m.add_class::<Privacy>()?;
    m.add_class::<ServiceConfiguration>()?;
    m.add_class::<Storage>()?;
    Ok(())
}
