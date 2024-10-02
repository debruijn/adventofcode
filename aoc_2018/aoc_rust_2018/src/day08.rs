use defaultmap::DefaultHashMap;
use pyo3::pyfunction;
use std::collections::HashMap;

// 2018 day 8, utility function in Rust
fn get_metadata_sum<'a>(
    data: &'a [usize],
    nodes: &mut HashMap<usize, Vec<usize>>,
    children: &mut DefaultHashMap<usize, Vec<usize>>,
    mut counter: usize,
    depth: usize,
) -> (usize, usize, &'a [usize], usize) {
    let mut metadata_sum = 0;
    let mut value_vec = Vec::new();
    let this_header = &data[..2];
    let mut data = &data[2..];
    let this_counter = counter;

    for _child in 0..this_header[0] {
        children[this_counter].push(counter + 1);
        let child_res = get_metadata_sum(data, nodes, children, counter + 1, depth + 1);
        metadata_sum += child_res.0;
        value_vec.push(child_res.1);
        data = &*child_res.2;
        counter = child_res.3;
    }

    let this_sum = data[0..this_header[1]].iter().sum();
    let new_vec = vec![this_header[0], this_header[1], this_sum, depth];
    nodes.insert(this_counter, new_vec);
    metadata_sum += this_sum;
    let value = if !value_vec.is_empty() {
        data[..this_header[1]]
            .iter()
            .filter(|x| x <= &&value_vec.len())
            .map(|x| value_vec[x - 1])
            .sum()
    } else {
        this_sum
    };
    data = &data[this_header[1]..];

    (metadata_sum, value, data, counter)
}

#[pyfunction]
pub fn run_process<'a>(data: Vec<usize>) -> (usize, usize, HashMap<usize, Vec<usize>>) {
    let mut nodes = HashMap::new();
    let mut children: DefaultHashMap<usize, Vec<usize>> = DefaultHashMap::default();

    let res = get_metadata_sum(&data, &mut nodes, &mut children, 0, 0);
    (res.0, res.1, nodes)
}
