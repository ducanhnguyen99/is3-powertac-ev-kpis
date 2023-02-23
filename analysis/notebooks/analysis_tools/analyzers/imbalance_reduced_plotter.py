import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects

def add_median_labels(ax, fmt='.2f'):
    """Add labels for the median at its location.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        fmt (String): The rounding format.
    """
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

def kpi1_plotter(final_df, powertype, imbalance, path, game):
    """Plot a boxplot of the hourly reduced imbalance through balancing with the command line arguments.

    Arguments:
        final_df (Pd.DataFrame): The Data frame containing tariff transactions and balancing actions.
        powertype (String): The tariff type
        imbalance (String): The regulation type
        path (String): The output location for the image file
    """
    
    # map the command line arguments and aggregate per timeslot
    imb_pattern = r".*" if imbalance == 'both' else 'PRODUCE' if imbalance == 'up' else 'CONSUME'
    powertype_pattern = r".*" if powertype == 'all' else powertype
    
    kpi1_imb_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) ][['ts', 'totalImbalance']].copy()
    kpi1_imb_up['totalImbalance'] = abs(kpi1_imb_up['totalImbalance'].astype(int))
    kpi1_imb_up = kpi1_imb_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_reg_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) 
                           & (final_df['tariff-type'].str.match(powertype_pattern))][['ts', 'regUsed']].copy()
    kpi1_reg_up['regUsed'] = abs(kpi1_reg_up['regUsed'])
    kpi1_reg_up = kpi1_reg_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_perc = kpi1_imb_up.merge(kpi1_reg_up, on = ['ts'], how = 'left')
    
    # calculate the percentage of imbalance reduced in all timeslots reduced to a 24-hour interval
    kpi1_perc['hour'] = kpi1_perc['ts'] % 24
    kpi1_perc['perc'] = kpi1_perc['regUsed'] / kpi1_perc['totalImbalance']
    
    # dictionary for the legend
    powertype_dict = {'BATTERY_STORAGE': 'Battery Storage', 'PRODUCTION': 'Production', 'STORAGE': 'Storage'
                      , 'CONSUMPTION': 'Consumption', 'THERMAL_STORAGE_CONSUMPTION' : 'Thermal Storage Consumption'
                      , 'SOLAR_PRODUCTION' : 'Solar Production', 'WIND_PRODUCTION': 'Wind Production', 'all':'all'}

    sns.set_style("whitegrid")
    
    f = plt.figure(figsize=(16,4))
    
    mid = (f.subplotpars.right + f.subplotpars.left)/2
    
    try:
        box_plot = sns.boxplot(x='hour', y='perc', data=kpi1_perc)

        plt.suptitle('Imbalance reduced in % (Powertype: {0}, {1})'.format(powertype_dict[powertype], imbalance)
                       , y = 0.95
                       , x = mid
                       , fontsize = 14,
                        fontweight = 'bold')
        plt.title('Game: {}'.format(game), y = 1.1)
        plt.ylabel('% of imbalance reduced', fontsize=12, labelpad=10)
        plt.xlabel('hour', fontsize=12, labelpad=10)

        add_median_labels(box_plot)

        f.savefig(path, bbox_inches='tight')
    
    except Exception:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))
    


