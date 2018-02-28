"""
Statistics relating to model parameters
"""
import os
import sys
src_dir = os.path.join(os.getcwd(), os.pardir, os.pardir)
sys.path.append(src_dir)

import scipy.stats.mean as mean
import src.config as conf
from operator import itemgetter
from itertools import groupby
from src.models.model_tools import load_model


CONDITIONS = ['SS', 'CP', 'CS', 'US']

PARAM_KEYS = {
    'drift': 'v',
    'threshold': 'a',
    'non_decision': 't',
    'bias': 'z'
}


def get_parameter(model, parameter, conditions=conf.CONDITIONS, between_subj=False, between_cond=False):
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
    return mean([subject[parameter] for subject in _param_per_subject(model, parameter)])


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
    print("Initialising...")
    from src.utils import dicts_to_csv
    os.chdir('../..')

    print("Loading healthy model data...")
    healthy_model = load_model(
        conf.HEALTHY_DATA,
        conf.HEALTHY_MODELS_DIR + '-v_dep',
        depends_on={'v': 'stim'}
    )

    print("Gathering healthy model parameters...")
    healthy_parameters = (
        (get_parameter(healthy_model, 'drift', between_cond=True), conf.HEALTHY_OUT_DIR + 'healthy_driftrates.csv'),
        (get_parameter(healthy_model, 'bias', between_subj=True), conf.HEALTHY_OUT_DIR + 'healthy_bias.csv'),
        (get_parameter(healthy_model, 'threshold', between_subj=True), conf.HEALTHY_OUT_DIR + 'healthy_threshold.csv'),
        (get_parameter(healthy_model, 'non_decision', between_subj=True), conf.HEALTHY_OUT_DIR + 'healthy_nondec.csv'),
    )

    print("Writing healthy model parameters to csv files...")
    for parameter, out_path in healthy_parameters:
        dicts_to_csv(parameter, out_path)
        print("Wrote " + out_path)
