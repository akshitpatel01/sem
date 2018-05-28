# A Simulation Execution Manager for ns-3 #

A Python library to perform multiple ns-3 script executions, manage
the results and collect them in processing-friendly data structures.

## Building the module ##

This module is developed using `pipenv` facilities. In order to manage
virtual environments and install dependencies, make sure `pipenv` is
installed. Typically, the following is enough:

```bash
pip install pipenv
```

From the project root, one can then install the package and the
requirements with the following:

```bash
pipenv install
```

If a development environment is also desired, the `Pipfile`'s
`dev-packages` can be installed by attaching the `--dev` flag to the
command above.

After this step, a sub-shell using the new virtual environment can be
created by calling:

```bash
pipenv shell
```

From here, the examples in `examples/` can be run and a python
REPL can be started to use the library interactively.

## Documentation ##

Documentation can be built locally using the makefile's `docs` target.
The documentation of the current version of the package is also
available on [readthedocs][rtd].

## Authors ##

Davide Magrin

[rtd]: https://simulationexecutionmanager.readthedocs.io