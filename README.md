# adventofcode

This is the repository of Bert de Bruijn for the Advent of Code challenges (https://adventofcode.com).

The goal of this repo is to have the solutions to the puzzles in here, for all years, and making use of locally cached
data that has been pulled from the server using authentication and the aocd package 
(https://github.com/wimglenn/advent-of-code-data)

## Status per year
- 2015: To Do
- 2016: To Do
- 2017: To Do
- 2018: Doing
- 2019: Done
- 2020: Done
- 2021: Done (except for using aocd)
- 2022: Done (except for using aocd)
- 2023: Done

## General todo's
Outside simply doing the coding challenges, I might want to come back to these when all has been done to:
- Automatically pull and cache data - to avoid committing data to the repo but still use it everywhere (ongoing process)
- Improve run time: ideally they all run under 1 sec per day and under 10 secs per year
- More utility functions for common operations or data structures
- Redo days that use numpy without numpy such that I can leverage pypy more
- Combining previous 2: create numpy-replacing utility functions in pure python
- Redo days in other languages I might want to learn, like Rust or Go
