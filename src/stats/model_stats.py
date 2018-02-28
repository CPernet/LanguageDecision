"""
Statistics relating to model parameters
"""
import os
import sys
src_dir = os.path.join(os.getcwd(), os.pardir, os.pardir)
sys.path.append(src_dir)

from operator import itemgetter
from itertools import groupby
from src.models.model_tools import load_model


HEALTHY_DATA = 'data/derivative/healthy/sub-healthy_all.csv'
CONTROL_DATA = 'data/derivative/control/sub-control_all.csv'
PATIENT_DATA = 'data/derivative/patient/sub-patient_all.csv'

HEALTHY_MODELS = 'models/db_healthy'
CONTROL_MODELS = 'models/db_controls'
PATIENT_MODELS = 'models/db_patients'

HEALTHY_OUT = 'data/processed/healthy'
CONTROL_OUT = 'data/processed/control'
PATIENT_OUT = 'data/processed/patient'

CONDITIONS = ['SS', 'CP', 'CS', 'US']

PARAM_KEYS = {
    'drift': 'v',
    'threshold': 'a',
    'non_decision': 't',
    'bias': 'z'
}


def get_parameter(model, parameter, conditions=CONDITIONS, between_subj=False, between_cond=False):
    """

    :param model:
    :param parameter:
    :param conditions:
    :param between_subj:
    :param between_cond:
    :return:
    """
    if between_cond:
        return _param_per_condition(model, parameter, conditions)
    if between_subj:
        return _param_per_subject(model, parameter)
    return _param_per_group(model, parameter)


def _param_per_group(model, parameter):
    """
    Get a parameter value representative for the whole group (varies between subjects)
    :param model:
    :param parameter:
    :return:
    """
    param_key = PARAM_KEYS[str(parameter)]
    subjects = set(model.data.subj_idx.values.tolist())
    print(model.nodes_db.node[['z']])
    traces = [c.trace() for c in model.nodes_db.node[[param_key]]]


def _param_per_subject(model, parameter):
    """
    Parameter varies between subjects (within groups)
    :param model:
    :param parameter:
    :return:
    """
    param_key = PARAM_KEYS[str(parameter)]
    subjects = set(model.data.subj_idx.values.tolist())
    nodes = [(subj_idx, param_key + '_subj.' + str(subj_idx))
             for subj_idx in subjects]
    traces = [(subj_idx, model.nodes_db.node[node].trace())
              for subj_idx, node in nodes]

    return [{'subj_idx': subj_idx, parameter: trace.mean()} for subj_idx, trace in traces]


def _param_per_condition(model, parameter, conditions):
    """
    Parameter varies both between subjects and between conditions
    :param model:
    :param parameter:
    :param conditions:
    :return:
    """
    param_key = PARAM_KEYS[str(parameter)]
    subjects = set(model.data.subj_idx.values.tolist())
    cond_nodes = [(cond, str(param_key) + '_subj(' + cond + ')') for cond in conditions]
    nodes = [(subj_idx, cond, cond_node + '.' + str(subj_idx))
                for cond, cond_node in cond_nodes
                for subj_idx in subjects]
    traces = [(subj_idx, cond, model.nodes_db.node[node].trace())
              for subj_idx, cond, node in nodes]

    subject_params = []
    param_means = [{'subj_idx': x[0], x[1]: x[2].mean()} for x in traces]
    sorted_params = sorted(param_means, key=itemgetter('subj_idx'))
    for key, group in groupby(sorted_params, key=lambda x: x['subj_idx']):
        subject = dict.fromkeys(['subj_idx'])
        subject['subj_idx'] = key
        group = list(group)
        for condition in conditions:
            subject[condition] = [x[condition] for x in list(group) if condition in x.keys()][0]
        subject_params.append(subject)

    return subject_params


if __name__ == '__main__':
    os.chdir('../..')
    healthy_vdep = HEALTHY_MODELS + '-v_dep'
    m = load_model(HEALTHY_DATA, healthy_vdep, depends_on={'v': 'stim'})
    healthy_drifts = get_parameter(m, 'drift')

    print(_param_per_subject(m,'bias'))

    import csv

    out_path = HEALTHY_OUT + '/healthy_driftrates.csv'
    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, healthy_drifts[0].keys())
        writer.writeheader()
        writer.writerows(healthy_drifts)
