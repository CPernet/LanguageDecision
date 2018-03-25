"""
Script to generate all visualisations
Run from project directory, preferably using make
"""
if __name__ == '__main__':
    import healthy_plots

    out_dir = 'reports/'

    # healthy deriv + processed paths
    healthy_deriv = 'data/derivative/healthy/sub-healthy_all.csv'
    healthy_dprimes = 'data/processed/healthy/healthy_dprimes.csv'
    healthy_drifts = 'data/processed/healthy/healthy_driftrates.csv'
    healthy_bias = 'data/processed/healthy/healthy_bias.csv'
    healthy_threshold = 'data/processed/healthy/healthy_threshold.csv'
    healthy_nondec = 'data/processed/healthy/healthy_nondec.csv'

    healthy_plots.plot_rts(healthy_deriv, out_path=out_dir + 'healthy_rts')
    healthy_plots.plot_accuracy(healthy_deriv, out_path=out_dir + 'healthy_accs')
    healthy_plots.plot_dprime(healthy_dprimes, out_path=out_dir + 'healthy_dprimes')
    healthy_plots.plot_drift_rate(healthy_drifts, out_path=out_dir + 'healthy_drifts')
    healthy_plots.plot_bias(healthy_bias, out_path=out_dir + 'healthy_bias')
    healthy_plots.plot_threshold(healthy_threshold, out_path=out_dir + 'healthy_threshold')
    healthy_plots.plot_nondec_time(healthy_nondec, out_path=out_dir + 'healthy_nondec')
