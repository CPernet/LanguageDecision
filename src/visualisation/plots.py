"""
Make visualisations for results
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import mean, median


STIMULI = ['SS', 'CP', 'CS', 'US']
sns.set_style("whitegrid")


def plot_median_rts(derivative_path, out_path=None):
    subjects = pd.read_csv(derivative_path)
    stim_rts = subjects.groupby(['stim', 'subj_idx'])['rt'].median()

    plot = sns.violinplot(
        data=[stim_rts[stim] for stim in STIMULI],
        #palette="colorblind"
    )
    plot.set_xticklabels(['SS', 'CP', 'CS', 'US'])
    plot.set_xlabel("Condition")
    plot.set_ylabel("Median Reaction Time (s)")
    if not out_path:
        return plot

    plot.set_title("Subject median reaction time per condition")
    fig = plot.get_figure()
    fig.savefig(out_path)


if __name__ == '__main__':
    print('Plotting data...')
