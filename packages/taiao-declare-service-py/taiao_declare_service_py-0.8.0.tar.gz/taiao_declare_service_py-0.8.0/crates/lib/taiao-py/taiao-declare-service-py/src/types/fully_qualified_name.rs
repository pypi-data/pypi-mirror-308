use pyo3::{pyclass, pymethods};
use crate::util::FromStrParameter;
use taiao_types::{FullyQualifiedName as FullyQualifiedNameRs};
use crate::types::{ClientName, ProjectName, ServiceName};

type OrString<T> = FromStrParameter<false, T>;

/// The fully-qualified name of a service, `client-project-service`.
#[pyclass]
#[derive(Copy, Clone)]
pub struct FullyQualifiedName {
    inner: FullyQualifiedNameRs
}

#[pymethods]
impl FullyQualifiedName {
    #[new]
    pub fn new(
        client: OrString<ClientName>,
        project: OrString<ProjectName>,
        service: OrString<ServiceName>
    ) -> Self {
        FullyQualifiedNameRs {
            client: client.value.into(),
            project: project.value.into(),
            service: service.value.into()
        }.into()
    }

    #[getter]
    pub fn get_client(&self) -> ClientName {
        self.inner.client.into()
    }

    #[getter]
    pub fn get_project(&self) -> ProjectName {
        self.inner.project.into()
    }

    #[getter]
    pub fn get_service(&self) -> ServiceName {
        self.inner.service.into()
    }

    #[setter]
    pub fn set_client(&mut self, client: OrString<ClientName>) {
        self.inner.client = client.value.into();
    }

    #[setter]
    pub fn set_project(&mut self, project: OrString<ProjectName>) {
        self.inner.project = project.value.into();
    }

    #[setter]
    pub fn set_service(&mut self, service: OrString<ServiceName>){
        self.inner.service = service.value.into();
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

impl From<FullyQualifiedNameRs> for FullyQualifiedName {
    fn from(value: FullyQualifiedNameRs) -> Self {
        Self { inner: value }
    }
}

impl From<FullyQualifiedName> for FullyQualifiedNameRs {
    fn from(value: FullyQualifiedName) -> Self {
        value.inner
    }
}
