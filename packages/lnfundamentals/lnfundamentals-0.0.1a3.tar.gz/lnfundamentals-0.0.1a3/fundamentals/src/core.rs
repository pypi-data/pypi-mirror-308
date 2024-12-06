//! core API of the lnspec crater.
use std::io;
use std::io::{Read, Write};

/// trait that implement the logic
/// to encode a type into the lightning
/// network wire protocol.
pub trait ToWire {
    fn to_wire<W: Write>(&self, buff: &mut W) -> io::Result<()>;
}

/// trait that implement the logic
/// to decode a type from a network
/// wire protocol.
pub trait FromWire: Sized {
    fn from_wire<R: Read>(buff: &mut R) -> io::Result<Self>;
}
