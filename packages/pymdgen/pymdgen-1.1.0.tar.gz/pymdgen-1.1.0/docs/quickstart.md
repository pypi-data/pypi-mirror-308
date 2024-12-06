
# Usage

{pymdgen-cmd:pymdgen --help}

```sh
pymdgen pymdgen
```

# Markdown extension

pymddgen also provides a markdown extension that allows you to
easily insert code and command documentation into your generated
docs.

Simply add the `pymdgen` extension to the `markdown_extensions` section in
your `mkdocs.yml` config file.

## Generate docs for a python module

```
{!examples/md-codedocs.txt!}
```

## Generate output for `ls --help`

```
{!examples/md-cmddocs.txt!}
```
