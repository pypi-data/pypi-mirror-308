//! Rust implementation for the Type Length Value Encoding.
//!
//! Within communication protocols, TLV (type-length-value or tag-length-value)
//! is an encoding scheme used for optional informational elements
//! in a certain protocol.
//!
//! A TLV-encoded data stream contains code related to the record type,
//! the record value's length, and finally the value itself.
//!
//! Details
//! The type and length are fixed in size (typically 1–4 bytes), and the value field is of variable size. These fields are used as follows:
//!
//! Type
//!
//! A binary code, often simply alphanumeric, which indicates the kind of field that this part of the message represents;
//!
//! Length
//! The size of the value field (typically in bytes);
//!
//! Value
//! Variable-sized series of bytes which contains data for this part of the message.
//!
//! Some advantages of using a TLV representation data system solution are:
//!
//! - TLV sequences are easily searched using generalized parsing functions;
//! - New message elements which are received at an older node can be safely skipped and the rest
//! of the message can be parsed. This is similar to the way that unknown XML tags can be safely skipped;
//! - TLV elements can be placed in any order inside the message body;
//! - TLV elements are typically used in a binary format and binary protocols which
//! makes parsing faster and the data smaller than in comparable text based protocols.
//!
//! Author: Vincenzo Palazzo <vincenzopalazzodev@gmail.com>
#[cfg(feature = "pyo3")]
use pyo3::pyclass;

use crate::core::{FromWire, ToWire};
use crate::types::BigSize;

/// Stream - A `tlv_stream` is a series of (possibly zero) `tlv_record`s, represented as the
/// concatenation of the encoded `tlv_record`s. When used to extend existing
/// messages, a `tlv_stream` is typically placed after all currently defined fields.
#[cfg_attr(feature = "pyo3", pyclass)]
#[derive(Clone, Default)]
pub struct Stream {
    pub records: Vec<Record>,
}

impl std::fmt::Debug for Stream {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.records)
    }
}

impl ToWire for Stream {
    fn to_wire<W: std::io::Write>(&self, writer: &mut W) -> std::io::Result<()> {
        for record in &self.records {
            record.to_wire(writer)?;
        }
        Ok(())
    }
}

impl FromWire for Stream {
    fn from_wire<R: std::io::Read>(reader: &mut R) -> std::io::Result<Self> {
        let mut records = Vec::new();
        loop {
            let record = Record::from_wire(reader);
            if let Err(err) = &record {
                // we arrived at end of stream, so we break the loop
                if err.kind() == std::io::ErrorKind::UnexpectedEof {
                    break;
                }
            }
            records.push(record?);
        }
        Ok(Self { records })
    }
}

/// A `tlv_record` represents a single field, encoded in the form:
///
/// * [`bigsize`: `type`]
/// * [`bigsize`: `length`]
/// * [`length`: `value`]
#[cfg_attr(feature = "pyo3", pyclass)]
#[derive(Clone)]
pub struct Record {
    /// The `type` is encoded using the BigSize format. It functions as a
    /// message-specific, 64-bit identifier for the `tlv_record` determining how the
    /// contents of `value` should be decoded. `type` identifiers below 2^16 are
    /// reserved for use in this specification. `type` identifiers greater than or equal
    /// to 2^16 are available for custom records. Any record not defined in this
    /// specification is considered a custom record. This includes experimental and
    /// application-specific messages.
    pub ty: BigSize,
    /// The `length` is encoded using the BigSize format signaling the size of
    /// `value` in bytes.
    pub lenght: BigSize,
    /// The `value` depends entirely on the `type`, and should be encoded or decoded
    /// according to the message-specific format determined by `type`.
    pub value: Vec<u8>,
}

impl std::fmt::Debug for Record {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{{")?;
        writeln!(f, "   ty: {:?}", self.ty)?;
        writeln!(f, "   len: {:?}", self.lenght)?;
        writeln!(f, "   hex: {:x}", self)?;
        write!(f, "}}")
    }
}

impl std::fmt::LowerHex for Record {
    fn fmt(&self, fmtr: &mut std::fmt::Formatter) -> Result<(), std::fmt::Error> {
        for byte in self.value.iter() {
            fmtr.write_fmt(format_args!("{:02x}", byte))?;
        }
        Ok(())
    }
}

impl ToWire for Record {
    fn to_wire<W: std::io::Write>(&self, writer: &mut W) -> std::io::Result<()> {
        self.ty.to_wire(writer)?;
        self.lenght.to_wire(writer)?;
        writer.write(&self.value)?;
        Ok(())
    }
}

impl FromWire for Record {
    fn from_wire<R: std::io::Read>(reader: &mut R) -> std::io::Result<Self> {
        let ty = BigSize::from_wire(reader)?;
        let lenght = BigSize::from_wire(reader)?;
        // FIXME: this depends from the types
        let mut buffer = vec![0u8; lenght.value as usize];
        reader.read_exact(&mut buffer)?;
        Ok(Record {
            ty,
            lenght,
            value: buffer.to_vec(),
        })
    }
}
