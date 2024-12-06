FiveOrbs MkDocs Theme
=====================

This is a theme for MkDocs which is mainly used for the documentation of
[FiveOrbs](https://fiveorbs.dev) projects 

## Installation

Install the package from PyPi using `pip`:

    pip install mkdocs-fiveorbs

Add the theme to your `mkdocs.yml` file:

    theme:
        name: fiveorbs

## Development server

    mkdocs serve -w theme   

## Styles

Install Dart Sass via `npm install -g sass`. During develompment:

    sass --watch styles:theme

## Deploy to PyPi

Install `uv` if not already done. Bump version number in
`setup.py`, then:

    git tag -a X.X.X -m "Release Version X.X.X"
    git push origin vX.X.X
    sass --style=compressed --no-source-map styles:theme
    uv build
    uv publish --username <user> --token <token> # or uv-publish with .pypirc
