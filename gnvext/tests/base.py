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

from __future__ import annotations

__all__ = (
    "EnvVariablesTestSuite",
    "TestData",
)

import os
import unittest
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Type

from gnvext.converters.base import EnvVariable
from gnvext.tests.utils import MISSING


class _TestCaseFactory(unittest.TestCase):

    def __init__(
        self,
        suite: EnvVariablesTestSuite,
        value: str,
        expected: Any,
        default: Any = None,
        context: dict = None,
        *,
        method_name: str = "test_convert",
    ) -> None:
        self._suite = suite
        self._value = value
        self._expected = expected
        self._default = default
        self._context = context if context else {}

        super().__init__(method_name)

    @contextmanager
    def _set_env_var(self, varname: str, value: str = MISSING) -> None:
        """
        contextmanager which sets env variable on enter and removes it on exit

        Parameters
        ----------
        varname:
            new env variable name
        value:
            value of new env variable
        """

        try:
            # skip variable creation if value is missing
            if value is not MISSING:
                os.environ[varname] = value
            yield
        finally:
            if os.environ.get(varname):
                os.environ.pop(varname)

    @staticmethod
    def _get_property_as_callable(cls: Type, prop_name: str) -> Callable:
        """
        gets property by name and makes it callable

        Parameters
        ----------
        cls:
            class to get property from
        prop_name:
            property name
        """

        mro = [cls] + cls.mro()

        for obj in mro:
            if prop_name in obj.__dict__:
                return obj.__dict__[prop_name].__get__

    def test_convert(self) -> None:
        """
        runs TESTCASES of given :class:`EnvVariablesTestSuite` instance
        """

        # call self._set_env_var(), so while test is running
        # env variable with name TEST_ENV_VAR_NAME exists
        with self._set_env_var(self._suite.TEST_ENV_VAR_NAME, self._value):
            converter = self._suite.CLS_TO_TEST(
                self._suite.TEST_ENV_VAR_NAME, self._default
            )

            # passing context into converter instance
            for param, value in self._context.items():
                setattr(converter, param, value)

            # exception class is provided as an expected value
            if isinstance(self._expected, type) and issubclass(
                self._expected, BaseException
            ):
                # unwrap value property to callable
                # and call it with converter argument
                # which is instance to get value from
                return self.assertRaises(
                    self._expected,
                    self._get_property_as_callable(
                        cls=self._suite.CLS_TO_TEST,
                        prop_name="value",
                    ),
                    converter,
                )

            # get converted value and check if it is the same as expected
            self.assertEqual(converter.value, self._expected)


@dataclass
class TestData:
    value: str
    expected: Any
    default: Any = None
    context: dict = field(default_factory=dict)

    def __iter__(self) -> Iterable:
        return iter((self.value, self.expected, self.default, self.context))


class EnvVariablesTestSuite(unittest.TestSuite):
    """
    base class to test a subclass of :class:`EnvVariable`

    Attributes
    ----------
    TEST_ENV_VAR_NAME:
        variable name to be created while test is running
    CLS_TO_TEST:
        subclass of :class:`EnvVariable` to be tested
    TESTCASES:
        collection which contains tests data to be passed
        into each test case sequentially.
        Test data must look like [Value, Expected, Default]
        where Value is a value of env variable with TEST_ENV_VAR_NAME name,
        Expected is a value which should be gotten after convert,
        Default is a value to be returned is Value param is :class:`MISSING`
    """

    TEST_ENV_VAR_NAME: str = "__TEST_ENV_VAR__"
    CLS_TO_TEST: Type[EnvVariable] = ...
    TESTCASES: Iterable[TestData] = ...

    def _make_tests(self) -> None:
        for testdata in map(lambda td: TestData(*td), self.TESTCASES):
            testcase = _TestCaseFactory(
                suite=self,
                value=testdata.value,
                expected=testdata.expected,
                default=testdata.default,
                context=testdata.context,
            )
            self.addTest(testcase)

    def run(
        self, result: unittest.TestResult, debug: bool = False
    ) -> unittest.TestResult:
        """
        creates tests from given TESTCASES and runs them separately
        """

        self._make_tests()
        return super().run(result, debug)
