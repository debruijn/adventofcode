use itertools::Itertools;
use pyo3::pyfunction;
use std::collections::HashMap;

// 2018 day 3
#[pyfunction]
pub fn process_contested_claims<'a>(input: Vec<[i16; 5]>) -> (usize, i16) {
    // For both parts: construct count of claims for each (r, c) coordinate
    let mut counts = HashMap::new();
    for claim in &input {
        for r in claim[1]..claim[1] + claim[3] {
            for c in claim[2]..claim[2] + claim[4] {
                let this_count: &mut i64 = counts.entry((r, c)).or_insert(0);
                *this_count += 1;
            }
        }
    }

    // Part 1: count the coordinates with more than 1 claim
    let mut count_contested_claims = 0;
    for count in counts.values() {
        if *count > 1 {
            count_contested_claims += 1;
        }
    }

    // Part 2: find the index of the claim without any (r, c) coordinates with a count larger than 1
    'for_claim: for claim in input {
        for r in claim[1]..claim[1] + claim[3] {
            for c in claim[2]..claim[2] + claim[4] {
                if counts[&(r, c)] > 1 {
                    continue 'for_claim;
                }
            }
        }
        return (count_contested_claims, claim[0]);
    }
    (count_contested_claims, 0)
}

fn get_claim(input: &str) -> [i16; 5] {
    let input = input.split(' ').collect_vec();

    let locs: Vec<i16> = input[2]
        .replace(':', "")
        .split(',')
        .map(|x| x.parse::<i16>().unwrap())
        .collect_vec();
    let dims: Vec<i16> = input[3]
        .split('x')
        .map(|x| x.parse::<i16>().unwrap())
        .collect_vec();
    let out: [i16; 5] = [
        input[0][1..].parse().unwrap(),
        locs[0],
        locs[1],
        dims[0],
        dims[1],
    ];
    out
}

pub fn run(input: Vec<String>) -> (String, String) {
    let input = input.iter().map(|x| get_claim(x)).collect_vec();
    let res = process_contested_claims(input);
    (format!("{}", res.0), format!("{}", res.1))
}
