pub mod impls;
pub mod record;

mod into_python_storage;
pub use into_python_storage::{IntoPythonStorage, IntoOwnedPythonStorage};

mod storage_provider;
pub use storage_provider::StorageProvider;

mod storage_type;
pub use storage_type::{StorageType, StorageTypeInner, OwnedStorageType, OwnedStorageTypeInner};

use pyo3::prelude::*;
use crate::util::add_package_submodule;

/// Implementations for storage access for services on the TAIAO Platform.
#[pymodule]
pub fn storage_submodule(m: &Bound<PyModule>) -> PyResult<()> {
    add_package_submodule::<false, _>(m, "impls", impls::impls_submodule)?;
    add_package_submodule::<false, _>(m, "record", record::record_submodule)?;
    m.add_class::<StorageProvider>()?;
    m.add_class::<StorageType>()?;
    m.add_class::<OwnedStorageType>()?;
    Ok(())
}
