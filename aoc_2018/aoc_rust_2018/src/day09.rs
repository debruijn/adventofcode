use pyo3::pyfunction;
use std::collections::VecDeque;

// 2018 day 9, utility function in Rust
#[pyfunction]
pub fn find_winning_score<'a>(nr_players: usize, last_ball: usize) -> usize {
    let mut circle = VecDeque::from([0]);
    let mut points = vec![0; nr_players];

    for new_ball in 1..=last_ball {
        if new_ball % 23 == 0 {
            circle.rotate_left(7);
            points[new_ball % nr_players] += new_ball + circle.pop_back().unwrap();
        } else {
            if circle.len() >= 2 {
                circle.rotate_right(2);
            }
            circle.push_back(new_ball);
        }
    }

    *points.iter().max().unwrap()
}
