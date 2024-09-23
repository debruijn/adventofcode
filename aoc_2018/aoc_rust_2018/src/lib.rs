use std::collections::{HashMap, HashSet};
use itertools::Itertools;
use pyo3::prelude::*;


// 2018 day 1 part 2 utility function
#[pyfunction]
fn get_frequency_shifts<'a>(input: Vec<isize>) -> isize {
    let mut curr_freq = 0;
    let mut freqs = HashSet::new();
    for c in input.into_iter().cycle() {
        curr_freq += c;
        if freqs.contains(&curr_freq) {
            break
        } else {
            freqs.replace(curr_freq);
        }
    }
    curr_freq
}

#[pyfunction]
fn get_frequency_shifts_raw_input<'a>(input: String) -> isize {
    let v = input.split(", ").map(|d| d.parse::<isize>().unwrap());
    let mut curr_freq = 0;
    let mut freqs = HashSet::new();
    for c in v.into_iter().cycle() {
        curr_freq += c;
        if freqs.contains(&curr_freq) {
            break
        } else {
            freqs.replace(curr_freq);
        }
    }
    curr_freq
}


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
fn get_box_checksum_and_correct_id<'a>(input: Vec<String>) -> (isize, String) {
    (get_box_checksums(input.clone()), get_correct_box_ids(input))
}


// 2018 day 3
#[pyfunction]
fn process_contested_claims<'a>(input: Vec<[i16;5]>) -> (usize, i16) {
    // For both parts: construct count of claims for each (r, c) coordinate
    let mut counts = HashMap::new();
    for claim in &input {
        for r in claim[1]..claim[1]+claim[3] {
            for c in claim[2]..claim[2]+claim[4] {
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
        for r in claim[1]..claim[1]+claim[3] {
            for c in claim[2]..claim[2]+claim[4] {
                if counts[&(r, c)] > 1 {
                    continue 'for_claim;
                }
            }
        }
        return (count_contested_claims, claim[0])
    }
    (count_contested_claims, 0)
}


// 2018 day 5, utility function in Rust
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

// 2018 day 14, utility function in Rust
#[pyfunction]
fn find_recipe<'a>(input: usize) -> (Vec<usize>, usize) {

    // part 1 in its own namespace
    let part1 = {
        let mut recipes = vec![3, 7];
        let mut p1 = 0;
        let mut p2 = 1;
        let nr_take = 10;
        while recipes.len() < input + nr_take {
            let mut score = recipes[p1] + recipes[p2];

            // Push to recipes for one digit at a time
            if score >= 10 {
                recipes.push(score / 10);
                score %= 10;
            }
            recipes.push(score);

            // New p
            p1 = (p1 + 1 + recipes[p1]) % recipes.len();
            p2 = (p2 + 1 + recipes[p2]) % recipes.len();
        }
        recipes[input..input+nr_take].to_vec()
    };

    // part 2 - can immediately return when answer found
    let mut recipes = vec![3, 7];
    let mut p1 = 0;
    let mut p2 = 1;
    // input as vector in this case
    let input: Vec<usize> = input.to_string().chars().map(|d|
        d.to_digit(10).unwrap() as usize).collect();
    let ans;
    loop {
        let mut score = recipes[p1] + recipes[p2];
        let mut two_digit = false;
        if score >= 10 {
            two_digit = true;
            recipes.push(score / 10);
            score %= 10;
        }
        recipes.push(score);
        p1 = (p1 + 1 + recipes[p1]) % recipes.len();
        p2 = (p2 + 1 + recipes[p2]) % recipes.len();

        let recipe_len = recipes.len();
        let input_len = input.len();
        if recipe_len > input_len {  // can only check when recipe is long enough
            if &recipes[recipe_len - input_len..recipe_len] == input {
                ans = recipe_len - input_len;  // match final il digits
                return (part1, ans);
            }
        }
        if two_digit && recipe_len > input_len + 1 { // different ending possible for two_digit case
            if &recipes[recipe_len - 1 - input_len..recipe_len - 1] == input {
                ans = recipe_len - 1 - input_len;
                return (part1, ans);
            }
        }
    }
}


#[pymodule]
#[pyo3(name="aoc_rust")]
fn aoc_rust_2018(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_polymerization, m)?)?;
    m.add_function(wrap_pyfunction!(find_recipe, m)?)?;
    m.add_function(wrap_pyfunction!(get_frequency_shifts, m)?)?;
    m.add_function(wrap_pyfunction!(get_frequency_shifts_raw_input, m)?)?;
    m.add_function(wrap_pyfunction!(get_box_checksums, m)?)?;
    m.add_function(wrap_pyfunction!(get_correct_box_ids, m)?)?;
    m.add_function(wrap_pyfunction!(get_box_checksum_and_correct_id, m)?)?;
    m.add_function(wrap_pyfunction!(process_contested_claims, m)?)?;
    Ok(())
}
