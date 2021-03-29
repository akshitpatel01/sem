from sem import SimulationRunner, ParallelRunner
import os
import pytest
from shutil import copyfile

###################
# Runner creation #
###################


@pytest.fixture(scope='function', params=[['ParallelRunner', True],
                                          ['ParallelRunner', False]])
def runner(ns_3_compiled, ns_3_compiled_debug, config, request):
    ns_3_folder = ns_3_compiled if request.param[1] is True else ns_3_compiled_debug
    if request.param[0] == 'SimulationRunner':
        return SimulationRunner(ns_3_folder, config['script'],
                                optimized=request.param[1])
    elif request.param[0] == 'ParallelRunner':
        return ParallelRunner(ns_3_folder, config['script'],
                              optimized=request.param[1])


def test_get_available_parameters(runner, config):
    # Try getting the available parameters of the script
    assert runner.get_available_parameters() == config['params']


@pytest.mark.parametrize('runner',
                         [
                             ['SimulationRunner', True],
                             ['ParallelRunner', True],
                          ],
                         indirect=True)
def test_run_simulations(runner, config,
                         parameter_combination):
    # Make sure that simulations run without any issue
    data_dir = os.path.join(config['campaign_dir'], 'data')
    list(runner.run_simulations([parameter_combination], data_dir))


def test_scratch_script(ns_3_compiled, config):
    data_dir = os.path.join(config['campaign_dir'], 'data')
    runner = ParallelRunner(ns_3_compiled, 'scratch-simulator')
    list(runner.run_simulations([{}], data_dir))


def test_non_existent_script(ns_3_compiled):
    with pytest.raises(ValueError):
        ParallelRunner(ns_3_compiled, 'non_existing_script')


def test_script_without_args(ns_3_compiled):
    ParallelRunner(ns_3_compiled, 'sample-random-variable')


def test_empty_param_list(ns_3_compiled, config, parameter_combination):
    with pytest.raises(ValueError):
        runner = SimulationRunner(ns_3_compiled, 'error-throwing-example')
    data_dir = os.path.join(config['campaign_dir'], 'data')
    with pytest.raises(Exception):
        list(runner.run_simulations([parameter_combination], data_dir))

def test_multiple_files_present(ns_3_compiled, config):
    data_dir = os.path.join(config['campaign_dir'],'data')
    copyfile(os.path.join(ns_3_compiled,'src/core/examples/sample-random-variable.cc'), os.path.join(ns_3_compiled,'scratch/sample-random-variable.cc'))
    ParallelRunner(ns_3_compiled, 'sample-random-variable')

def test_ns3_build_fail(ns_3_compiled, config):
    data_dir = os.path.join(config['campaign_dir'],'data')
    #copyfile(os.path.join(ns_3_compiled,'src/core/examples/sample-random-variable.cc'), os.path.join(ns_3_compiled,'scratch/sample-random-variable.cc'))
    with open(os.path.join(ns_3_compiled, 'src/core/examples/hash-example.cc'),
              'a') as example:
        example.write('Garbage')
    with pytest.raises(Exception):
        ParallelRunner(ns_3_compiled, config['script'])

