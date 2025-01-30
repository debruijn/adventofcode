# adventofcode

This is the repository of Bert de Bruijn for the Advent of Code challenges (https://adventofcode.com).

The goal of this repo is to have the solutions to the puzzles in here, for all years, and making use of locally cached
data that has been pulled from the server using authentication and the aocd package 
(https://github.com/wimglenn/advent-of-code-data)

The majority of the work will be done in (pure) Python, except for the first few years I participated (2021/2022) when
I was still using numpy and pandas a lot (which is fine, it is just not my goal anymore; I want to make it work 
without external packages for pypy).

Next to this I also want to start experimenting more with using Rust for key performance bottlenecks from within Python.
An early example of this can be found in the aoc_2018 folder.

## Status per year
- 2015: Done
- 2016: Done
- 2017: Done
- 2018: Done
- 2019: Done
- 2020: Done
- 2021: Done (except for using aocd)
- 2022: Done (except for using aocd)
- 2023: Done
- 2024: Done

## General todo's
Outside simply doing the coding challenges in a reasonable run time, you can (but might not) find other commits as well:
- Improve run time: ideally they all run under 1 sec per day and under 10 secs per year
- More utility functions for common operations or data structures
- Redo days from 2021/2022 that use numpy without numpy
- Redo (more) days in other languages I might want to learn, like Rust or Go, or calling those implementations in Python
  - While I might still add more experimentation for calling another language from Python, my general AoC work in other
  languages will now be in a new repo: [more-adventofcode](https://github.com/debruijn/more-adventofcode).
