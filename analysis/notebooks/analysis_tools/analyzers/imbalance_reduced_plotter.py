import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_tools.utility import (add_median_labels)
from analysis_tools.utility import (highlight_palette, axes_facecolor, figure_facecolor)

'''
    Boxplotter for KPI1 imbalance reduced through balancing actions with command line arguments.
'''

def kpi1_plotter(kpi1_perc, tarifftype, imbalance, path, game, brokers):
    

    
    current_palette = highlight_palette
    sns.set(rc={"axes.facecolor": axes_facecolor, "figure.facecolor": figure_facecolor})
    
    
    # dictionary for the legend
    tarifftype_dict = {'BATTERY_STORAGE': 'Battery Storage', 'PRODUCTION': 'Production', 'STORAGE': 'Storage'
                      , 'CONSUMPTION': 'Consumption', 'THERMAL_STORAGE_CONSUMPTION' : 'Thermal Storage Consumption'
                      , 'SOLAR_PRODUCTION' : 'Solar Production', 'WIND_PRODUCTION': 'Wind Production', 'all':'all'}    
    
    # plot
    
    f = plt.figure(figsize=(16,4))
    
    mid = (f.subplotpars.right + f.subplotpars.left)/2 # centered title
    
    try:
        box_plot = sns.boxplot(x='hour', y='perc', data=kpi1_perc, palette=current_palette)

        plt.suptitle('Imbalance reduced in % (Game: {0})'.format(game)
                       , y = 0.95
                       , x = mid
                       , fontsize = 14,
                        fontweight = 'bold')
        plt.title('Tariff-type: {0}, Up/Down-reg: {1}, Brokers: {2}'.format(tarifftype_dict[tarifftype], imbalance, brokers), y = 1.1)
        plt.ylabel('% of imbalance reduced', fontsize=12, labelpad=10)
        plt.xlabel('hour', fontsize=12, labelpad=10)

        add_median_labels(box_plot)

        f.savefig(path, bbox_inches='tight')
    
    except Exception:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))
    


