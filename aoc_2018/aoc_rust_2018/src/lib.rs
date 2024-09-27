use pyo3::prelude::*;

mod day1;
mod day2;
mod day3;
mod day5;
mod day14;


#[pymodule]
#[pyo3(name="aoc_rust")]
fn aoc_rust_2018(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(day1::get_frequency_shifts, m)?)?;
    m.add_function(wrap_pyfunction!(day1::get_frequency_shifts_raw_input, m)?)?;
    // m.add_function(wrap_pyfunction!(day2::get_box_checksums, m)?)?;
    // m.add_function(wrap_pyfunction!(day2::get_correct_box_ids, m)?)?;
    m.add_function(wrap_pyfunction!(day2::get_box_checksum_and_correct_id, m)?)?;
    m.add_function(wrap_pyfunction!(day3::process_contested_claims, m)?)?;

    m.add_function(wrap_pyfunction!(day5::run_polymerization, m)?)?;

    m.add_function(wrap_pyfunction!(day14::find_recipe, m)?)?;
    Ok(())
}
