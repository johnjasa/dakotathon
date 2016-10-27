#!/usr/bin/env python

import os
import sys
import shutil
from nose.tools import raises, with_setup
from dakotathon.run_component import run_component, main
from dakotathon.dakota import Dakota
from . import start_dir, data_dir


run_dir = os.getcwd()
local_config_file = 'dakota.yaml'
config_file = os.path.join(data_dir, local_config_file)
local_params_file = 'params.in'
params_file = os.path.join(data_dir, local_params_file)
results_file = 'results.out'


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def setup():
    """Called at start of any test using it @with_setup()"""
    global d
    d = Dakota.from_file_like(config_file)


def teardown():
    """Called at end of any test using it @with_setup()"""
    if os.path.exists(results_file):
        os.remove(results_file)
    if os.path.exists(local_config_file):
        os.remove(local_config_file)
    if os.path.exists(local_params_file):
        os.remove(local_params_file)


def teardown_module():
    """Called after all tests have completed."""
    pass


@raises(IOError)
def test_run_component_unknown_config_file():
    """Tests run_component() fails with unknown config file."""
    run_component(params_file, results_file)


# @raises(ImportError)
# @with_setup(setup, teardown)
# def test_run_component_unknown_module():
#     """Tests run_component() fails with unknown module."""
#     d.component = 'foo'
#     d.serialize(local_config_file)
#     run_component(params_file, results_file)


@raises(IndexError)
def test_main_no_args():
    """Tests main() fails without args."""
    sys.argv = []
    main()
