use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn version() -> PyResult<String> {
    Ok(env!("CARGO_PKG_VERSION").to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn plane_partitions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
