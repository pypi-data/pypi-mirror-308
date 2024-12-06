use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use serde_json;

use fundamentals::core::{FromWire, ToWire};
use fundamentals::types::BigSize;

#[derive(Serialize, Deserialize)]
struct BigSizeTestVector {
    pub name: String,
    pub value: u64,
    pub bytes: String,
    pub exp_error: Option<String>,
}

fn load_test_vectors<T: DeserializeOwned>(vector: &str) -> T {
    use std::env;
    use std::fs;
    let root = env::var("CARGO_MANIFEST_DIR").unwrap();
    let content = fs::read_to_string(format!("{root}/tests/test_vectors/{vector}")).unwrap();
    let value: T = serde_json::from_str(&content).unwrap();
    value
}

#[test]
fn test_bigsize() {
    use std::io::BufReader;
    use std::io::BufWriter;

    let test_vectors: Vec<BigSizeTestVector> = load_test_vectors("bigsize_decoding.json");
    for vector in test_vectors {
        let bytes = hex::decode(vector.bytes.clone());
        assert!(bytes.is_ok(), "{:?}", bytes.unwrap_err());
        let bytes = bytes.unwrap();
        let mut reader = BufReader::new(bytes.as_slice());
        let wire_value = BigSize::from_wire(&mut reader);
        if vector.exp_error.is_some() {
            assert!(
                wire_value.is_err(),
                "{}: expected error but the decoding return no errors: {:?}",
                vector.name,
                wire_value
            );
            // FIXME: if the error do not match emit a warning
            // assert_eq!(
            //     vector.exp_error.unwrap(),
            //     wire_value.err().as_ref().unwrap().to_string()
            // );
        } else {
            let wire_value = wire_value.unwrap();
            assert_eq!(
                wire_value.value, vector.value,
                "{}: received value `{}` different from expected `{}`",
                vector.name, wire_value.value, vector.value
            );

            let buff = Vec::new();
            let mut writer = BufWriter::new(buff);
            let wire_value = wire_value.to_wire(&mut writer);
            assert!(wire_value.is_ok(), "{:?}", wire_value);
            let wire_value = hex::encode(writer.buffer());
            assert_eq!(
                wire_value, vector.bytes,
                "{}: encoded hex value `{}` different from the expected `{}`",
                vector.name, wire_value, vector.bytes
            );
        }
    }
}
