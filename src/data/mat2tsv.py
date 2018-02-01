import glob
import csv
import os
import scipy.io as scio

TSV_KEYS = ['Condition', 'Onset', 'Duration', 'Response', 'Error_onset', 'Error_duration']


def parse_dir(dir_path):
    """
    Parse all .mat files in a directory to .tsv files

    Args:
    -- dir_path => directory where .mat files are located
    """
    mat_paths = glob.glob(str(dir_path) + '*.mat')

    for path in mat_paths:
        mat2tsv(path)


def mat2tsv(mat_path):
    """
    Parse a .mat file to .tsv

    Args:
    -- mat_path => path to .mat file
    """
    parsed_mat = _import_mat(mat_path)

    dicts2tsv(parsed_mat, mat_path)


def dicts2tsv(dict_list, mat_path, out_path=None):
    """
    Write a list of dictionaries to a .tsv file

    Args:
    -- dict_list => list of dictionaries to be written to .tsv file
    -- mat_path => file path of original .mat file
    -- out_path (optional) => output path. If not provided, original .mat path
    is used, changing the file extension to .tsv
    """
    if not out_path:
        out_path = str(mat_path).replace('.mat', '.tsv')

    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, TSV_KEYS, delimiter='\t')
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

    responses = [x[0] for x in mat_struct.perf1.tolist()]
    responses = [x if str(x) != 'nan' else 'nil' for x in responses]

    stimuli = [x[0] for x in mat_struct.conditions1.tolist()]
    stimuli = [x if x != 'nan' else 'nil' for x in stimuli]

    onsets = [x[0] for x in mat_struct.onsets1.tolist()]
    onsets = [x if x != 'nan' else 'nil' for x in onsets]

    durations = [x[0] for x in mat_struct.durations1.tolist()]
    durations = [x if x != 'nan' else 'nil' for x in durations]

    subject = []

    for exp_run in list(zip(stimuli, onsets, durations, responses)):
        trial = dict.fromkeys(TSV_KEYS)
        if exp_run[3] == 0:  # error response
            trial['Condition'], trial['Onset'], trial['Duration'], trial['Response'] = exp_run
            trial['Error_onset'] = trial['Onset']
            trial['Error_duration'] = trial['Duration']
        else:
            trial['Condition'], trial['Onset'], trial['Duration'], trial['Response'] = exp_run
            trial['Error_onset'] = 'nil'
            trial['Error_duration'] = 'nil'
        subject.append(trial)

    return subject


if __name__ == '__main__':
    dir_path = input("Path to data: ")
    patient_type = input("Patient type (healthy, control, patient): ")
    parse_dir(dir_path)
    files = glob.glob(dir_path + '*.tsv')

    import shutil
    for file in files:
        shutil.move(file, file.replace('data_', 'sub-' + str(patient_type)).replace('.tsv', '_ses-01_task-audicomp_events.tsv'))
    print("Done! - " + str(dir_path))
