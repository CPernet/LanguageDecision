"""
General utilities used in all stages of the analysis
"""
import csv


def dicts_to_csv(list_of_dicts, out_path):
    """
    Write a list of dictionaries to a CSV
    Dictionary keys are used as headers, so obviously every dict in the list must have
    the same keys
    :param list_of_dicts:
    :param out_path:
    :return:
    """
    with open(out_path, 'w') as out:
        writer = csv.DictWriter(out, list_of_dicts[0].keys())
        writer.writeheader()
        writer.writerows(list_of_dicts)
