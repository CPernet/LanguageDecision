import csv
from operator import itemgetter
from itertools import groupby
try:
    from . import signal_detection  # if loaded as module
except (SystemError, ImportError):
    import signal_detection  # if run as script


STIM_PAIRS = (
    ('SS', 'CP'),  # phonology
    ('SS', 'CS'),  # semantic
    ('SS', 'US'),  # unrelated
)


def dprimes_from_csv(derivative_path, out_path=None):
    csv_entries = list(_import_csv(derivative_path))

    subjects = groupby(sorted(csv_entries, key=itemgetter('subj_idx')), key=itemgetter('subj_idx'))
    subjects_dprimes = []
    for subject in subjects:
        subj_idx, subj_data = subject
        subj_data = list(subj_data)  # convert iteritems object to list
        subj_dprimes = {'subj_idx': subj_idx}
        print(subj_idx)
        for pair in STIM_PAIRS:
            stim1, stim2 = pair
            subj_stim1 = [d['response'] for d in subj_data if d['stim'] == str(stim1)]
            subj_stim2 = [d['response'] for d in subj_data if d['stim'] == str(stim2)]
            hits = len([d for d in subj_stim1 if d == '1' or d == '1.0'])
            false_alarms = len([v for v in subj_stim2 if v == '0' or v == '0.0'])
            d_prime = signal_detection.signal_detection(len(subj_stim1), len(subj_stim2), hits, false_alarms)['d_prime']
            subj_dprimes[str(stim1) + '_' + str(stim2)] = d_prime
        subjects_dprimes.append(subj_dprimes)
        print(subj_dprimes)

    if out_path:
        _write_to_csv(subjects_dprimes, out_path=out_path)
    return subjects_dprimes


def _import_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def _write_to_csv(subjects_dprimes, out_path):
    if not out_path.endswith('/') and out_path:
        out_path = out_path + '/'

    out_path = out_path + 'dprimes.csv'

    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, subjects_dprimes[0].keys())
        writer.writeheader()
        writer.writerows(subjects_dprimes)


if __name__ == '__main__':
    dir_path = input("Path to compiled derivative data: ")
    out_dir = input("Output directory: ")

    import os
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    dprimes_from_csv(dir_path, out_dir)

    print('Done! - ' + str(out_dir))
