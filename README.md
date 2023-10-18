# adventofcode

This is the repository of Bert de Bruijn for the Advent of Code challenges (https://adventofcode.com).

The goal of this repo is to have the solutions to the puzzles in here, together with their input. 
Next to this, I plan on adding tests for checking that the solutions give the right answer. These
tests are used to make sure future changes to the shared utility folder don't break older puzzles.

## Status per year
- 2015: To Do
- 2016: To Do
- 2017: To Do
- 2018: To Do
- 2019: To Do
- 2020: Done
- 2021: Done (but will require refactoring and adding tests)
- 2022: Done (but will require adding tests)

## General todo's
Outside simply doing the coding challenges, I want to:
- Improve run time of tests: ideally they all run under 1 sec per day and under 10 secs per year
- Automatically pull and cache data - to avoid committing data to the repo
- More utility functions for common operations or data structures
- Redo days that use numpy without numpy such that I can leverage pypy more
- Combining previous 2: create numpy-replacing utility functions in pure python