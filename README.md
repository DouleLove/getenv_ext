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

Also, gnvext may be cloned from GitHub:
```bash
$ git clone https://github.com/DouleLove/gnvext
```

<br>

## Usage example
```py
import gnvext
import django

# let's assume we have DJANGO_ALLOWED_HOSTS environment variable
# which we want to extract and convert to list.
# If it does not exist, ['*'] will be returned

ALLOWED_HOSTS = gnvext.CollectionEnvVariable(
    'DJANGO_ALLOWED_HOSTS',
    ['*'],
).value

...  # django project settings.py stuff here
```
