use pyo3::prelude::*;


#[pyfunction]
fn run_polymerization<'a>(input: Vec<u8>) -> usize {
    let mut v = Vec::new();
    for &c in input.iter() {
        match v.last() {
            None => v.push(c),
            Some(&d) => if d.to_ascii_lowercase() == c.to_ascii_lowercase() && d != c {
                v.pop();
            } else {
                v.push(c);
            }
        }
    }
    v.len()
}

#[pymodule]
#[pyo3(name="aoc_rust")]
fn aoc_rust_2018(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_polymerization, m)?)?;
    Ok(())
}
