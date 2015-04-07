#!/usr/bin/env python
"""Brokers communication between Dakota and a component through files.

This module provides a generic *analysis driver* for a Dakota
experiment. At each evaluation step, Dakota calls this module as an
executable script with the names of the parameters file and the
results file as arguments.

The parameters file provides information on the current Dakota
evaluation step, including the names and values of model variables and
their responses. It also includes, as *analysis components*, a set of
user values configured for this analysis driver: the name of the BMI
component to call, the output file(s) to examine, and the statistic to
apply to the output file(s).

Once the BMI component is identified, an interface is instantiated,
which performs three steps: preprocessing, execution, and
postprocessing. In the preprocessing step, information from the Dakota
parameters file is transferred to the component. Next, in the
execution step, the component is called, using the information passed
from Dakota. In the final step, output from the component is read, and
a single statistic (e.g., mean, median, max, etc.) is applied to
it. This number, one for each response, is returned to Dakota through
the results file, ending the Dakota evaluation step.

"""

import sys
import os
import importlib
from .utils import get_analysis_components
from . import components_path

def main():
    """Sets up component inputs, runs component, gathers output."""

    # References to files passed by Dakota.
    params_file = sys.argv[1]
    results_file = sys.argv[2]

    # Retrieve the analysis components passed into the Dakota parameters file.
    ac = get_analysis_components(sys.argv[1])

    # The first analysis component (Dakota terminology) is the name of
    # the component (CSDMS terminology) to call.
    component = ac.pop(0)
    try:
        module = importlib.import_module(components_path + component)
    except ImportError:
        raise
    if module.is_installed():
        component = module.component()
    else:
        raise NameError('Component cannot be created.')

    # The file and statistic used in each Dakota response.
    component.response_functions = ac

    # Set up the simulation, taking information from the parameters
    # file created by Dakota.
    start_dir = os.path.dirname(os.path.realpath(__file__))
    component.setup(start_dir, params_file)

    # Call the component, calculate the response statistic for the
    # experiment, then write the output to the Dakota results file.
    component.call()
    component.calculate()
    component.write(params_file, results_file)

if __name__ == '__main__':
    main()
