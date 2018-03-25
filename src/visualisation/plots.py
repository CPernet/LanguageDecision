"""
Make visualisations for results
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import mean, median


STIMULI = ['SS', 'CP', 'CS', 'US']
sns.set_style("whitegrid")


def plot_rts(derivative_path, out_path=None, plot_medians=False):
    subjects = pd.read_csv(derivative_path)
    stim_rts = subjects.groupby(['stim', 'subj_idx'])['rt'].median() if plot_medians \
        else subjects.groupby(['stim'])['rt']

    plot = sns.violinplot(
        data=[stim_rts[stim] for stim in STIMULI] if plot_medians
        else [stim_rts.get_group(stim) for stim in STIMULI],
        # palette="colorblind"
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Condition")

    y_label = "Median Reaction Time (s)" if plot_medians else "Reaction Time (s)"
    plot.set_ylabel(y_label)
    if not out_path:
        return plot

    title = "Subject Median Reaction Time per Condition" if plot_medians \
            else "Subject Reaction Time per Condition"
    plot.set_title(title)
    fig = plot.get_figure()
    fig.savefig(out_path)


if __name__ == '__main__':
    print('Plotting data...')
