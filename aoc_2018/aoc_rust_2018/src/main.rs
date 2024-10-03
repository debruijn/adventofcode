use clap::Parser;
use std::time::Instant;
use aoc_rust;

/// Search for a pattern in a file and display the lines that contain it.
#[derive(Parser)]
struct Cli {
    #[arg(short, long, default_value_t = 0)]
    day: isize,
}

fn main() {
    let args = Cli::parse();
    if args.day == 0 {
        println!("Please input a number to run..");
        return;
    }
    let before = Instant::now();
    let res = aoc_rust::run(args.day);
    let after = Instant::now();
    println!("{}, {} in {:?}", res.0, res.1, after - before)
}
