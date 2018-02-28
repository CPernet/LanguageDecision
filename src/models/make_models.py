#!/usr/bin/env python3
"""
Generate drift diffusion models from processed csv data
"""
try:
    from .model_tools import gen_models  # if loaded as module
except (ImportError, SystemError):
    from model_tools import gen_models  # if run as script

HEALTHY_DATA = 'data/derivative/healthy/sub-healthy_all.csv'
CONTROL_DATA = 'data/derivative/control/sub-control_all.csv'
PATIENT_DATA = 'data/derivative/patient/sub-patient_all.csv'

HEALTHY_MODELS = 'models/db_healthy'
CONTROL_MODELS = 'models/db_controls'
PATIENT_MODELS = 'models/db_patients'


def make_models(path, models_dir):
    return {
        'lumped': _make_lumped(path, out=models_dir + '-lumped'),
        'v_dep': _make_v_dependent(path, out=models_dir + '-v_dep'),
    }


def _make_lumped(path, out):
    return gen_models(path, out)


def _make_v_dependent(path, out):
    return gen_models(path, out, depends_on={'v': 'stim'}, bias=True)


def _make_t_dependent(path, out):
    return gen_models(path, out, depends_on={'t': 'stim'}, bias=True)


def _make_v_t_dependent(path, out):
    return gen_models(path, out, depends_on={'v': 'stim', 't': 'stim'}, bias=True)


if __name__ == '__main__':
    import os
    os.chdir('../..')
    print(os.getcwd())
    make_models(HEALTHY_DATA, HEALTHY_MODELS)
    make_models(CONTROL_DATA, CONTROL_MODELS)
    make_models(PATIENT_DATA, PATIENT_MODELS)
