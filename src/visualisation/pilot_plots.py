"""
Make visualisations for pilot results
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import mean, median


STIMULI = ['SS', 'CP', 'CS', 'US']
STIMULI_PAIRS = ['SS_CP', 'SS_CS', 'SS_US']
TRIALS_PER_STIM = 30
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

    if out_path:
        title = "Subject Median Reaction Time per Condition" if plot_medians \
            else "Subject Reaction Time per Condition"
        plot.set_title(title)
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_accuracy(derivative_path, out_path=None):
    subjects = pd.read_csv(derivative_path)
    stim_accs = subjects.groupby(['stim', 'subj_idx']).response.\
        agg(lambda x: pd.to_numeric(x, errors='coerce').sum() / x.count())

    plot = sns.boxplot(
        data=[stim_accs[stim] for stim in STIMULI],
        showfliers=False
    )
    sns.swarmplot(
        data=[stim_accs[stim] for stim in STIMULI],
        color=".25",
        ax=plot
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Condition")
    plot.set_ylabel("Accuracy Score")
    plot.set_ylim(0, 1.01)

    if out_path:
        plot.set_title("Subject Accuracy Score per Condition")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_dprime(processed_path, out_path=None):
    subjects_dprimes = pd.read_csv(processed_path)

    plot = sns.violinplot(
        data=[subjects_dprimes[pair] for pair in STIMULI_PAIRS],
        palette="muted"
    )
    plot.set_xticklabels(STIMULI_PAIRS)
    plot.set_xlabel("Condition Pairs")
    plot.set_ylabel("d'")

    if out_path:
        plot.set_title("Subject Incongruence (d') Score")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_drift_rate(processed_path, out_path=None):
    subjects_drift = pd.read_csv(processed_path)

    plot = sns.violinplot(
        data=[subjects_drift[stim] for stim in STIMULI]
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Conditions")
    plot.set_ylabel("Drift Rate")

    if out_path:
        plot.set_title("Subject Drift Rate per Condition")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_threshold(processed_path, out_path=None):
    return


def plot_bias(processed_path, out_path=None):
    return


def plot_nondec_time(processed_path, out_path=None):
    return
