from aoc_2020 import aoc_9, aoc_10, aoc_11, aoc_12, aoc_13, aoc_14
import pytest

import os
os.chdir('../../aoc_2020')


@pytest.mark.parametrize("day,expected_test,expected_actual",
                         [(aoc_9, [(127, 62)], (138879426, 23761694)),
                          (aoc_10, [(35, 8), (220, 19208)], (2470, 1973822685184)),
                          (aoc_11, [(37, 26)], (2386, 2091)),
                          (aoc_12, [(25, 286)], (998, 71586)),
                          (aoc_13, [(295, 1068781), (130, 3417), (295, 754018), (295, 779210), (295, 1261476),
                                    (47, 1202161486)], (3215, 1001569619313439)),
                          (aoc_14, [(165, 'Not feasible'), (51, 208)], (15919415426101, 3443997590975))],
                         ids=["aoc_9", "aoc_10", "aoc_11", "aoc_12", "aoc_13", "aoc_14"])
def test_answers(day, expected_test, expected_actual):
    for test_nr in range(len(expected_test)):
        assert day.run_all(test_nr+1)[:2] == expected_test[test_nr]
    assert day.run_all(0)[:2] == expected_actual
