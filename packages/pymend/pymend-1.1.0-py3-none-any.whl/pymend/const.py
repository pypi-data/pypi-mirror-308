"""Constant value used across pymend."""

import re

DEFAULT_EXCLUDES = re.compile(
    r"/(\.direnv|\.eggs|\.git|\.hg|\.ipynb_checkpoints|\.mypy_cache|\.nox|\.pytest_cache|\.ruff_cache|\.tox|\.svn|\.venv|\.vscode|__pypackages__|_build|buck-out|build|dist|venv)/"  # pylint: disable=line-too-long
)
DEFAULT_DESCRIPTION = "_description_"
DEFAULT_TYPE = "_type_"
DEFAULT_SUMMARY = "_summary_."
DEFAULT_EXCEPTION = "__UnknownError__"

ARG_TYPE_SET = "Parameter had type despite `force-arg-types=False` being set."
RETURN_TYPE_SET = (
    "Return type was specified despite `force-return-type=False` being set."
)
ATTRIBUTE_TYPE_SET = (
    "Attribute had type despite `force-attribute-types=False` being set."
)
