"""
Collate .csv data for individual patients in a directory
to a single .csv file ready for consumption by the hddm
library
"""
import glob
import csv


def compile_dir(path, out, delimiter=','):
    csv_dir = str(path)
    subjects = []

    if not csv_dir.endswith('/'):
        csv_dir + '/'

    extension = '.tsv' if delimiter == '\t' else '.csv'
    files = glob.glob(csv_dir + 'sub*' + extension)
    if not files:
        return False

    for csv_file in files:
        subject = []

        subj_idx = csv_file.split('/')[-1].split('_')[0][-5:]  # Use id from filenames last 5 chars
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for trial in reader:
                trial['subj_idx'] = subj_idx
                trial['stim'] = _parse_condition(trial['stim'])
                subject.append(trial)
        subjects.append(subject)

    keys = subjects[0][0].keys()

    with open(out, 'w') as out_path:
        writer = csv.DictWriter(out_path, keys)
        writer.writeheader()
        for subj in subjects:
            writer.writerows(subj)

    return str(out)


def _parse_condition(stim_num):
    if stim_num == '1':
        return 'SS'
    if stim_num == '2':
        return 'CP'
    if stim_num == '3':
        return 'CS'
    if stim_num == '4':
        return 'US'
