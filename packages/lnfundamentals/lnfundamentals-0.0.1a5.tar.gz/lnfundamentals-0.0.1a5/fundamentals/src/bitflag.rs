//! Bitflag rust Implementation.
//!
//! Author: Vincenzo Palazzo <vincenzopalazzodev@gmail.com>.
use std::vec::Vec;

#[cfg(feature = "pyo3")]
use pyo3::pyclass;

use crate::core::{FromWire, ToWire};

// FIXME: rename to bitvector :)
#[cfg_attr(feature = "pyo3", pyclass)]
#[derive(Clone, Debug, Default)]
pub struct BitFlag {
    pub len: u16,
    inner: Vec<u8>,
}

impl BitFlag {
    pub fn to_slice(&self) -> &[u8] {
        &self.inner
    }
}

impl ToWire for BitFlag {
    fn to_wire<W: std::io::Write>(&self, writer: &mut W) -> std::io::Result<()> {
        self.len.to_wire(writer)?;
        writer.write_all(&self.inner)?;
        Ok(())
    }
}

impl FromWire for BitFlag {
    fn from_wire<R: std::io::Read>(reader: &mut R) -> std::io::Result<Self> {
        let size = u16::from_wire(reader)?;
        let mut buff = vec![0u8; size as usize];
        reader.read_exact(&mut buff)?;
        Ok(Self {
            len: size,
            inner: buff,
        })
    }
}
