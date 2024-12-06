"""Summarize pymend runs to users."""

from dataclasses import dataclass, field
from enum import Enum

from click import style
from typing_extensions import override

from .output import err, out


class Changed(Enum):
    """Enum for changed status."""

    NO = 0
    YES = 1


class NothingChanged(UserWarning):
    """Raised when reformatted code is the same as source."""


@dataclass
class Report:
    """Provides a reformatting counter. Can be rendered with `str(report)`."""

    check: bool = False
    diff: bool = False
    quiet: bool = False
    verbose: bool = False
    change_count: int = 0
    same_count: int = 0
    failure_count: int = 0
    issue_count: int = 0
    issues: list[str] = field(default_factory=list)

    def done(
        self, src: str, *, changed: Changed, issues: bool, issue_report: str
    ) -> None:
        """Increment the counter for successful reformatting. Write out a message.

        Parameters
        ----------
        src : str
            Source file that was successfully fixed.
        changed : Changed
            Whether the file was changed.
        issues : bool
            Whether the file had any issues.
        issue_report : str
            Issue report for the file at question.
        """
        if issues or changed == Changed.YES:
            self.issue_count += 1
            self.issues.append(issue_report)
            if changed == Changed.YES:
                reformatted = "would reformat" if self.diff else "reformatted"
                self.change_count += 1
            else:
                reformatted = "had issues"
            if self.verbose or not self.quiet:
                out(f"{reformatted} {src}")
        else:
            if self.verbose:
                msg = f"{src} already well formatted, good job."
                out(msg, bold=False)
            self.same_count += 1

    def failed(self, src: str, message: str) -> None:
        """Increment the counter for failed reformatting. Write out a message.

        Parameters
        ----------
        src : str
            File that failed to reformat.
        message : str
            Custom message to output. Should be the reason for the failure.
        """
        err(f"error: cannot format {src}: {message}")
        self.failure_count += 1

    def path_ignored(self, path: str, message: str) -> None:
        """Write out a message if a specific path was ignored.

        Parameters
        ----------
        path : str
            Path that was ignored.
        message : str
            Reason the path was ignored.
        """
        if self.verbose:
            out(f"{path} ignored: {message}", bold=False)

    @property
    def return_code(self) -> int:
        """Return the exit code that the app should use.

        This considers the current state of changed files and failures:
        - if there were any failures, return 123;
        - if any files were changed and --check is being used, return 1;
        - otherwise return 0.

        Returns
        -------
        int
            return code.
        """
        # According to http://tldp.org/LDP/abs/html/exitcodes.html starting with
        # 126 we have special return codes reserved by the shell.
        if self.failure_count:
            return 123

        if self.issue_count and self.check:
            return 1

        return 0

    @override
    def __str__(self) -> str:
        """Render a color report of the current state.

        Use `click.unstyle` to remove colors.

        Returns
        -------
        str
            Pretty string representation of the report.
        """
        if self.diff:
            reformatted = "would be reformatted"
            unchanged = "would be left unchanged"
            failed = "would fail to reformat"
        else:
            reformatted = "reformatted"
            unchanged = "left unchanged"
            failed = "failed to reformat"
        report: list[str] = []
        if self.change_count:
            s = "s" if self.change_count > 1 else ""
            report.append(
                style(f"{self.change_count} file{s} ", bold=True, fg="blue")
                + style(f"{reformatted}", bold=True)
            )
        issue_report = ""
        if self.same_count:
            s = "s" if self.same_count > 1 else ""
            report.append(style(f"{self.same_count} file{s} ", fg="blue") + unchanged)
        if self.failure_count:
            s = "s" if self.failure_count > 1 else ""
            report.append(style(f"{self.failure_count} file{s} {failed}", fg="red"))
        if self.check and self.issue_count:
            s = "s" if self.issue_count > 1 else ""
            report.append(style(f"{self.issue_count} file{s} had issues", fg="red"))
            issue_report = "\n\n" + "\n".join(
                style(msg, fg="red") for msg in self.issues
            )
        return ", ".join(report) + "." + issue_report
