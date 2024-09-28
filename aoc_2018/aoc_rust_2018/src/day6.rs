use std::thread;
use std::sync::{Arc, Mutex};
use pyo3::pyfunction;
use num::complex::Complex;
use num::ToPrimitive;

fn get_dist_shift(dist: isize, pt: Complex<isize>) -> Vec<Complex<isize>> {
    let mut points: Vec<Complex<isize>> = Vec::new();
    points.extend((0..(dist+1)).map(|x| pt + Complex::new(x, dist - x)));
    points.extend((0..dist).map(|x| pt + Complex::new(x, x - dist)));
    points.extend((1..(dist+1)).map(|x| pt + Complex::new(-1*x, dist - x)));
    points.extend((1..dist).map(|x| pt + Complex::new(-1*x, x - dist)));

    points
}


// 2018 day 6, utility function in Rust for part 1
fn find_max_numbers<'a>(cands: Vec<Complex<isize>>, all_pts: Vec<Complex<isize>>) -> isize {
    // Target variable
    let mut max_count = 0;

    // For loop could be done distributedly
    for pt in cands.iter() {
        let mut this_count = 1;
        let mut this_dist = 0;
        let mut curr_count = 1;
        'loop_label: loop {
            this_dist += 1;
            let pts_at_dist = get_dist_shift(this_dist, *pt);
            'for_label: for check_pt in pts_at_dist.iter() {
                let check_dist = check_pt.im.abs_diff(pt.im) + check_pt.re.abs_diff(pt.re);
                for other_pt in all_pts.iter().filter(|x| x.ne(&pt)) {
                    let other_dist = check_pt.im.abs_diff(other_pt.im) + check_pt.re.abs_diff(other_pt.re);
                    if other_dist <= check_dist {
                        continue 'for_label
                    }
                }
                curr_count += 1;
            }
            if curr_count == this_count {
                break 'loop_label
            } else {
                this_count = curr_count;
            }
        }
        if curr_count > max_count {
            max_count = curr_count;
        }
    }
    max_count
}

// 2018 day 6, utility function in Rust for part 2
fn find_region_size<'a>(all_pts: &Vec<Complex<isize>>, bound: usize) -> isize {
    // Convert input to vectors of complex numbers since Maturin could not do that

    let center: Complex<isize> = all_pts.iter().sum::<Complex<isize>>() / all_pts.len() as isize;
    let mut this_count = 1;
    let mut this_dist = 0;
    let mut curr_count = 1;
    loop {
        this_dist +=1;
        let pts_at_dist = get_dist_shift(this_dist, center);
        for check_pt in pts_at_dist.iter() {
            let total_dist = all_pts.iter()
                .map(|pt| check_pt.im.abs_diff(pt.im) + check_pt.re.abs_diff(pt.re))
                .sum::<usize>();
            if total_dist < bound {
                curr_count += 1
            }
        }
        if curr_count == this_count {
            break
        } else {
            this_count = curr_count;
        }
    }
    curr_count
}

#[pyfunction]
pub fn find_max_nrs_and_region_size<'a>(cands: Vec<(isize, isize)>,
                                        all_pts: Vec<(isize, isize)>,
                                        bound: usize, do_parallel: bool) -> (isize, isize) {
    // Convert input to vectors of complex numbers since Maturin could not do that
    let cands: Vec<Complex<isize>> = cands.iter().
        map(|x| Complex::new(x.0, x.1)).collect();
    let all_pts: Vec<Complex<isize>> = all_pts.iter().
        map(|x| Complex::new(x.0, x.1)).collect();

    // Answers per part
    let part2 = find_region_size(&all_pts, bound);
    let part1 = if do_parallel {
        find_max_numbers_concurrently(cands, all_pts)
    } else {
        find_max_numbers(cands, all_pts)
    };
    (part1, part2)
}

fn find_max_numbers_concurrently<'a>(cands: Vec<Complex<isize>>,
                                     all_pts: Vec<Complex<isize>>) -> isize {
    // Target variable
    let counts = Arc::new(Mutex::new(Vec::new()));
    let mut handles = Vec::new();

    // For loop could be done distributedly
    for pt in cands.iter() {
        let pt = pt.clone();
        let this_all_pts = all_pts.clone();
        let counts_shared = Arc::clone(&counts);
        let handle = thread::spawn(move || {
            let mut this_count = 1;
            let mut this_dist = 0;
            let mut curr_count = 1;
            'loop_label: loop {
                this_dist += 1;
                let pts_at_dist = get_dist_shift(this_dist, pt);
                'for_label: for check_pt in pts_at_dist.iter() {
                    let check_dist = check_pt.im.abs_diff(pt.im) + check_pt.re.abs_diff(pt.re);
                    for other_pt in this_all_pts.iter().filter(|x| x.ne(&&pt)) {
                        let other_dist = check_pt.im.abs_diff(other_pt.im) + check_pt.re.abs_diff(other_pt.re);
                        if other_dist <= check_dist {
                            continue 'for_label
                        }
                    }
                    curr_count += 1;
                }
                if curr_count == this_count {
                    break 'loop_label
                } else {
                    this_count = curr_count;
                }
            }
            counts_shared.lock().unwrap().push(curr_count)
            }
        );
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
    }

    let ans= counts.lock().unwrap().iter().max().unwrap().to_isize().unwrap();
    ans
}