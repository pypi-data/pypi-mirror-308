//! Lightning Network types implementation
use std::io::{Read, Write};

use crate::core::{FromWire, ToWire};
use crate::prelude::*;

/// to_wire_type_with_size - is an helper macros to
/// generate a ToWire and FromWire trait on basic
/// types that will be used in the `derive` proc macro.
///
/// EXPAND:
///
/// ```ingore
/// type Foo = [u8, 32];
///
/// impl ToWire for Foo {
///     fn to_write<W: Write>(&self, writer: &mut W) -> Result<(), Error> {
///         // this works because `u8` implement the `ToWire` crate
///         writer.write_all(self)
///     }
/// }
///
/// impl FromWire for Foo {
///     fn from_wire<R: Read>(reader: &mut R) -> std::io::Result<Self> {
///         // note that we know tha side here that is 32
///         let mut buffer = [0; 32];
///         reader.read_exact(&mut buff)?;
///         Ok(buff)
///     }
/// }
/// ```
macro_rules! to_wire_type_with_size {
    ($ty: ty, $size: expr) => {
        impl ToWire for $ty {
            fn to_wire<W: Write>(&self, buff: &mut W) -> std::io::Result<()> {
                buff.write_all(self)
            }
        }

        impl FromWire for $ty {
            fn from_wire<R: Read>(reader: &mut R) -> std::io::Result<Self> {
                let mut buff = [0; $size];
                reader.read_exact(&mut buff)?;
                Ok(buff)
            }
        }
    };
}

pub type ChainHash = [u8; 32];
pub type ChannelId = [u8; 32];
pub type Sha256 = [u8; 32];
pub type Signature = [u8; 64];
pub type Point = [u8; 33];
pub type ShortChannelId = [u8; 8];
pub type Color = [u8; 3];

to_wire_type_with_size!(ChainHash, 32);
to_wire_type_with_size!(Signature, 64);
to_wire_type_with_size!(Point, 33);
to_wire_type_with_size!(ShortChannelId, 8);
to_wire_type_with_size!(Color, 3);

/// BigSize type implementation.
#[derive(Debug, Clone)]
pub struct BigSize {
    pub value: u64,
}

impl FromWire for BigSize {
    fn from_wire<R: Read>(buff: &mut R) -> std::io::Result<Self> {
        let flag = u8::from_wire(buff)?;
        let value = match flag {
            0xFF => {
                let value = u64::from_wire(buff)?;
                if value < 0x100000000 {
                    return error!("decoded bigsize is not canonical");
                }
                BigSize { value }
            }
            0xFE => {
                let value = u32::from_wire(buff)?;
                if value < 0x10000 {
                    return error!("decoded bigsize is not canonical");
                }
                BigSize {
                    value: value as u64,
                }
            }
            0xFD => {
                let value = u16::from_wire(buff)?;
                if value < 0xFD {
                    return error!("decoded bigsize is not canonical");
                }
                BigSize {
                    value: value as u64,
                }
            }
            _ => BigSize { value: flag as u64 },
        };
        Ok(value)
    }
}

impl ToWire for BigSize {
    fn to_wire<W: Write>(&self, buff: &mut W) -> std::io::Result<()> {
        match self.value {
            0..=0xFC => (self.value as u8).to_wire(buff),
            0xFD..=0xFFFF => {
                0xFDu8.to_wire(buff)?;
                (self.value as u16).to_wire(buff)
            }
            0x10000..=0xFFFFFFFF => {
                0xFEu8.to_wire(buff)?;
                (self.value as u32).to_wire(buff)
            }
            _ => {
                0xFFu8.to_wire(buff)?;
                (self.value as u64).to_wire(buff)
            }
        }
    }
}
