"""The loud holes — cites `language/operators.md`, `language/modules-and-imports.md`.

This is the file that justifies the whole track. Where the official sources define no outcome,
the model raises `Unspecified` (or records it in the registry) instead of quietly inheriting
CPython's answer. Each topic asserted here is a Track 2 experiment waiting to be run, and each
must be a key in `UNSPECIFIED_CATALOG`.
"""

import pytest

from tfwrlang.errors import Unspecified, UNSPECIFIED_CATALOG
from conftest import run


def test_non_boolean_truthiness_is_unspecified():
    # operators.md only defines booleans in a condition and never says what a non-boolean means,
    # so the model refuses `if 5:` rather than guessing 5 is truthy.
    with pytest.raises(Unspecified) as exc:
        run("if 5:\n    pass\n")
    assert exc.value.topic == "truthiness"


def test_truthiness_hole_is_recorded_in_the_registry():
    interp = run("", max_loop_iterations=None)  # registry starts empty
    with pytest.raises(Unspecified):
        interp.run_source("while 1:\n    pass\n")
    assert "truthiness" in interp.registry.topics()


def test_import_is_refused_not_faked():
    # modules-and-imports.md: `import` resolves by the game window's name, not a file path. The
    # model has no such name-space, so it refuses rather than invent one.
    with pytest.raises(Unspecified) as exc:
        run("import helpers\n")
    assert exc.value.topic == "module-by-window-name"


def test_short_circuit_choice_is_recorded_when_observable():
    # operators.md never promises short-circuit evaluation. The model picks left-to-right + skip,
    # but records the choice whenever the skipped operand could have had a side effect.
    interp = run(
        "def noisy():\n"
        "    return True\n"
        "x = False and noisy()\n"  # right side skipped, and it is a call
    )
    assert "boolean-short-circuit" in interp.registry.topics()
    assert interp.global_env.get("x") is False


def test_default_argument_timing_is_recorded():
    # functions.md calls `def` an assignment but never pins down *when* a default is evaluated.
    # The model evaluates defaults at call time and records that choice.
    interp = run(
        "def f(a, b=1):\n"
        "    return a + b\n"
        "y = f(10)\n"
    )
    assert interp.global_env.get("y") == 11.0
    assert "default-arg-eval-time" in interp.registry.topics()


def test_every_recorded_topic_is_catalogued():
    # The registry must never record a topic that UNSPECIFIED.md wouldn't document — the two
    # stay in lockstep because both are generated from UNSPECIFIED_CATALOG.
    interp = run(
        "def f(a, b=2):\n"
        "    return b\n"  # calling with b defaulted records default-arg-eval-time
        "z = f(1)\n"
    )
    assert interp.registry.topics()  # at least one hole was recorded
    for topic in interp.registry.topics():
        assert topic in UNSPECIFIED_CATALOG
