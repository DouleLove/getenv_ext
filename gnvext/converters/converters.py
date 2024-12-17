"""
The MIT License (MIT)

Copyright (c) 2024-present DouleLove

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__all__ = (
    "StringEnvVariable",
    "IntegerEnvVariable",
    "FloatEnvVariable",
    "BooleanEnvVariable",
    "CollectionEnvVariable",
)

import ast
from contextlib import suppress
from typing import Any, Type

from gnvext.converters.base import EnvVariable as _EnvVariable


class StringEnvVariable(_EnvVariable):
    """
    class to extract env variable as a string
    """

    def convert(self, value: str) -> str:
        return value


class IntegerEnvVariable(_EnvVariable):
    """
    class to extract env variable as an integer
    """

    def convert(self, value: str) -> int:
        return int(value)


class FloatEnvVariable(_EnvVariable):
    """
    class to extract env variable as a floating number
    """

    def convert(self, value: str) -> float:
        return float(value)


class BooleanEnvVariable(_EnvVariable):
    """
    class to extract env variable as a boolean object

    Attributes
    ----------
    truthy_values:
        values to be recognized as truthy
    falsy_values:
        values to be recognized as falsy
    """

    truthy_values = ("TRUE", "True", "true", "T", "t", "1")
    falsy_values = ("FALSE", "False", "false", "F", "f", "0")

    def convert(self, value: str | bool) -> bool:
        cleaned = value.strip()

        if cleaned in self.truthy_values:
            return True
        if cleaned in self.falsy_values:
            return False

        raise ValueError(f'could not convert "{value}" to bool')


class CollectionEnvVariable(_EnvVariable):
    """
    class to extract env variable as a collection

    Attributes
    ----------
    convert_collection_type:
        the type to which the collection should be cast (list by default)
    """

    convert_collection_type: Type = None
    _DEFAULT_CONVERT_COLLECTION_TYPE = list
    _BRACKETS = "{}()[]"

    def convert(self, value: str) -> Any:
        tuple_like_string = self._parse(value)

        # building collection from a cleaned string
        collection = ast.literal_eval(tuple_like_string)

        # convert collection to the expected type and return it
        try:
            return self._to_expected_type(value, collection)
        except ValueError:
            return self._to_determined_type(value, collection)

    def _to_expected_type(self, value: str, collection: tuple[str]) -> Any:
        if self.convert_collection_type == dict:
            return self._try_to_dict(collection)

        try:
            return self.convert_collection_type(collection)
        except TypeError:
            raise ValueError(
                f'Could not convert "{value}" to expected type',
            ) from None

    def _to_determined_type(self, value: str, collection: tuple[str]) -> Any:
        # returning dict if it's possible to convert to dict.
        # Otherwise, ignoring ValueError which is raised by self._try_to_dict()
        with suppress(ValueError):
            return self._try_to_dict(collection)

        as_str = value.strip()

        try:
            # taking first and last chars of stripped string.
            # If they are matching to some of the python types like
            # [], (), {}, then determining the value type from the brackets
            determined_type = type(ast.literal_eval(as_str[0] + as_str[-1]))

            # check that brackets are not "" or something like this,
            # which will also be validly converted to str by ast.literal_eval()
            if determined_type not in (list, tuple, set, dict):
                determined_type = self._DEFAULT_CONVERT_COLLECTION_TYPE
        except (ValueError, SyntaxError, IndexError):
            # ast.literal_eval() raised an error,
            # which means that we could not determine the type of given string,
            # and just convert collection to default convert type
            determined_type = self._DEFAULT_CONVERT_COLLECTION_TYPE

        # {} is recognized as dict by default, but we have already checked
        # that collection is not a dict (with self._try_to_dict()), so
        # out collection is a set
        if determined_type == dict:
            determined_type = set

        return determined_type(collection)

    @staticmethod
    def _try_to_dict(collection: tuple[str]) -> tuple | dict:
        # length of collection must be even to convert it to key-value pairs
        if len(collection) % 2 != 0:
            raise ValueError(f'Could not convert "{collection}" to dict')

        as_dict = {}
        for idx in range(0, len(collection), 2):
            k, v = collection[idx], collection[idx + 1]
            if not k.endswith(":") or v.endswith(":"):
                raise ValueError(f'Could not convert "{collection}" to dict')
            # put key to dict with wrapping quotes removed
            as_dict[k[:-1].strip('"').strip("'")] = v

        return as_dict

    @staticmethod
    def _clean_split(value: str, brackets: str = _BRACKETS) -> list[str]:
        """
        removes brackets, leading and ending spaces and then splits
        """

        no_brackets = value.strip().strip(brackets)
        return no_brackets.split()

    @staticmethod
    def _wrap_with_quotes(value: str) -> str:
        """
        escapes all the quotes in the string
        and then wraps it into double quotes
        """

        value = value.strip().replace("'", "\\'").replace('"', '\\"')

        if value.endswith(","):
            value = value[:-1]

        # escaping quotes with backslashes
        if (
            value.startswith('\\"')
            and value.endswith('\\"')
            or value.startswith("\\'")
            and value.endswith("\\'")
        ) and len(value) != 2:
            value = value[2:-2]

        return f'"{value}"'

    def _parse(self, value: str, brackets: str = _BRACKETS) -> str:
        """
        makes a collection-convertable string from an env variable value
        """

        values = self._clean_split(value, brackets=brackets)

        for idx, v in enumerate(values):
            values[idx] = self._wrap_with_quotes(v)

        # wrap with parenthesis to make it look tuple-like
        value = f'({", ".join(values)},)'
        return value
