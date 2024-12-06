"""All exceptions used in the instigator_py code base are defined here."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jinja2 import TemplateError


class instigator_pyException(Exception):
    """
    Base exception class.

    All instigator_py-specific exceptions should subclass this class.
    """


class NonTemplatedInputDirException(instigator_pyException):
    """
    Exception for when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(instigator_pyException):
    """
    Exception for ambiguous project template directory.

    Raised when instigator_py cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

    # unused locally


class MissingProjectDir(instigator_pyException):
    """
    Exception for missing generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """

    # unused locally


class ConfigDoesNotExistException(instigator_pyException):
    """
    Exception for missing config file.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(instigator_pyException):
    """
    Exception for invalid configuration file.

    Raised if the global configuration file is not valid YAML or is
    badly constructed.
    """


class UnknownRepoType(instigator_pyException):
    """
    Exception for unknown repo types.

    Raised if a repo's type cannot be determined.
    """


class VCSNotInstalled(instigator_pyException):
    """
    Exception when version control is unavailable.

    Raised if the version control system (git or hg) is not installed.
    """


class ContextDecodingException(instigator_pyException):
    """
    Exception for failed JSON decoding.

    Raised when a project's JSON context file can not be decoded.
    """


class OutputDirExistsException(instigator_pyException):
    """
    Exception for existing output directory.

    Raised when the output directory of the project exists already.
    """


class EmptyDirNameException(instigator_pyException):
    """
    Exception for a empty directory name.

    Raised when the directory name provided is empty.
    """


class InvalidModeException(instigator_pyException):
    """
    Exception for incompatible modes.

    Raised when instigator_py is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class FailedHookException(instigator_pyException):
    """
    Exception for hook failures.

    Raised when a hook script fails.
    """


class UndefinedVariableInTemplate(instigator_pyException):
    """
    Exception for out-of-scope variables.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(
        self, message: str, error: TemplateError, context: dict[str, Any]
    ) -> None:
        """Exception for out-of-scope variables."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self) -> str:
        """Text representation of UndefinedVariableInTemplate."""
        return (
            f"{self.message}. "
            f"Error message: {self.error.message}. "
            f"Context: {self.context}"
        )


class UnknownExtension(instigator_pyException):
    """
    Exception for un-importable extension.

    Raised when an environment is unable to import a required extension.
    """


class RepositoryNotFound(instigator_pyException):
    """
    Exception for missing repo.

    Raised when the specified instigator_py repository doesn't exist.
    """


class RepositoryCloneFailed(instigator_pyException):
    """
    Exception for un-cloneable repo.

    Raised when a instigator_py template can't be cloned.
    """


class InvalidZipRepository(instigator_pyException):
    """
    Exception for bad zip repo.

    Raised when the specified instigator_py repository isn't a valid
    Zip archive.
    """
