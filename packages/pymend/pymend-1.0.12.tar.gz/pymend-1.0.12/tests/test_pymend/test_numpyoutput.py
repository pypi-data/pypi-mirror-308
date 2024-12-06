"""Integration tests of output to numpy format."""

import re
from pathlib import Path

import pytest

import pymend.pymend as pym
from pymend.types import FixerSettings

CURRENT_DIR = Path(__file__).parent


def absdir(file: str) -> Path:
    """Get absolute path for file.

    Parameters
    ----------
    file : str
        File path

    Returns
    -------
    str
        Absolute path to file
    """
    return CURRENT_DIR / Path(file)


def get_expected_patch(name: str) -> str:
    """Open a patch file, and if found Pymend signature remove the 2 first lines.

    Parameters
    ----------
    name : str
        Name of the patch

    Returns
    -------
    str
        Expected patch as a string.
    """
    try:
        with absdir(f"refs/{name}").open(encoding="utf-8") as file:
            expected_lines = file.readlines()
            if expected_lines[0].startswith("# Patch"):
                expected_lines = expected_lines[2:]
            expected = "".join(expected_lines)
    except Exception as error:  # noqa: BLE001
        pytest.fail(f'Raised exception: "{error}"')
    return expected


def remove_diff_header(diff: str) -> str:
    """Remove header differences from diff.

    Parameters
    ----------
    diff : str
        Diff file to clean.

    Returns
    -------
    str
        Cleaned diff.
    """
    return re.sub(r"(@@.+@@)|(\-\-\-.*)|(\+\+\+.*)", "", diff)


def check_expected_diff(test_name: str) -> None:
    """Check that the patch on source_file equals the expected patch."""
    expected = get_expected_patch(f"{test_name}.py.patch.numpydoc.expected")
    comment = pym.PyComment(
        absdir(f"refs/{test_name}.py"), fixer_settings=FixerSettings()
    )
    result = "".join(comment._docstring_diff())
    assert remove_diff_header(result) == remove_diff_header(expected)


class TestNumpyOutput:
    """Integration tests for numpy style output."""

    def test_positional_only_identifier(self) -> None:
        """Make sure that '/' is parsed correctly in signatures."""
        check_expected_diff("positional_only")

    def test_keyword_only_identifier(self) -> None:
        """Make sure that '*' is parsed correctly in signatures."""
        check_expected_diff("keyword_only")

    def test_returns(self) -> None:
        """Make sure single and multi return values are parsed/produced correctly."""
        check_expected_diff("returns")

    def test_star_args(self) -> None:
        """Make sure that *args are treated correctly."""
        check_expected_diff("star_args")

    def test_starstar_kwargs(self) -> None:
        """Make sure that **kwargs are treated correctly."""
        check_expected_diff("star_star_kwargs")

    def test_module_doc_dot(self) -> None:
        """Make sure missing '.' are added to the first line of module docstring."""
        check_expected_diff("module_dot_missing")

    def test_ast_ref(self) -> None:
        """Bunch of different stuff."""
        check_expected_diff("ast_ref")

    def test_yields(self) -> None:
        """Make sure yields are handled correctly from body."""
        check_expected_diff("yields")

    def test_raises(self) -> None:
        """Make sure raises are handled correctly from body."""
        check_expected_diff("raises")

    def test_skip_overload(self) -> None:
        """Function annotated with @overload should be skipped for DS creation."""
        check_expected_diff("skip_overload_decorator")

    def test_class_body(self) -> None:
        """Correctly parse and compose class from body information."""
        check_expected_diff("class_body")

    def test_quote_default(self) -> None:
        """Test that default values of triple quotes do not cause issues."""
        check_expected_diff("quote_default")

    def test_blank_lines(self) -> None:
        """Test that blank lines are set correctly."""
        expected = get_expected_patch("blank_lines.py.patch.numpydoc.expected")
        comment = pym.PyComment(
            absdir("refs/blank_lines.py"),
            fixer_settings=FixerSettings(force_params=False),
        )
        result = "".join(comment._docstring_diff())
        assert remove_diff_header(result) == remove_diff_header(expected)

    def test_comments_after_docstring(self) -> None:
        """Test that comments after the last line are not removed."""
        check_expected_diff("comments_after_docstring")
