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

__all__ = ("EnvVariable",)

import abc
import os
from typing import Any


class EnvVariable(abc.ABC):
    """
    base class to extract a variable from env and convert it to some type
    """

    def __init__(self, name: str, default: Any = None) -> None:
        """
        Parameters
        ----------
        name:
            env variable name to be extracted
        default:
            value to be returned if env variable with given name does not exist
        """

        self._name = name
        self._default = default

        self._extracted = os.getenv(self._name, self._default)

    @property
    def value(self) -> str | None:
        """
        property to get a converted value of env variable with the given name
        """

        # ignore convertion if env variable's value is missing
        if self._extracted == self._default:
            return self._extracted

        return self.convert(self._extracted)

    @abc.abstractmethod
    def convert(self, value: str) -> Any:
        raise NotImplementedError()
