# Django Requirements

When generating api-documentation for django projects it will likely complain that django is not configured during the generation process.


## Create a file called `pymdgen_init.py`

This should be created in the same place as all the other source code files.

```py
import logging

logger = logging.getLogger("django")

try:

    # This is to be included in doc *.md files that
    # render api documentation for django models
    # requiring django environment to be setup (app configure etc.)
    #
    # There appears to be no good check on whether this has happened
    # yet or not, in the case of setup being called again an
    # exception will be raised that we catch and ignore

    import django

    django.setup()

except Exception as exc:

    logger.error(f"exception during django-setup for pymdgen: {exc}")


```

## Attach it to pymdgen doc files that generate django code

Any md file that calls `pydmgen` on django code needs to also call `pymdgen` on this new module.

So for example

```
{pymdgen:my_django_app.module}
```

becomes

```
{pymdgen:my_django_app.pymdgen_init}{pymdgen:my_django_app.module}
```
