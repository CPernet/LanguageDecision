#!/usr/bin/env python3
"""
Generate drift diffusion models from processed csv data
"""
import hddm
import datetime
try:
    from .model_tools import gen_models  # if loaded as module
except (ImportError, SystemError):
    from model_tools import gen_models  # if run as script

PILOT_DATA = 'data/processed/pilot_clean.csv'
CONTROL_DATA = 'data/processed/controls_clean.csv'
PATIENT_DATA = 'data/processed/patients_clean.csv'

PILOT_MODELS = 'models/db_pilot'
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
    make_models(PILOT_DATA, PILOT_MODELS)
    make_models(CONTROL_DATA, CONTROL_MODELS)
    make_models(PATIENT_DATA, PATIENT_MODELS)
