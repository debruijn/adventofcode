from aoc_2020 import (aoc_1, aoc_2, aoc_3, aoc_4, aoc_5, aoc_6, aoc_7, aoc_8, aoc_9, aoc_10,
                      aoc_11, aoc_12, aoc_13, aoc_14, aoc_15, aoc_16, aoc_17, aoc_18, aoc_19,
                      aoc_20, aoc_21, aoc_22, aoc_23, aoc_24, aoc_25)
import pytest
import os

os.chdir('../../aoc_2020')


@pytest.mark.parametrize("day,expected_test,expected_actual",
                         [(aoc_1, [(514579, 241861950)], (319531, 244300320)),
                          (aoc_2, [(2, 1)], (410, 694)),
                          (aoc_3, [(7, 336)], (276, 7812180000)),
                          (aoc_4, [(2, 2)], (247, 145)),
                          (aoc_5, [(357, "NA"), (567, 'NA'), (119, 'NA'), (820, 'NA')], (970, 587)),
                          (aoc_6, [(6, 3), (11, 6)], (6726, 3316)),
                          (aoc_7, [(4, 32)], (229, 6683)),
                          (aoc_8, [(5, 8)], (1548, 1375)),
                          (aoc_9, [(127, 62)], (138879426, 23761694)),
                          (aoc_10, [(35, 8), (220, 19208)], (2470, 1973822685184)),
                          (aoc_11, [(37, 26)], (2386, 2091)),
                          (aoc_12, [(25, 286)], (998, 71586)),
                          (aoc_13, [(295, 1068781), (169, 3417), (49, 754018), (49, 779210), (49, 1261476),
                                    (1369, 1202161486)], (3215, 1001569619313439)),
                          (aoc_14, [(165, 'Not feasible')], (15919415426101, 3443997590975)),
                          (aoc_15, [([436], [175594])], ([496], [883])),
                          (aoc_16, [(71, 1)], (27870, 3173135507987)),
                          (aoc_17, [(112, 848)], (315, 1520)),
                          (aoc_18, [(71, 231), (51, 51), (26, 46), (437, 1445), (12240, 669060), (13632, 23340)],
                           (4940631886147, 283582817678281)),
                          (aoc_19, [(2, 'Not applicable to this data'), (2, 'Not applicable to this data')],
                           (216, 400)),
                          (aoc_20, [(20899048083289, 273)], (7492183537913, 2323)),
                          (aoc_21, [(5, 'mxmxvkd,sqjhc,fvjkl')],
                           (2428, 'bjq,jznhvh,klplr,dtvhzt,sbzd,tlgjzx,ctmbr,kqms')),
                          (aoc_22, [(306, 291)], (33400, 33745)),
                          (aoc_23, [(67384529, 149245887792)], (97245386, 156180332979)),
                          (aoc_24, [(10, 2208)], (332, 3900)),
                          (aoc_25, [(14897079, "Merry Christmas")], (18293391, "Merry Christmas"))
                          ],
                         ids=["aoc_1", "aoc_2", "aoc_3", "aoc_4", "aoc_5", "aoc_6","aoc_7", "aoc_8", "aoc_9", "aoc_10",
                              "aoc_11", "aoc_12", "aoc_13", "aoc_14", "aoc_15", "aoc_16", "aoc_17", "aoc_18", "aoc_19",
                              "aoc_20", "aoc_21", "aoc_22", "aoc_23", "aoc_24", "aoc_25"])
def test_answers(day, expected_test, expected_actual):
    for test_nr in range(len(expected_test)):
        assert day.run_all(test_nr + 1)[:2] == expected_test[test_nr]
    assert day.run_all(0)[:2] == expected_actual
