use std::collections::HashSet;
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
    Ok(())
}
