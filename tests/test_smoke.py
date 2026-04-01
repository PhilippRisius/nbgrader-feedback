"""Smoke tests — verify the package imports and exposes its public API."""

import nbgrader_feedback


def test_version():
    assert isinstance(nbgrader_feedback.__version__, str)
    assert nbgrader_feedback.__version__ != ""


def test_all_exports_importable():
    for name in nbgrader_feedback.__all__:
        assert hasattr(nbgrader_feedback, name), f"{name!r} listed in __all__ but not importable"
