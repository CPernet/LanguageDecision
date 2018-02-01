"""
Parse raw mat files to csv and tsv files
ready for modelling
"""
import os
import glob
import scipy.io as scio
import csv

#TSV_KEYS = ['Condition', 'Onset', 'Duration', 'Response', 'Error_onset', 'Error_duration']
KEYS = ['stim', 'onset', 'rt', 'response', 'error_onset', 'error_duration']
SUBJECT_TYPES = (
    ('healthy', 'sub-healthy', 'sub-healthy_all'),
    ('control', 'sub-control', 'sub-control_all'),
    ('patient', 'sub-patient', 'sub-patient_all')
)
TASK = '_ses-01_task-audicomp_events'
TASK2 = '_ses-02_task-audicomp_events'

# subject idxs with second session -- dataset specific!
SECOND_SESSION = [
    '20129',
    '20731',
    '21280',
    '18910',
    '18333',
    '21440',
    '20126',
    '19156',
    '20054',
    '19582',
    '20890',
    '20130',
    '21586',
    '19566',
    '20732',
    '19582',
]


def parse_dir(dir_path, out_dir, delimiter=','):
    """
    Parse all .mat files in a directory to .tsv files

    Args:
    -- dir_path => directory where .mat files are located
    """
    if not dir_path.endswith('/'):
        dir_path = dir_path + '/'

    mat_paths = glob.glob(str(dir_path) + '*.mat')

    for path in mat_paths:
        mat2delimited(path, out_dir, delimiter=delimiter)


def mat2delimited(mat_path, out_path=None, delimiter=','):
    """
    Parse a .mat file to .tsv
    Args:
    -- mat_path => path to .mat file
    """
    parsed_mat = _import_mat(mat_path)
    extension = '.tsv' if delimiter == '\t' else '.csv'

    subj_idx = mat_path.split('/')[-1].replace('.mat', '').split('_')[-1][-5:]
    task_session = TASK if subj_idx not in SECOND_SESSION else TASK2

    if not out_path.endswith('/') and out_path:
        out_path = out_path + '/'

    for subj_type in SUBJECT_TYPES:
        if subj_type[0] in str(mat_path):
            out_path = out_path + subj_type[1] + subj_idx + task_session + extension

    _write_delimited(parsed_mat, mat_path, out_path, delimiter)


def _write_delimited(subject, mat_path, out_path=None, delimiter=','):
    """
    Write a list of dictionaries to a .tsv file

    Args:
    -- dict_list => list of dictionaries to be written to .tsv file
    -- mat_path => file path of original .mat file
    -- out_path (optional) => output path. If not provided, original .mat path
    is used, changing the file extension to .tsv
    """
    if not out_path:
        out_path = str(mat_path).replace('.mat', '.tsv' if delimiter == '\t' else '.csv')

    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, KEYS, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(subject)


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
        trial = dict.fromkeys(KEYS)
        if exp_run[3] == 0:  # error response
            trial['stim'], trial['onset'], trial['rt'], trial['response'] = exp_run
            trial['error_onset'] = trial['onset']
            trial['error_duration'] = trial['rt']
        else:
            trial['stim'], trial['onset'], trial['rt'], trial['response'] = exp_run
            trial['error_onset'] = 'nil'
            trial['error_duration'] = 'nil'
        subject.append(trial)

    return subject


if __name__ == '__main__':
    dir_path = input("Path to raw data: ")
    out_type = input("Output type (csv, tsv): ")
    out_dir = input("Output directory: ")

    delimiter = '\t' if out_type == 'tsv' else ','

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    parse_dir(dir_path, out_dir, delimiter)

    if not out_dir.endswith('/'):
        out_path = out_dir + '/'

    # Collate multiple delimited files to single file
    import collate
    collated_path = out_path + 'collated'
    for subj_type in SUBJECT_TYPES:
        if subj_type[0] in str(dir_path):
            collated_path = out_path + subj_type[2] + '.' + out_type
    collate.compile_dir(path=out_path, out=collated_path, delimiter=delimiter)

    print("Done! - " + str(out_dir))