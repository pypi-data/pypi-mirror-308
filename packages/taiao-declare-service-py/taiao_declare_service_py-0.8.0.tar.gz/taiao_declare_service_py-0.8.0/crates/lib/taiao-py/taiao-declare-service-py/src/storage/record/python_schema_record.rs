use std::borrow::Cow;
use std::convert::Infallible;
use taiao_storage::record::Record;
use taiao_storage::record::schema::Schema;

pub struct PythonSchemaRecord<S: Schema>(pub S::Value);

impl<S: Schema> Record for PythonSchemaRecord<S> {
    type Schema = S;
    type SchemaInitParams = S;
    type SchemaError = Infallible;
    type TryToValueError = Infallible;
    type TryFromValueError = Infallible;

    fn schema(init_params: Self::SchemaInitParams) -> Result<Self::Schema, Self::SchemaError> {
        Ok(init_params)
    }

    fn try_to_value(&self, _schema: &Self::Schema) -> Result<Cow<<Self::Schema as Schema>::Value>, Self::TryToValueError> {
        Ok(Cow::Borrowed(&self.0))
    }

    fn try_from_value(value: Cow<<Self::Schema as Schema>::Value>, _schema: &Self::Schema) -> Result<Self, Self::TryFromValueError> {
        Ok(Self(value.into_owned()))
    }
}
