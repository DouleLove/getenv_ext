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

__all__ = ()

from gnvext.converters.converters import (
    BooleanEnvVariable,
    CollectionEnvVariable,
    FloatEnvVariable,
    IntegerEnvVariable,
    StringEnvVariable,
)
from gnvext.tests.base import EnvVariablesTestSuite, TestData
from gnvext.tests.utils import MISSING, generic_suite_runner


class TestStringEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = StringEnvVariable
    TESTCASES = [
        TestData("abcd", "abcd"),
        TestData("ab cd", "ab cd"),
        TestData(MISSING, "abcd", "abcd"),
        TestData(MISSING, None),
        TestData(MISSING, 10, 10),
    ]


class TestIntegerEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = IntegerEnvVariable
    TESTCASES = [
        TestData("123", 123),
        TestData("12 34", ValueError),
        TestData("   1234 ", 1234),
        TestData("1234.0", ValueError),
        TestData(MISSING, 1234, 1234),
        TestData(MISSING, None),
        TestData(MISSING, 17.4, 17.4),
    ]


class TestFloatEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = FloatEnvVariable
    TESTCASES = [
        TestData("1234.0", 1234.0),
        TestData("5735.7", 5735.7),
        TestData("123 4.0", ValueError),
        TestData("1234. 4", ValueError),
        TestData("1234", 1234.0),
        TestData(MISSING, 1234.4, 1234.4),
        TestData(MISSING, None),
        TestData(MISSING, 17, 17),
    ]


class TestBooleanEnvVariable(EnvVariablesTestSuite):
    _TRUTHY_VALUES_ATTR_NAME = "truthy_values"
    _FALSY_VALUES_ATTR_NAME = "falsy_values"

    _Tt1_CTX = {_TRUTHY_VALUES_ATTR_NAME: ("TRUE", "True", "true", "1")}
    _t1_CTX = {_TRUTHY_VALUES_ATTR_NAME: ("true", "1")}
    _Yy1_CTX = {_TRUTHY_VALUES_ATTR_NAME: ("Yes", "yes", "1")}

    _Ff0_CTX = {_FALSY_VALUES_ATTR_NAME: ("FALSE", "False", "false", "0")}
    _f0_CTX = {_FALSY_VALUES_ATTR_NAME: ("false", "0")}
    _Nn_CTX = {_FALSY_VALUES_ATTR_NAME: ("No", "no", "0")}

    CLS_TO_TEST = BooleanEnvVariable
    TESTCASES = [
        TestData("True", True),
        TestData("  t", True),
        TestData("1", True),
        TestData("true", True, context=_Tt1_CTX),
        TestData("t", ValueError, context=_Tt1_CTX),
        TestData("yes", True, context=_Yy1_CTX),
        TestData("True", ValueError, context=_t1_CTX),
        TestData("   False   ", False),
        TestData(" false ", False),
        TestData("0", False),
        TestData("f", ValueError, context=_Ff0_CTX),
        TestData("false", False, context=_f0_CTX),
        TestData("False", ValueError, context=_f0_CTX),
        TestData("no", False, context=_Nn_CTX),
        TestData(MISSING, True, True),
        TestData(MISSING, False, False),
        TestData(MISSING, None),
        TestData(MISSING, "True", "True"),
    ]


class TestCollectionEnvVariable(EnvVariablesTestSuite):
    _CONVERT_TYPE_ATTR_NAME = "convert_collection_type"

    _LIST_CTX = {_CONVERT_TYPE_ATTR_NAME: list}
    _TUPLE_CTX = {_CONVERT_TYPE_ATTR_NAME: tuple}
    _SET_CTX = {_CONVERT_TYPE_ATTR_NAME: set}
    _DICT_CTX = {_CONVERT_TYPE_ATTR_NAME: dict}

    CLS_TO_TEST = CollectionEnvVariable
    TESTCASES = [
        TestData("val1, val2, val3", ["val1", "val2", "val3"]),
        TestData("[val1, val2]", ["val1", "val2"]),
        TestData("[val1, val2,]", ["val1", "val2"]),
        TestData("(val1, val2,)", ("val1", "val2")),
        TestData("val1, val2 val3", ["val1", "val2", "val3"]),
        TestData('"val1", "val2", "val3"', ["val1", "val2", "val3"]),
        TestData("  [abcd]    ", ["abcd"]),
        TestData(""" ["abcd", 'abc', " '] """, ["abcd", "abc", '"', "'"]),
        TestData(""" "abcd", "'", '"', b """, ["abcd", "'", '"', "b"]),
        TestData(' [ ab,cd,,abcd, "val2"  ]  ', ["ab,cd,,abcd", "val2"]),
        TestData(MISSING, ["val1", "val2", "val3"], ["val1", "val2", "val3"]),
        TestData(MISSING, None),
        TestData(MISSING, (1, 2, 3), (1, 2, 3)),
        TestData('{"a": 1, "b": 2}', {"a": "1", "b": "2"}),
        TestData('"a":1, "b": 2', ['"a":1', '"b":', "2"], context=_DICT_CTX),
        TestData('{"a": 2, "b": 4}', {"a": "2", "b": "4"}, context=_DICT_CTX),
        TestData(""" {"a", 'b'}""", {"a", "b"}),
        TestData('  {"ab", "bc"} ', {"ab", "bc"}, context=_SET_CTX),
        TestData('("a", "b")', ("a", "b")),
        TestData("(val,)", ("val",)),
        TestData('["a", "b"]', ("a", "b"), context=_TUPLE_CTX),
    ]


if __name__ == "__main__":
    with generic_suite_runner() as suite:
        suite.addTest(TestStringEnvVariable())
        suite.addTest(TestIntegerEnvVariable())
        suite.addTest(TestFloatEnvVariable())
        suite.addTest(TestBooleanEnvVariable())
        suite.addTest(TestCollectionEnvVariable())
