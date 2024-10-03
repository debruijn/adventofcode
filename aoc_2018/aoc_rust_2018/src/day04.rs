use counter::Counter;
use defaultmap::DefaultHashMap;
use pyo3::pyfunction;
use std::collections::HashMap;

fn most_sleepy_part_1(count_asleep: &HashMap<isize, Counter<isize>>) -> isize {
    // Part 1
    let most_sleepy_guard = count_asleep
        .keys()
        .into_iter()
        .max_by_key(|x| count_asleep[x].total::<usize>())
        .unwrap();
    let most_sleepy_minute = count_asleep[most_sleepy_guard].k_most_common_ordered(1)[0].0;
    most_sleepy_guard * most_sleepy_minute
}

fn most_sleepy_part_2(count_asleep: &HashMap<isize, Counter<isize>>) -> isize {
    // Part 1
    let most_sleepy_guard = count_asleep
        .keys()
        .into_iter()
        .max_by_key(|x| count_asleep[x].k_most_common_ordered(1)[0].1)
        .unwrap();
    let most_sleepy_minute = count_asleep[most_sleepy_guard].k_most_common_ordered(1)[0].0;

    most_sleepy_guard * most_sleepy_minute
}

fn row_to_minute(row: &str) -> isize {
    row.split("]")
        .next()
        .unwrap()
        .split(" ")
        .last()
        .unwrap()
        .split(":")
        .last()
        .unwrap()
        .parse()
        .expect("Should be integer from input format")
}

// 2018 day 4 in Rust
#[pyfunction]
pub fn get_most_sleepy_guards(mut input: Vec<String>, sorted: bool) -> (isize, isize) {
    if !sorted {
        input.sort();
    }

    let mut count_asleep: DefaultHashMap<isize, Counter<isize>> = DefaultHashMap::default();
    let mut curr_guard = -9999;
    let mut start_sleep = 0;

    for row in input.iter() {
        if row.ends_with("begins shift") {
            curr_guard = row[row.find("#").unwrap() + 1..]
                .split(" ")
                .next()
                .unwrap()
                .parse()
                .expect("Should be integer from input format");
        } else if row.ends_with("falls asleep") {
            start_sleep = row_to_minute(row);
        } else {
            let end_sleep = row_to_minute(row);
            let this_nap = (start_sleep..end_sleep).collect::<Counter<_>>();
            count_asleep[curr_guard].extend(this_nap);
        }
    }

    let count_asleep: HashMap<isize, Counter<isize>> = HashMap::from(count_asleep);
    (
        most_sleepy_part_1(&count_asleep),
        most_sleepy_part_2(&count_asleep),
    )
}

pub fn run(input: Vec<String>) -> (String, String) {
    let res = get_most_sleepy_guards(input, false);
    (format!("{}", res.0), format!("{}", res.1))
}