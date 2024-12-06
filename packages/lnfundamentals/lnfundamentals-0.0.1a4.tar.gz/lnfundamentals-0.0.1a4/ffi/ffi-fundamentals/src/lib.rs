use pyo3::prelude::*;

use fundamentals::prelude::*;

// For python bindings
/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn libfundamentals(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<bolt1::Init>()?;
    m.add_class::<bolt1::Error>()?;
    m.add_class::<bolt1::Ping>()?;
    m.add_class::<bolt1::Pong>()?;
    m.add_class::<bolt1::Warning>()?;
    Ok(())
}
