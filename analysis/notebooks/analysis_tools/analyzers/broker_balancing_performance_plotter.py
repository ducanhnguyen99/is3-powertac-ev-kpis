import matplotlib.pyplot as plt
import seaborn as sns
from analysis_tools.utility import (add_median_labels)
from analysis_tools.utility import (highlight_palette, axes_facecolor, figure_facecolor)

'''
    Boxplotter for KPI2 broker balancing performance with command line arguments.
'''

def broker_balancing_performance_boxplot(melt_energy_up_and_down_per_broker, melt_profit_up_and_down_per_broker, tarifftype, path, game):
    try:
        
        current_palette = highlight_palette
        sns.set(rc={"axes.facecolor": axes_facecolor, "figure.facecolor": figure_facecolor})
        
        # plot
        
        f, axes = plt.subplots(2,1, figsize = (20,16))

        a = sns.boxplot(x='broker', y='value', hue='variable', data=melt_energy_up_and_down_per_broker, ax=axes[0], showfliers = False, palette = current_palette)
        b = sns.boxplot(x='broker', y='value', hue='variable', data=melt_profit_up_and_down_per_broker, ax=axes[1], showfliers = False, palette = current_palette)
   
    except Exception:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))

    # labels and legend
       
    new_labels = ['Total Energy (Up-Regulation)', 'Total Energy (Down-Regulation)']
    h, l = a.get_legend_handles_labels()
    a.legend(h, new_labels, loc = "upper right")

    new_labels = ['Payment (Up-Regulation)', 'Profit (Up-Regulation)', 'Payment (Down-Regulation)', 'Profit (Down-Regulation)']
    h, l = b.get_legend_handles_labels()
    b.legend(h, new_labels, loc = "upper right")

    try:
        add_median_labels(a)
        add_median_labels(b)
    except ZeroDivisionError:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))

    axes[0].set(ylabel="Energy")
    axes[1].set(ylabel="Money")
    axes[0].set_title("Energy up-/down-regulated per broker")
    axes[1].set_title("Payment on Balancing Market and Profits per broker")

    mid = (f.subplotpars.right + f.subplotpars.left)/2
    f.suptitle('Broker Balancing Performance (Game: {1}, Tariff-Type: {0})'.format(tarifftype, game), y = 0.92, fontsize = 16, x = mid)
    
    f.savefig(path, bbox_inches='tight')