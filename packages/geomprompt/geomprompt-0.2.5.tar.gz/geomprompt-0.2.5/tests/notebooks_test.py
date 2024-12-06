"""Test that the notebooks running start to finish without error.

This file is based on the GDA-Cookiecutter, version 2.1.9
In most cases, it should not need to be edited by hand.  See
https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/blob/master/README.md
for instructions on how to update to a newer version of the GDA-Cookiecutter.
"""

import os
from glob import glob

import nbformat
import pytest
from nbconvert import HTMLExporter
from nbconvert.exporters import export
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

# these will be run from inside the `./notebooks` directory
NOTEBOOK_PATHS = [file for file in glob("./notebooks/*.ipynb", recursive=True)]

# Allow customization of the kernel to use for testing
KERNEL_NAME = os.environ.get("KERNEL_NAME", "geomprompt")


@pytest.mark.parametrize("notebook", NOTEBOOK_PATHS)
def test_run_to_completion(notebook: str):
    """Make sure python script versions of jupyter notebooks run without error.

    :param notebook: path to python scripts of the jupyter notebooks
    :return:
    """
    # read in the notebook, we will not need to save a copy to disk
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = ExecutePreprocessor(timeout=1200, kernel_name=KERNEL_NAME)
    try:
        # execute the notebook
        ep.preprocess(nb)
        assert True
    #
    except CellExecutionError as e:
        # save the failed notebook as an html file to
        # `./data/pytest/failed_notebooks/`
        exporter_instance = HTMLExporter()
        html_output = export(exporter_instance, nb)
        file_basename = os.path.basename(notebook).split(".")[0]
        with open(
            f"./data/pytest/failed_notebooks/{file_basename}.html",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(html_output[0])
        # print some additional info to stdout
        # (that should also get picked up by pytest)
        assert False, f"Notebook failed: {notebook}\n{e}"

    return None
