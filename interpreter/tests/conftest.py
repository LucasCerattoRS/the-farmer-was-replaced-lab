"""Test harness for the reference model.

Puts the `interpreter/` directory on `sys.path` so `import tfwrlang` works without installing
anything, and exposes one small helper, `run(src, ...)`, that every test drives the model
through. Each test file names the `language/` page whose claim it pins down — the model exists
to make those prose claims executable, so a test that doesn't cite a page is testing nothing the
docs promised.
"""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
INTERPRETER = os.path.dirname(HERE)
sys.path.insert(0, INTERPRETER)

from tfwrlang.interp import Interpreter  # noqa: E402


def run(src, **kwargs):
    """Execute `src` and hand back the finished interpreter, so a test can read `.global_env`,
    `.output` and `.registry`. Every loop is bounded by default (`max_loop_iterations=10_000`)
    so a broken `break` fails the test fast instead of hanging the run; pass it explicitly to
    override."""
    kwargs.setdefault("max_loop_iterations", 10_000)
    interp = Interpreter(**kwargs)
    interp.run_source(src)
    return interp


@pytest.fixture
def run_():
    return run
