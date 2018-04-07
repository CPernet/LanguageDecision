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

sns.set()
palette = sns.cubehelix_palette(6, start=3, rot=1.9, gamma=.8, hue=2, reverse=True)
sns.set_style("whitegrid")
sns.set_palette(palette)


def plot_rts(derivative_path, out_path=None, plot_medians=False):
    subjects = pd.read_csv(derivative_path)
    accurate_rts = subjects[pd.to_numeric(subjects.response, errors='coerce') > 0]
    stim_rts = accurate_rts.groupby(['stim', 'subj_idx'])['rt'].median() if plot_medians \
            else accurate_rts.groupby(['stim', 'subj_idx'])['rt'] 

    plt.figure()
    plot = sns.violinplot(
        data=[stim_rts[stim] for stim in STIMULI] if plot_medians
        else [stim_rts.get_group(stim) for stim in STIMULI],
        # palette="colorblind"
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Condition")
    y_label = "Median Reaction Time (s)" if plot_medians else "Reaction Time (s)"
    plot.set_ylabel(y_label)
    plt.setp(plot.collections, alpha=.7)

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

    plt.figure()
    plot = sns.boxplot(
        data=[stim_accs[stim] for stim in STIMULI],
        showfliers=False,
        boxprops= dict(alpha=.7)
    )
    sns.swarmplot(
        data=[stim_accs[stim] for stim in STIMULI],
        color=".25",
        ax=plot
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Condition")
    plot.set_ylabel("Accuracy Score")
    plot.set_ylim(0.8, 1.01)

    if out_path:
        plot.set_title("Subject Accuracy Score per Condition")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_dprime(processed_path, out_path=None):
    subjects_dprimes = pd.read_csv(processed_path)

    plt.figure()
    plot = sns.violinplot(
        data=[subjects_dprimes[pair] for pair in STIMULI_PAIRS],
        palette=palette[1:]
    )
    plot.set_xticklabels(STIMULI_PAIRS)
    plot.set_xlabel("Condition Pairs")
    plot.set_ylabel("d'")
    plt.setp(plot.collections, alpha=.7)

    if out_path:
        plot.set_title("Subject Incongruence (d') Score")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_drift_rate(processed_path, out_path=None):
    subjects_drift = pd.read_csv(processed_path)

    plt.figure()
    plot = sns.violinplot(
        data=[subjects_drift[stim] for stim in STIMULI]
    )
    plot.set_xticklabels(STIMULI)
    plot.set_xlabel("Conditions")
    plot.set_ylabel("Drift Rate")
    plt.setp(plot.collections, alpha=.7)

    if out_path:
        plot.set_title("Subject Drift Rate per Condition")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_threshold(processed_path, out_path=None):
    subjects_threshold = pd.read_csv(processed_path).threshold

    plt.figure()
    plot = sns.distplot(
        subjects_threshold,
        color='steelblue',
        rug=True
    )
    plot.set_ylabel("Density")
    plot.set_xlabel("Threshold")

    if out_path:
        plot.set_title("Subject Threshold")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_bias(processed_path, out_path=None):
    subjects_bias = pd.read_csv(processed_path).bias

    plt.figure()
    plot = sns.distplot(
        subjects_bias,
        color='steelblue',
        rug=True
    )
    plot.set_ylabel("Density")
    plot.set_xlabel("Bias")

    if out_path:
        plot.set_title("Subject Bias")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot


def plot_nondec_time(processed_path, out_path=None):
    subjects_nondec = pd.read_csv(processed_path).non_decision

    plt.figure()
    plot = sns.distplot(
        subjects_nondec,
        color='steelblue',
        rug=True
    )
    plot.set_ylabel("Density")
    plot.set_xlabel("Non-Decision Time (s)")

    if out_path:
        plot.set_title("Subject Non-Decision Time")
        fig = plot.get_figure()
        fig.savefig(out_path)
    return plot
