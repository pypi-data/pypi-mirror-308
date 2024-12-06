//! lnspec basic block to encode and decode the
//! basics types with rust.
use pyo3::{pymodule, types::{PyModule, PyModuleMethods}, Bound, PyResult};


pub mod bitflag;
pub mod bolt;
pub mod core;
pub mod primitives;
pub mod tlv;
pub mod types;

pub mod prelude {
    pub use crate::bitflag::*;
    pub use crate::bolt::*;
    #[allow(unused_imports)]
    pub use crate::primitives::*;
    pub use crate::tlv::*;
    pub use crate::types::*;

    // FIXME: make this a not std compatible
    #[macro_export]
    macro_rules! error {
    ($($msg:tt)*) => {{
        let msg = format!($($msg)*);
        Err(std::io::Error::new(std::io::ErrorKind::Other, msg))
    }};
}

    pub use error;
}

// For python bindings
/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn fundamentals(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<bolt::bolt1::Init>()?;
    m.add_class::<bolt::bolt1::Error>()?;
    m.add_class::<bolt::bolt1::Ping>()?;
    m.add_class::<bolt::bolt1::Pong>()?;
    m.add_class::<bolt::bolt1::Warning>()?;
    Ok(())
}
