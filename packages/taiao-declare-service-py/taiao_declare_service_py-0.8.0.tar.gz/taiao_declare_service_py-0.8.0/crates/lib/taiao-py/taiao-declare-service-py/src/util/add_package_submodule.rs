use pyo3::{Bound, PyResult};
use pyo3::types::{PyAnyMethods, PyModule, PyModuleMethods, PyStringMethods};

pub fn add_package_submodule<const STRIP: bool, F: FnOnce(&Bound<PyModule>) -> PyResult<()>>(
    parent: &Bound<PyModule>,
    name: &str,
    f: F
) -> PyResult<()> {
    let py = parent.py();
    let parent_name = parent.name()?;
    let parent_name = parent_name.to_str()?;
    let parent_name = if STRIP {
        parent_name.strip_prefix("taiao_declare_service_py.").expect("STRIP only used at top level")
    } else { 
        parent_name
    };
    let fqn = format!("{}.{}", parent_name, name);
    let child_module = PyModule::new_bound(py, &fqn)?;
    f(&child_module)?;
    parent.add(name, &child_module)?;
    py.import_bound("sys")?
        .getattr("modules")?
        .set_item(fqn, child_module)?;
    Ok(())
}
