from steely.plugins.btc import *
from nose.tools import *


def test_percentage_increase():
    data = [
        (100, 100, 0),
        (40, 40, 0),
        (100, 101, 1),
        (100, 99, -1),
        (1000, 1010, 1),
        (1000, 1500, 50),
        (9000, 9, -99.9),
    ]
    for before, after, expected in data:
        yield assert_equal, expected, percentage_increase(before, after)


def test_percentage_string():
    data = [
        (0, "+0%"),
        (1, "+1%"),
        (123, "+123%"),
        (-99, "-99%"),
        (-1122, "-1122%"),
    ]
    for percentage_delta, expected_string in data:
        yield assert_equal, expected_string, percentage_string(percentage_delta)
