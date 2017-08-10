"""
Parse experiment matlab struct files to a csv format
for a set of desired attributes relevant to the DDM analysis
"""

import scipy.io as scio
import csv
import glob


CSV_KEYS = ['rt', 'response', 'stim']


def parse_dir(dir_path):
    """
    Parse all .mat files in a directory to .csv files

    Args:
    -- dir_path => directory where .mat files are located
    """
    mat_paths = glob.glob(str(dir_path) + '*.mat')

    for path in mat_paths:
        mat2csv(path)


def mat2csv(mat_path):
    """
    Parse a .mat file to .csv

    Args:
    -- mat_path => path to .mat file
    """
    parsed_mat = _import_mat(mat_path)

    dicts2csv(parsed_mat, mat_path)


def dicts2csv(dict_list, mat_path, out_path=None):
    """
    Write a list of dictionaries to a .csv file

    Args:
    -- dict_list => list of dictionaries to be written to .csv file
    -- mat_path => file path of original .mat file
    -- out_path (optional) => output path. If not provided, original .mat path
    is used, changing the file extension to .csv
    """
    if not out_path:
        out_path = str(mat_path).replace('.mat', '.csv')

    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, CSV_KEYS)
        writer.writeheader()
        writer.writerows(dict_list)


def _import_mat(mat_path):
    """
    Import .mat file into a python data structure, parsing data
    for a single subject as a list of dictionaries, where each
    dictionary holds data for a single trial

    Args:
    -- mat_path => Path to .mat file
    """
    mat_data = scio.loadmat(mat_path, struct_as_record=False)

    mat_struct = mat_data['data'][0, 0]  # MATLAB weirdness

    reaction_times = mat_struct.rt1.tolist()[0]
    responses = [x[0] for x in mat_struct.perf1.tolist()]
    stimuli = [x[0] for x in mat_struct.conditions1.tolist()]

    subject = []

    for exp_run in list(zip(reaction_times, responses, stimuli)):
        trial = dict.fromkeys(CSV_KEYS)
        trial['rt'], trial['response'], trial['stim'] = exp_run
        subject.append(trial)

    return subject
