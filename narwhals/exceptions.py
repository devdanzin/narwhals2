from __future__ import annotations


class FormattedKeyError(KeyError):
    """KeyError with formatted error message.

    Python's `KeyError` has special casing around formatting
    (see https://bugs.python.org/issue2651). Use this class when the error
    message has newlines and other special format characters.
    Needed by https://github.com/tensorflow/tensorflow/issues/36857.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class ColumnNotFoundError(FormattedKeyError):
    """Exception raised when column name isn't present."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    @classmethod
    def from_missing_and_available_column_names(
        cls, missing_columns: list[str], available_columns: list[str]
    ) -> ColumnNotFoundError:
        message = (
            f"The following columns were not found: {missing_columns}"
            f"\n\nHint: Did you mean one of these columns: {available_columns}?"
        )
        return ColumnNotFoundError(message)


class InvalidOperationError(Exception):
    """Exception raised during invalid operations."""


class InvalidIntoExprError(TypeError):
    """Exception raised when object can't be converted to expression."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    @classmethod
    def from_invalid_type(cls, invalid_type: type) -> InvalidIntoExprError:
        message = (
            f"Expected an object which can be converted into an expression, got {invalid_type}\n\n"
            "Hint: if you were trying to select a column which does not have a string column name, then "
            "you should explicitly use `nw.col`.\nFor example, `df.select(nw.col(0))` if you have a column "
            "named `0`."
        )
        return InvalidIntoExprError(message)