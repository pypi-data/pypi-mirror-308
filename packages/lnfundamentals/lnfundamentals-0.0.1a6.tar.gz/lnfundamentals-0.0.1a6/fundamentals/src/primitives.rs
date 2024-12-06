//! lightning network primitives implementation
//! in rust.
use std::io::{Read, Write};
use std::mem::size_of;

use crate::core::{FromWire, ToWire};

/// macros to implement the FromWire and ToWire
/// for the basics types.
///
/// This implementation is inspired from the
/// rust-lightning implementation but it is a little bit
/// improved wit modern rust
///
/// EXPAND
/// ```ignore
///
/// impl ToWire for u8 {
///    fn to_wire<W: Write>(&self, writer: &mut W) -> std::io::Result<()> {
///         writer.write_all(&self.to_be_bytes())
///    }
/// }
///
/// impl FromWire for u8 {
///     fn from_write<R: Read>(&self, reader: &mut R) -> std::io::Result<Self> {
///          const BUFF_SIZE: usize = size_of::<u8>();
///          let mut buff = [0; BUFF_SIZE];
///          let size = buff.read(&mut buff)?;
///          assert_eq!(size, size_of::<u8>());
///          Ok(let res = <u8>::from_be_bytes(buff))
///     }
/// }
/// ````
#[macro_export]
macro_rules! to_wire_type {
    ($ty: ty) => {
        impl ToWire for $ty {
            fn to_wire<W: Write>(&self, buff: &mut W) -> std::io::Result<()> {
                buff.write_all(&self.to_be_bytes())
            }
        }

        impl FromWire for $ty {
            fn from_wire<R: Read>(buff: &mut R) -> std::io::Result<Self> {
                const BUFF_SIZE: usize = size_of::<$ty>();
                let mut tmp_buff = [0; BUFF_SIZE];
                buff.read_exact(&mut tmp_buff)?;
                let value = <$ty>::from_be_bytes(tmp_buff);
                Ok(value)
            }
        }
    };
}

to_wire_type!(u8);
to_wire_type!(u16);
to_wire_type!(u32);
to_wire_type!(u64);
