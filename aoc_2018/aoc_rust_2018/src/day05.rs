use pyo3::pyfunction;

// 2018 day 5, utility function in Rust
#[pyfunction]
pub fn run_polymerization<'a>(input: Vec<u8>) -> usize {
    let mut v = Vec::new();
    for &c in input.iter() {
        match v.last() {
            None => v.push(c),
            Some(&d) => {
                if d.to_ascii_lowercase() == c.to_ascii_lowercase() && d != c {
                    v.pop();
                } else {
                    v.push(c);
                }
            }
        }
    }
    v.len()
}
