use pyo3::{pyclass, pymethods};
use rrule::RRuleSet;
use taiao_types::{Periodicity as PeriodicityRs};
use crate::util::FromStrParameter;

type StringRepr<T> = FromStrParameter<true, T>;

/// How often a service should be scheduled for execution. GPU use requires that the service
/// be periodic.
#[pyclass]
#[derive(Clone)]
pub struct Periodicity {
    inner: PeriodicityRs
}

#[pymethods]
impl Periodicity {
    /// The service should run continuously.
    #[staticmethod]
    pub fn continuous() -> Self {
        Self {
            inner: PeriodicityRs::Continuous
        }
    }

    /// The service requires GPU hardware support, so should run periodically.
    /// 
    /// * `rules`: a [Recurrence Rule](https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3)
    ///            describing when to schedule the service.
    #[staticmethod]
    pub fn periodic_with_gpu(rules: StringRepr<RRuleSet>) -> Self {
        Self {
            inner: PeriodicityRs::PeriodicWithGPU(rules.value)
        }
    }

    /// The service should run periodically, but does not require GPU hardware support.
    ///
    /// * `rules`: a [Recurrence Rule](https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3)
    ///            describing when to schedule the service.
    #[staticmethod]
    pub fn periodic_without_gpu(rules: StringRepr<RRuleSet>) -> Self {
        Self {
            inner: PeriodicityRs::PeriodicWithoutGPU(rules.value)
        }
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

impl From<PeriodicityRs> for Periodicity {
    fn from(value: PeriodicityRs) -> Self {
        Self { inner: value }
    }
}

impl From<Periodicity> for PeriodicityRs {
    fn from(value: Periodicity) -> Self {
        value.inner
    }
}
