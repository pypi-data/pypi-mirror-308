use pyo3::{pyclass, pymethods};
use taiao_types::{ServiceConfiguration as ServiceConfigurationRs};
use crate::types::{ClientName, FullyQualifiedName, Periodicity, PortNumber, Privacy, ProjectName, ServiceName, Storage};
use crate::util::FromStrParameter;

type OrStringRepr<T> = FromStrParameter<false, T>;

/// How a service is configured to run on the TAIAO Platform.
#[pyclass]
#[derive(Clone)]
pub struct ServiceConfiguration {
    inner: ServiceConfigurationRs
}

#[pymethods]
impl ServiceConfiguration {
    /// Creates a new [configuration](ServiceConfiguration).
    /// 
    /// * `client`: The client who owns the service
    /// * `project`: The client's project that the service belongs to
    /// * `service`: The name of the service
    /// * `storage`: The service's [storage type](Storage)
    /// * `privacy`: Who can access the service's dataset
    /// * `periodicity`: How often the service should run
    /// * `listen`: Which port the service should listen on (if any)
    #[new]
    pub fn new(
        client: OrStringRepr<ClientName>,
        project: OrStringRepr<ProjectName>,
        service: OrStringRepr<ServiceName>,
        storage: OrStringRepr<Storage>,
        privacy: OrStringRepr<Privacy>,
        periodicity: Periodicity,
        listen: OrStringRepr<PortNumber>
    ) -> Self {
        ServiceConfigurationRs {
            client: client.value.into(),
            project: project.value.into(),
            service: service.value.into(),
            storage: storage.value.into(),
            privacy: privacy.value.into(),
            periodicity: periodicity.into(),
            listen: listen.value.into(),
        }.into()
    }

    /// Gets the [fully-qualified name](FullyQualifiedName) of the service.
    #[getter]
    pub fn get_fully_qualified_name(&self) -> FullyQualifiedName {
        self.inner.fully_qualified_name().into()
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

    #[getter]
    pub fn get_storage(&self) -> Storage {
        self.inner.storage.into()
    }

    #[getter]
    pub fn get_privacy(&self) -> Privacy {
        self.inner.privacy.into()
    }

    #[getter]
    pub fn get_periodicity(&self) -> Periodicity {
        self.inner.periodicity.clone().into()
    }

    #[getter]
    pub fn get_listen(&self) -> PortNumber {
            self.inner.listen.into()
    }

    #[setter]
    pub fn set_client(&mut self, client: OrStringRepr<ClientName>) {
        self.inner.client = client.value.into();
    }

    #[setter]
    pub fn set_project(&mut self, project: OrStringRepr<ProjectName>) {
        self.inner.project = project.value.into();
    }

    #[setter]
    pub fn set_service(&mut self, service: OrStringRepr<ServiceName>) {
        self.inner.service = service.value.into();
    }

    #[setter]
    pub fn set_storage(&mut self, storage: OrStringRepr<Storage>) {
        self.inner.storage = storage.value.into();
    }

    #[setter]
    pub fn set_privacy(&mut self, privacy: OrStringRepr<Privacy>) {
        self.inner.privacy = privacy.value.into();
    }

    #[setter]
    pub fn set_periodicity(&mut self, periodicity: Periodicity) {
        self.inner.periodicity = periodicity.into();
    }

    #[setter]
    pub fn set_listen(&mut self, listen: OrStringRepr<PortNumber>) {
        self.inner.listen = listen.value.into();
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

impl From<ServiceConfigurationRs> for ServiceConfiguration {
    fn from(value: ServiceConfigurationRs) -> Self {
        Self { inner: value }
    }
}

impl From<ServiceConfiguration> for ServiceConfigurationRs {
    fn from(value: ServiceConfiguration) -> Self {
        value.inner
    }
}
