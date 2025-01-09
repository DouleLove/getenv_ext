# gnvext
Wrapper for converting environment variables to any python type

<br>

## Installing
**Python 3.10+ is required**

> [!NOTE]
> It's recommended to activate
> <a href="https://docs.python.org/3/library/venv.html">Virtual Environment</a>
> before installing gnvext

To clone and install required packages use the following command:
```bash
# linux/macOS
$ python3 -m pip install gnvext

# windows
$ py -3 -m pip install gnvext
```

<br>

## Quick example
```py
import gnvext

# you can load .env file here

# if "PRINT_HELLO_WORLD" env variable exists,
# then extracts it, otherwise, raises ValueError.
# (raises only if default is a subclass of BaseException (or its instance),
#  in another case, returns default as-is)
PRINT_HELLO_WORLD = gnvext.BooleanEnvVariable(
    name="PRINT_HELLO_WORLD",
    default=ValueError("we don't know if we should greet world or not :("),
).value

if PRINT_HELLO_WORLD:
    print("Hello, world!")

# output for PRINT_HELLO_WORLD=True
# Hello, world!

# output for PRINT_HELLO_WORLD=False
#

# output for PRINT_HELLO_WORLD=None
# ValueError: could not convert "None" to bool

# output for undeclared env var PRINT_HELLO_WORLD
# ValueError: we don't know if we should greet world or not :(
```
