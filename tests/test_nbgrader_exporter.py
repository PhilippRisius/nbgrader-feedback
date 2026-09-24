"""Tests for the nbgrader export helpers."""

import json
import pathlib

import nbgrader.api
import pytest

from nbgrader_feedback.report_creation import nbgrader_exporter


EXAMPLE = pathlib.Path(__file__).parent / "fixtures" / "example"


@pytest.fixture
def gradebook():
    with nbgrader.api.Gradebook(f"sqlite:///{EXAMPLE / 'gradebook.db'}") as gb:
        yield gb


@pytest.fixture
def write_config(tmp_path):
    def _write(config):
        path = tmp_path / "config.json"
        path.write_text(json.dumps(config))
        return path

    return _write


@pytest.mark.parametrize("missing_ok", [True, False])
def test_export_to_multiindex(gradebook, missing_ok):
    table = nbgrader_exporter.export_to_multiindex(gradebook, gradebook.students, gradebook.assignments, missing_ok)

    assert set(table.columns) == {"0", "1", "2", "reachable"}
    assert table.index.names == ["Assignment", "Task", "Cell"]
    assert table["reachable"].sum() == 6
    assert table["0"].sum() == 6
    assert table["1"].sum() == 0
    # student "2" has no submission
    assert table["2"].isna().all()


@pytest.mark.parametrize("missing_ok", [True, False])
def test_has_entry_notebook(gradebook, missing_ok):
    assignment = gradebook.find_assignment("example_task")
    notebook = assignment.notebooks[0]
    student = gradebook.find_student("0")

    assert nbgrader_exporter.has_entry(gradebook, assignment, missing_ok, student, notebook)


def test_has_entry_missing_submission(gradebook):
    assignment = gradebook.find_assignment("example_task")
    student = gradebook.find_student("2")

    assert nbgrader_exporter.has_entry(gradebook, assignment, True, student)
    assert not nbgrader_exporter.has_entry(gradebook, assignment, False, student)


def test_read_config_minimal(write_config):
    config = nbgrader_exporter.read_config(write_config({}))

    assert config["feedback"] == {"attach": False}
    assert config["grading"] == {"default_admission": True}


@pytest.mark.parametrize(
    ("percentage", "grade"),
    [(0, "F"), (4.9, "F"), (5, "E"), (9, "E"), (12, "D"), (99, "C"), (100, "B"), (-1, "F")],
)
def test_percentage_to_grade_numeric_order(write_config, percentage, grade):
    # keys of differing length expose lexicographic comparison ("5" > "10" > "100")
    table = {"0": "F", "5": "E", "10": "D", "50": "C", "100": "B"}
    config = nbgrader_exporter.read_config(
        write_config({"feedback": {}, "grading": {"points_100_percent": 10, "points_needed": 5, "percentage_to_grade": table}})
    )

    assert config["grading"]["percentage_to_grade"](percentage) == grade


def test_csv_exporter_defaults():
    assert nbgrader_exporter.CSVExporter.missing_ok is True
    assert nbgrader_exporter.CSVExporter.aggregated is False
