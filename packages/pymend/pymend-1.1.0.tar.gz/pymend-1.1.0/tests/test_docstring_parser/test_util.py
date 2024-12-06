"""Test for utility functions."""

from pymend.docstring_parser.common import DocstringReturns
from pymend.docstring_parser.util import combine_docstrings


def test_combine_docstrings() -> None:
    """Test combine_docstrings wrapper."""

    def fun1(arg_a, arg_b, arg_c, arg_d) -> None:  # noqa: ANN001
        """short_description: fun1.

        :param arg_a: fun1
        :param arg_b: fun1
        :return: fun1
        """
        assert arg_a
        assert arg_b
        assert arg_c
        assert arg_d

    def fun2(arg_b, arg_c, arg_d, arg_e) -> None:  # noqa: ANN001
        """short_description: fun2.

        long_description: fun2

        :param arg_b: fun2
        :param arg_c: fun2
        :param arg_e: fun2
        """
        assert arg_b
        assert arg_c
        assert arg_d
        assert arg_e

    @combine_docstrings(fun1, fun2)
    def decorated1(arg_a, arg_b, arg_c, arg_d, arg_e, arg_f) -> None:  # noqa: ANN001
        """
        :param arg_e: decorated
        :param arg_f: decorated
        """  # noqa: D205
        assert arg_a
        assert arg_b
        assert arg_c
        assert arg_d
        assert arg_e
        assert arg_f

    assert decorated1.__doc__ == (
        "short_description: fun2.\n"
        "\n"
        "long_description: fun2\n"
        "\n"
        ":param arg_a: fun1\n"
        ":param arg_b: fun1\n"
        ":param arg_c: fun2\n"
        ":param arg_e: fun2\n"
        ":param arg_f: decorated\n"
        ":returns: fun1"
    )

    @combine_docstrings(fun1, fun2, exclude=[DocstringReturns])
    def decorated2(arg_a, arg_b, arg_c, arg_d, arg_e, arg_f) -> None:  # noqa: ANN001
        assert arg_a
        assert arg_b
        assert arg_c
        assert arg_d
        assert arg_e
        assert arg_f

    assert decorated2.__doc__ == (
        "short_description: fun2.\n"
        "\n"
        "long_description: fun2\n"
        "\n"
        ":param arg_a: fun1\n"
        ":param arg_b: fun1\n"
        ":param arg_c: fun2\n"
        ":param arg_e: fun2"
    )
