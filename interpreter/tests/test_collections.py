"""Collections — cites `language/collections.md` and `api/reference.md`.

Lists, dicts, sets and tuples, and the exact set of mutating methods the documented subset
provides (`append`, `insert`, `pop`, `remove`, `add`). A method outside that set is a
`NotSupported`, not a silent pass-through to Python.
"""

import pytest

from tfwrlang.errors import NotSupported, TfwrRuntimeError
from conftest import run


def test_list_indexing_and_mutation():
    interp = run(
        "xs = [10, 20, 30]\n"
        "xs[1] = 99\n"
        "first = xs[0]\n"
    )
    assert interp.global_env.get("xs") == [10.0, 99.0, 30.0]
    assert interp.global_env.get("first") == 10.0


def test_documented_list_methods():
    interp = run(
        "xs = [1]\n"
        "xs.append(2)\n"
        "xs.insert(0, 0)\n"
        "last = xs.pop()\n"
        "xs.remove(1)\n"
    )
    assert interp.global_env.get("xs") == [0.0]
    assert interp.global_env.get("last") == 2.0


def test_undocumented_method_is_refused():
    # `sort` exists in Python but is not in the documented collection API — the model refuses it
    # rather than silently borrowing Python's implementation.
    with pytest.raises(NotSupported, match="sort"):
        run("xs = [3, 1, 2]\nxs.sort()\n")


def test_dict_lookup_and_missing_key():
    interp = run('d = {"a": 1}\nv = d["a"]\n')
    assert interp.global_env.get("v") == 1.0
    with pytest.raises(TfwrRuntimeError, match="not in dictionary"):
        run('d = {"a": 1}\nx = d["b"]\n')


def test_set_add_and_membership():
    interp = run(
        "s = {1, 2}\n"
        "s.add(3)\n"
        "has = 3 in s\n"
    )
    assert interp.global_env.get("has") is True


def test_tuples_are_immutable():
    with pytest.raises(TfwrRuntimeError, match="immutable"):
        run("t = (1, 2)\nt[0] = 9\n")


def test_tuple_unpacking_assignment():
    interp = run("a, b = (1, 2)\n")
    assert interp.global_env.get("a") == 1.0
    assert interp.global_env.get("b") == 2.0
