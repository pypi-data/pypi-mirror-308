# Contributing and Developing

## Organization

These build instructions are provided by GDA-Cookiecutter, version 2.1.9.

This repository is built to use setuptools, in our interpretation of standard best-practices in Fall 2023.
It is organized according to
https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout

## Work Flow

- Go to [Issues](https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/issues) and raise a new issue.  Choose the Issue template ([Bug](.gitlab/issue_templates/Bug.md), [Feature](.gitlab/issue_templates/Feature%20Request.md), [etc](.gitlab/issue_templates/)) that is most appropriate, and fill in the requested sections.
- Create a Merge Request, which automatically creates the associated branch.
- Fix the problem, or ask for help, on that branch.
- When the fix is complete, increment the version (following [semantic versioning](https://semver.org/)) in [pyproject.toml](pyproject.toml) and update the [CHANGELOG.md](CHANGELOG.md) detailing the high-level changes to the code. For more information on the changelog, see https://keepachangelog.com/.
- On the Merge Request, click the "Mark as ready" button and tag _**someone else**_ to review your Merge Request.
- Make sure that the [branch pipeline](https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/pipelines) passes entirely before merging.
- Merge when there is consensus.
- Make sure that the [main pipeline](https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/pipelines) passes entirely after merging.
- If ready for an internal release, click the `do_release_internal` job to tag this as a Release for GDA use.
- Optionally, click the `do_external_publish` job to deploy this publicly.

## Installation

### End-user's Installation

See [README.md](README.md)

### Developer's Installation

The following will replicate the setup in the CI/CD environment that uses `conda` (or `mamba` if available):

```bash
$ cd <path/to/geomprompt>
$ bash install.sh  # This builds two conda environments. geomprompt-base is minimal and geomprompt is all-inclusive.
```


## Notebooks

All jupyter notebooks are contained in the `./notebooks` directory.

These notebooks can be run in the `"Python (geomprompt)"` kernel that is created by `install.sh`.

The notebooks are tested to make sure they run end-to-end without error (see the "Testing" section for more information).

The notebooks are also embedded in the `sphinx` documentation (see the "Documentation" section for more information).


## Testing

The following will run the unit tests on the package:

```bash
$ source activate geomprompt
$ cd <path/to/geomprompt>
$ pytest -c ./tests/pytest_main.ini
```


The following will test whether the jupyter notebooks run end-to-end without error:
```bash
$ source activate geomprompt
$ cd <path/to/geomprompt>
$ pytest -c ./tests/pytest_notebooks.ini
```


## Software Versioning

A [changelog](CHANGELOG.md) is maintained. As the code evolves, this file should update accordingly
with information about added features, deprecations, and bug fixes.

When enough progress has been made or a big enough future change is planned, a version of the code should be tagged.

For more on versioning expectations and how to structure the changelog, see the links in the [changelog](CHANGELOG.md) document.

The version number should be changed accordingly in [pyproject.toml](pyproject.toml).

## Formatting and linting

[Ruff](https://docs.astral.sh/ruff/) is used for linting and formatting code. 

### Linting

Linting refers to a static analysis of the codebase to check for efficient and
compliant python code. The default checks are documented in the
[pyproject.toml](pyproject.toml) files. Ruff can be run from the command line
via `ruff check` or by installing ruff in an IDE. Certain errors in ruff can be
automatically fixed by running `ruff check --fix`. Any errors that pop up (e.g.
E401) can be expanded on by executing `ruff rule <error>`, as in `ruff rule
E401`.

### Formatting

Formatting refers to adjusting the physical appearance of the code (adding new lines, commas, etc.), without
modifying any of the intent or logic. Ruff can automatically format a specific file or an entire repository 
by executing `ruff format <path>/<to>/<file>` or `ruff format`.

## Documentation

### Viewing Docs

Published documentation is available at http://rootshape.pages.geomdata.com/geomprompt.

### Building Docs Locally

Once the repo is cloned, `sphinx` documentation can be built after installing the `conda` environment:

```bash
$ source activate geomprompt
$ cd <path/to/geomprompt>
$ bash build_sphinx_docs.sh
```

Note that the `-W` option is enabled in the `sphinx` build, which converts warnings to errors.
If debugging a failing doc build locally, it is often helpful
to temporarily remove this option (but add it back before merging).

Then, open up `<path/to/geomprompt>/public/index.html` in a web browser to view the locally-built documentation.

## Publishing Code and Docs

Documentation and software wheels are exclusively deployed through CI/CD.

For more on what can be published and where, see [PIPELINE.md](PIPELINE.md).

## Developer's Template Update Procedures

This code was templated from GDA-Cookiecutter, version 2.1.9.
If you are the developer, and want this repository to be up-to-date with more current cookiecutter templates, see https://gitlab.geomdata.com/geomdata/gda-cookiecutter.
There, you can find up-to-date instructions on how to automatically create a Merge Request with the necessary updates to this repository.
See the cookiecutter replay file at [.gda-cookiecutter_replay.json](.gda-cookiecutter_replay.json)
