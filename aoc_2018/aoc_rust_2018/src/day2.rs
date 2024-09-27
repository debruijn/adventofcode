use pyo3::pyfunction;
use std::collections::HashMap;
use itertools::Itertools;

// 2018 day 2 part 1 utility function
#[pyfunction]
fn get_box_checksums<'a>(input: Vec<String>) -> isize {
    let mut count2 = 0;
    let mut count3 = 0;

    for str in input.into_iter() {
        let mut char_counts: HashMap<char,i32> = HashMap::new();
        for c in str.chars() {
            *char_counts.entry(c).or_insert(0) += 1;
        }
        count2 += if char_counts.values().any(|&val| val == 2) {1} else {0};
        count3 += if char_counts.values().any(|&val| val == 3) {1} else {0};
    }
    count2 * count3
}

// 2018 day 2 part2 utility function
#[pyfunction]
fn get_correct_box_ids<'a>(input: Vec<String>) -> String {
    for str in input.into_iter().combinations(2) {
        let mut count_diff = 0;
        for (i, c1) in str[0].chars().enumerate() {
            let this = str[1].chars().nth(i).unwrap();
            count_diff += if this.eq(&c1) { 0 } else { 1 };
            if count_diff >= 2 { break };
        }
        if count_diff == 1 {
            let mut res = String::from("");
            for (i, c1) in str[0].chars().enumerate() {
                let this = str[1].chars().nth(i).unwrap();
                if this.eq(&c1) { res += &c1.to_string() }
            }
            return res
        }
    }
    "".to_string()
}

// 2018 day 2 together
#[pyfunction]
pub fn get_box_checksum_and_correct_id<'a>(input: Vec<String>) -> (isize, String) {
    (get_box_checksums(input.clone()), get_correct_box_ids(input))
}