use pyo3::prelude::*;
mod util;

mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day08;
mod day09;
mod day10;
mod day14;

#[pymodule]
#[pyo3(name = "aoc_rust")]
pub fn aoc_rust_2018(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(day01::get_frequency_shifts, m)?)?;
    m.add_function(wrap_pyfunction!(day01::get_frequency_shifts_raw_input, m)?)?;
    // m.add_function(wrap_pyfunction!(day2::get_box_checksums, m)?)?;
    // m.add_function(wrap_pyfunction!(day2::get_correct_box_ids, m)?)?;
    m.add_function(wrap_pyfunction!(day02::get_box_checksum_and_correct_id, m)?)?;
    m.add_function(wrap_pyfunction!(day03::process_contested_claims, m)?)?;
    m.add_function(wrap_pyfunction!(day04::get_most_sleepy_guards, m)?)?;
    m.add_function(wrap_pyfunction!(day05::run_polymerization, m)?)?;
    m.add_function(wrap_pyfunction!(day06::find_max_nrs_and_region_size, m)?)?;
    // m.add_function(wrap_pyfunction!(day6::find_region_size, m)?)?;

    m.add_function(wrap_pyfunction!(day08::run_process, m)?)?;
    m.add_function(wrap_pyfunction!(day09::find_winning_score, m)?)?;
    m.add_function(wrap_pyfunction!(day10::find_message_in_the_sky, m)?)?;

    m.add_function(wrap_pyfunction!(day14::find_recipe, m)?)?;
    Ok(())
}

pub fn run(day: isize) -> (String, String) {
    let input_str = util::read_input(2018, day);
    let res = match day {
        2 => day02::run(input_str),
        4 => day04::run(input_str),
        5 => day05::run(input_str),
        _ => (String::from("To do.."), String::new())
    };
    res
}