use pyo3::pyfunction;

fn get_dist(x: (isize, isize), mean_pos0: f32, mean_pos1: f32) -> f32 {
    ((x.0 as f32 - mean_pos0).powf(2.0) + (x.1 as f32 - mean_pos1).powf(2.0)).powf(0.5)
}

fn get_total_dist(t: &isize, nums: &Vec<[isize; 4]>) -> f32 {
    let pos_t = nums.iter().map(|x| (x[0] + x[2] * t, x[1] + x[3] * t));
    let mean_pos0: f32 =
        nums.iter().map(|x| x[0] + x[2] * t).sum::<isize>() as f32 / nums.len() as f32;
    let mean_pos1: f32 =
        nums.iter().map(|x| x[1] + x[3] * t).sum::<isize>() as f32 / nums.len() as f32;
    pos_t.map(|x| get_dist(x, mean_pos0, mean_pos1)).sum()
}

fn print_pos(t: &isize, nums: &Vec<[isize; 4]>) {
    let pos_t: Vec<(isize, isize)> = nums
        .iter()
        .map(|x| (x[0] + x[2] * t, x[1] + x[3] * t))
        .collect();
    let lims0 = (
        nums.iter().map(|x| x[0] + x[2] * t).min().unwrap(),
        nums.iter().map(|x| x[0] + x[2] * t).max().unwrap(),
    );
    let lims1 = (
        nums.iter().map(|x| x[1] + x[3] * t).min().unwrap(),
        nums.iter().map(|x| x[1] + x[3] * t).max().unwrap(),
    );

    for k in lims1.0..=lims1.1 {
        let mut this_str = Vec::new();
        for i in lims0.0..=lims0.1 {
            this_str.push(if pos_t.contains(&(i, k)) { '#' } else { ' ' })
        }
        println! {"{}", this_str.iter().collect::<String>()}
    }
}

// 2018 day 10, utility function in Rust
#[pyfunction]
pub fn find_message_in_the_sky<'a>(nums: Vec<[isize; 4]>) -> (isize, f32) {
    let mut stepsize = 10000;
    let (mut curr_t, mut curr_dist) = (0, get_total_dist(&0, &nums));
    let (mut last_t, mut last_dist, mut best_t, mut best_dist) =
        (0, get_total_dist(&0, &nums), 0, get_total_dist(&0, &nums));

    // Optimization algorithm that assumes convexity:
    // - Start with a large stepsize and initial t and f(t)
    // - Try new value of t and f(t)
    //      - if better: keep it
    //      - if not: revert to previous, decrease stepsize, and try again
    // We need to revert to previous one because on higher granularity, the better f(t) might be
    // for a t between last_t and curr_t, or between curr_t and new_t.
    while stepsize > 0 {
        let new_t = curr_t + stepsize;
        let new_dist = get_total_dist(&new_t, &nums);
        if new_dist <= curr_dist {
            (last_dist, last_t) = (curr_dist, curr_t);
            (curr_t, curr_dist) = (new_t, new_dist);
        } else {
            (best_dist, best_t) = (curr_dist, curr_t);
            (curr_t, curr_dist) = (last_t, last_dist);
            stepsize = stepsize / 10;
        }
    }
    print_pos(&best_t, &nums);
    (best_t, best_dist)
}
