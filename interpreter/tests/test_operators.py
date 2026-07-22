"""Operators and values — cites `language/operators.md` and `language/values-and-variables.md`.

Two model choices worth pinning: numbers are a single float type (there is no separate int in
the documented language), and ordering is defined on numbers only.
"""

import pytest

from tfwrlang.errors import TfwrRuntimeError
from conftest import run


def _val(src_expr):
    return run(f"result = {src_expr}\n").global_env.get("result")


def test_numbers_are_floats():
    # values-and-variables.md: one number type. `range`/`len` yield numbers too, and division
    # never truncates.
    assert _val("7 / 2") == 3.5
    assert _val("len([1, 2, 3])") == 3.0
    assert isinstance(_val("2 + 2"), float)


def test_floor_div_and_power_stay_numbers():
    assert _val("7 // 2") == 3.0
    assert _val("2 ** 10") == 1024.0


def test_ordering_is_numbers_only():
    # operators.md defines `< <= > >=` on numbers; comparing strings with them is a runtime error
    # in this model rather than borrowing Python's lexicographic order.
    assert _val("1 < 2") is True
    with pytest.raises(TfwrRuntimeError, match="ordering"):
        run('x = "a" < "b"\n')


def test_equality_works_across_types_without_ordering():
    # `==`/`!=` are defined for any values; only ordering is restricted.
    assert _val('1 == "1"') is False
    assert _val("2 != 3") is True


def test_string_and_list_concatenation():
    assert _val('"ab" + "cd"') == "abcd"
    assert _val("[1] + [2]") == [1.0, 2.0]


def test_cannot_add_across_types():
    with pytest.raises(TfwrRuntimeError, match="cannot add"):
        run('x = "a" + 1\n')


def test_division_by_zero_is_a_runtime_error():
    with pytest.raises(TfwrRuntimeError, match="division by zero"):
        run("x = 1 / 0\n")


def test_membership_in_collections():
    assert _val("2 in [1, 2, 3]") is True
    assert _val('"k" in {"k": 1}') is True
    assert _val("5 not in [1, 2, 3]") is True
