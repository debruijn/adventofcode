use pyo3::pyfunction;
use std::collections::HashSet;

// 2018 day 1 part 2 utility function
#[pyfunction]
pub fn get_frequency_shifts<'a>(input: Vec<isize>) -> isize {
    let mut curr_freq = 0;
    let mut freqs = HashSet::new();
    for c in input.into_iter().cycle() {
        curr_freq += c;
        if freqs.contains(&curr_freq) {
            break;
        } else {
            freqs.replace(curr_freq);
        }
    }
    curr_freq
}

#[pyfunction]
pub fn get_frequency_shifts_raw_input<'a>(input: String) -> isize {
    let v = input.split(", ").map(|d| d.parse::<isize>().unwrap());
    let mut curr_freq = 0;
    let mut freqs = HashSet::new();
    for c in v.into_iter().cycle() {
        curr_freq += c;
        if freqs.contains(&curr_freq) {
            break;
        } else {
            freqs.replace(curr_freq);
        }
    }
    curr_freq
}
