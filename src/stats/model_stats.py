"""
Statistics relating to model parameters
"""
import os
import sys
src_dir = os.path.join(os.getcwd(), os.pardir, os.pardir)
sys.path.append(src_dir)

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


def drift_rate_per_condition(model, conditions=CONDITIONS, dependson_cond=True, raw_trace=False):
    nodes = ['v']
    if dependson_cond:
        nodes = ['v(' + cond + ')' for cond in conditions]
    traces = [c.trace() for c in model.nodes_db.node[nodes]]
    [(x, m.nodes_db.node[x].trace().mean()) for x in m.nodes_db.node.keys() if 'v_subj' in x]
    return [trace.mean() for trace in traces] if not raw_trace else traces


def drift_rate_per_subject(model, conditions=CONDITIONS):
    subjects = set(model.data.subj_idx.values.tolist())
    cond_nodes = [(cond, 'v_subj(' + cond + ')') for cond in conditions]
    nodes = [(subj_idx, cond, cond_node + '.' + str(subj_idx))
                for cond, cond_node in cond_nodes
                for subj_idx in subjects]
    traces = [(subj_idx, cond, model.nodes_db.node[node].trace())
              for subj_idx, cond, node in nodes]

    subject_rates = list()
    for trace in traces:
        subj_idx, condition, drift_trace = trace
        drift = drift_trace.mean()
        subject_rates.append({
            'subj_idx': subj_idx,
            'stim': condition,
            'v': drift
        })
    return subject_rates


def get_threshold():
    return


def get_nondec_time():
    return


def get_bias():
    return


if __name__ == '__main__':
    os.chdir('../..')
    healthy_vdep = HEALTHY_MODELS + '-v_dep'
    m = load_model(HEALTHY_DATA, healthy_vdep, depends_on={'v': 'stim'})
    healthy_drifts = drift_rate_per_subject(m)

    import csv

    out_path = HEALTHY_OUT + '/healthy_driftrates.csv'
    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, healthy_drifts[0].keys())
        writer.writeheader()
        writer.writerows(healthy_drifts)

