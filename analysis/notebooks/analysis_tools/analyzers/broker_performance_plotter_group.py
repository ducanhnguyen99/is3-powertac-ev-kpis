import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects


def add_median_labels(ax, fmt='.2f'):
        lines = ax.get_lines()
        boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
        lines_per_box = int(len(lines) / len(boxes))
        for median in lines[4:len(lines):lines_per_box]:
            x, y = (data.mean() for data in median.get_data())
            # choose value depending on horizontal or vertical plot orientation
            value = x if (median.get_xdata()[1] - median.get_xdata()[0]) == 0 else y
            text = ax.text(x, y, f'{value:{fmt}}', ha='center', va='center',
                           fontweight='bold', color='white')
            # create median-colored border around white text for contrast
            text.set_path_effects([
                path_effects.Stroke(linewidth=3, foreground=median.get_color()),
                path_effects.Normal(),
            ])


def kpi2_plotter(df_melt_energy, df_melt_profit, df_melt_perKwh, powertype, path, game):
    try:
        sns.set_style("whitegrid")
        f, axes = plt.subplots(3,1, figsize = (20,24))

        a = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_energy, ax=axes[0], showfliers = False)
        b = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_profit, ax=axes[1], showfliers = False)
        c = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_perKwh, ax=axes[2], showfliers = False)
    except Exception:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))

    new_labels = ['Total Energy (Up-Regulation)', 'Total Energy (Down-Regulation)']

    h, l = a.get_legend_handles_labels()
    a.legend(h, new_labels, loc = "upper right")

    new_labels = ['Payment (Up-Regulation)', 'Profit (Up-Regulation)'
                                                   , 'Payment (Down-Regulation)', 'Profit (Down-Regulation)']
    h, l = b.get_legend_handles_labels()
    b.legend(h, new_labels, loc = "upper right")

    new_labels = ['Price per kWh (Up-Regulation)', 'Price per kWh (Down-Regulation)'
                                                   , 'net price per kWh (given powertypes)']
    h, l = c.get_legend_handles_labels()
    c.legend(h, new_labels, loc = "upper right")
    
    try:
        add_median_labels(a)
        add_median_labels(b)
        add_median_labels(c)
    except ZeroDivisionError:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))

    axes[0].set(ylabel="Energy")
    axes[1].set(ylabel="Money")
    axes[2].set(ylabel="Money per kWh")
    
    mid = (f.subplotpars.right + f.subplotpars.left)/2

    axes[0].set_title("Energy up-/down-regulated per broker")
    axes[1].set_title("Payment on Balancing Market and Profits per broker")
    axes[2].set_title("Price per kWh")
    
    powertype_dict = {'BATTERY_STORAGE': 'Battery Storage', 'PRODUCTION': 'Production', 'STORAGE': 'Storage'
                      , 'CONSUMPTION': 'Consumption', 'THERMAL_STORAGE_CONSUMPTION' : 'Thermal Storage Consumption'
                      , 'SOLAR_PRODUCTION' : 'Solar Production', 'WIND_PRODUCTION': 'Wind Production', 'all':'all'}
    
    f.suptitle('Broker Performance (Power Type: {0}, Game: {1})'.format(powertype_dict[powertype], game), y = 0.91, fontsize = 16, x = mid)
    
    f.savefig(path, bbox_inches='tight')