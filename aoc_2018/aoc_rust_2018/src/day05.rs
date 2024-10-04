use itertools::Itertools;
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

pub fn run(input: Vec<String>) -> (String, String) {
    let input = input[0].chars().map(|x| x as u8).collect_vec();
    let res1 = run_polymerization(input.clone());
    let mut res2 = res1.clone();
    for i in 0..26 {
        let char_i = ('A' as u8 + i, 'a' as u8 + i);
        let this_input = input
            .iter()
            .filter(|x| **x != char_i.0 && **x != char_i.1)
            .map(|x| x.to_owned())
            .collect_vec();
        let this_len = run_polymerization(this_input);
        if this_len < res2 {
            res2 = this_len;
        }
    }
    (format!("{}", res1), format!("{}", res2))
}
