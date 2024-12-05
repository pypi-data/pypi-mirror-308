use std::collections::BTreeMap;
use apache_avro::Schema;
use apache_avro::schema::{Name, RecordField, RecordFieldOrder, RecordSchema};

pub fn int_schema_name() -> Name {
    Name::from("TAIAO.Python.int")
}

pub fn int_schema(as_ref: bool) -> Schema {
    let name = int_schema_name();
    
    if as_ref {
        return Schema::Ref { name }
    }
    
    Schema::Record(
        RecordSchema {
            name,
            aliases: None,
            doc: Some("Avro record representing a Python int".to_owned()),
            fields: vec![
                RecordField {
                    name: "bytes".to_owned(),
                    doc: Some("Big-endian 2's-complement byte-array representation".to_owned()),
                    aliases: None,
                    default: None,
                    schema: Schema::Bytes,
                    order: RecordFieldOrder::Ignore,
                    position: 0,
                    custom_attributes: Default::default(),
                }
            ],
            lookup: BTreeMap::from([("bytes".to_owned(), 0)]),
            attributes: Default::default(),
        }
    )
}
