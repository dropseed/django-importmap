# django-importmap

Heavily inspired by [rails/importmap-rails](https://github.com/rails/importmap-rails),
this app adds a simple process for integrating [import maps](https://github.com/WICG/import-maps) into Django.

This is a new project and it hasn't been used in production yet.
But if you're looking to use import maps with Django, give it a try and tell us how it goes.
The structure (and code) is pretty simple.
Contributions are welcome!

## How to use it

You'll need to do four things to use django-importmap.

The TL;DR is:

- Add "importmap" to `INSTALLED_APPS`
- Create an `importmap.toml`
- Run `python manage.py importmap_generate`
- Use `{% importmap_scripts %}` in your template

### 1. Install it

Do the equivalent of `pip install django-importmap` and add it to your `INSTALLED_APPS` list in your `settings.py` file.

```python
# settings.py
INSTALLED_APPS = [
    ...
    "importmap",
]
```

### 2. Configuring an import map

You JavaScript dependencies are conveniently located in your`pyproject.toml` file.

They are listed under `[tool.importmap.dependencies]` and you can add them there. The format is `name = "version"`,
similar to how you would add a dependency to your `package.json` file.

```toml
# pyproject.toml
[tool.importmap.dependencies]
react = "17.0.2"
react-dom = "17.0.2"
```

[jspm.org generator](https://jspm.org/docs/api#install) is used lock and serve the dependencies,
but is basically just like installing them via `npm i <npm package>@<version>`.

### 3. Run `importmap_generate`

To resolve the import map, you'll need to run `python manage.py importmap_generate`.

This will create `importmap.lock` (which you should save and commit to your repo) that contains the actual import map JSON (both for development and production).

You don't need to look at this file yourself, but here is an example of what it will contain:

```json
{
  "config_hash": "09d6237cdd891aad07de60f54689d130",
  "importmap": {
    "imports": {
      "react": "https://ga.jspm.io/npm:react@17.0.2/index.js"
    },
    "scopes": {
      "https://ga.jspm.io/": {
        "object-assign": "https://ga.jspm.io/npm:object-assign@4.1.1/index.js"
      }
    }
  },
  "importmap_dev": {
    "imports": {
      "react": "https://ga.jspm.io/npm:react@17.0.2/dev.index.js"
    },
    "scopes": {
      "https://ga.jspm.io/": {
        "object-assign": "https://ga.jspm.io/npm:object-assign@4.1.1/index.js"
      }
    }
  }
}
```

### 4. Add the scripts to your template

The import map itself gets added by using `{% load importmap %}` and then `{% importmap_scripts %}` in the head of your HTML. This will include the [es-module-shim](https://github.com/guybedford/es-module-shims).

After that, you can include your own JavaScript!
This could be inline or from `static`.
Just be sure to use `type="module"` and the "name" you provided when doing your JS imports (i.e. "react").

```html
{% load importmap %}
<!DOCTYPE html>
<html lang="en">
<head>
    {% importmap_scripts %}
    <script type="module">
        import React from "react"

        console.log(React);
    </script>
</head>
<body>

</body>
</html>
```

When it renders you should get something like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://ga.jspm.io/npm:es-module-shims@1.3.6/dist/es-module-shims.js"></script>
    <script type="importmap">
    {
        "imports": {
            "react": "https://ga.jspm.io/npm:react@17.0.2/dev.index.js"
        },
        "scopes": {
            "https://ga.jspm.io/": {
                "object-assign": "https://ga.jspm.io/npm:object-assign@4.1.1/index.js"
            }
        }
    }
    </script>

    <script type="module">
        import React from "react"

        console.log(React);
    </script>
</head>
<body>

</body>
</html>
```

## Adding static files to import maps

You can include your own static files in the import map by passing kwargs to the `{% importmap_scripts %}` tag.
You can actually use this to include any additional imports, but by using `{% static "name" as name_static %}` you can get the URL to the static file.

```html
{% load importmap static %}
<!DOCTYPE html>
<html lang="en">
<head>
    {% static "my-script.js" as my_script_static %}
    {% importmap_scripts myscript=my_script_static %}
    <script type="module">
        import MyScript from "myscript"
    </script>
</head>
<body>

</body>
</html>
```

## Using Jinja2

To use django-importmap with Jinja2 templates,
you can add `importmap` to a customized Jinja environment.

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        ...
        "OPTIONS": {
            "environment": "app.jinja2.environment",
            ...
        },
    }
]
```

Then in `app/jinja2.py`:

```python
from django.conf import settings
from jinja2 import Environment

from importmap import Importmap


def environment(**options):
    env = Environment(**options)
    env.globals.update({"importmap": Importmap.json(development=settings.DEBUG)})
    return env
```

Then in your Jinja templates you can include a module shim and output the `importmap` variable like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://ga.jspm.io/npm:es-module-shims@1.3.6/dist/es-module-shims.js"></script>
    <script type="importmap">
    {{ importmap|safe }}
    </script>
    <script type="module">
        import React from "react"
        console.log(React);
    </script>
</head>
<body>

</body>
</html>
```

To include your own static files in the import map,
you can pass a dictionary of names and URLs to the `Importmap.json` method:

```python
from django.conf import settings
from django.templatetags.static import static
from jinja2 import Environment

from importmap import Importmap


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "importmap": Importmap.json(
                development=settings.DEBUG, extra_imports={"myjs": static("myjs.js")}
            )
        }
    )
    return env
```

## Project status

This is partly an experiment,
but honestly it's so simple that I don't think there can be much wrong with how it works currently.

Here's a list of things that would be nice to do (PRs welcome):

- Command to add new importmap dependency (use `^` version automatically?)
- Django check for comparing lock and config (at deploy time, etc.)
- Use [deps](https://www.dependencies.io/) to update shim version
- Preload option
- Vendoring option (including shim)
- More complete error handling (custom exceptions, etc.)
