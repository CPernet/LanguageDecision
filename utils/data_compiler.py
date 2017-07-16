"""
Compile .csv data for individual patients in a directory
to a single .csv file ready for consumption by the hddm
library
"""
import glob
import csv


def compile_dir(path, out):
    csv_dir = str(path)
    subjects = []

    for csv_file in glob.glob(csv_dir + 'data*.csv'):
        subject = []

        subj_idx = csv_file[-9:-4]  # Use id from filename
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
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






