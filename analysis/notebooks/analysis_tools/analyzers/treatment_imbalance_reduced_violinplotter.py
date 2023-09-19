import matplotlib.pyplot as plt
import seaborn as sns
from analysis_tools.utility import (add_median_labels)
from analysis_tools.utility import (highlight_palette, axes_facecolor, figure_facecolor)
from ..types import ImbalanceRegulationFrame
from pathlib import Path


'''
    Violinplotter comparison between treatments for imbalance reduced through balancing actions with command line arguments.
'''

def treatment_imbalance_reduced_per_timeslot_violinplot(imbalance_to_regulation1: ImbalanceRegulationFrame, imbalance_to_regulation2: ImbalanceRegulationFrame, imbalance_to_regulation3: ImbalanceRegulationFrame, tarifftype: str, imbalance: str, path: Path, game: str, brokers: str):

    current_palette = highlight_palette
    sns.set(rc={"axes.facecolor": axes_facecolor, "figure.facecolor": figure_facecolor})
    
    # plot
    
    f, axes = plt.subplots(1,3, figsize = (16,8))
    
    mid = (f.subplotpars.right + f.subplotpars.left)/2 # centered title
    
    try:
        v1 = sns.violinplot(y='perc', data=imbalance_to_regulation1, palette=current_palette, ax = axes[0])
        v2 = sns.violinplot(y='perc', data=imbalance_to_regulation2, palette=current_palette, ax = axes[1])
        v3 = sns.violinplot(y='perc', data=imbalance_to_regulation3, palette=current_palette, ax = axes[2])
        plt.suptitle('Frequency of Imbalances reduced in %'
                       , y = 1.02
                       , x = mid
                       , fontsize = 14,
                        fontweight = 'bold')

        axes[0].set_title("Treatment 1:\n VidyutVanika,IS3,COLDPOWER22,TUC_TAC22,Mertacor22")
        axes[0].set_xlabel('hour', fontsize=12)
        axes[0].set_ylabel('% of imbalance reduced', fontsize=12)
        axes[1].set_title("Treatment 2:\n VidyutVanika,TUC_TAC22,Mertacor22")
        axes[1].set_xlabel('hour', fontsize=12)
        axes[1].set_ylabel('% of imbalance reduced', fontsize=12)
        axes[2].set_title("Treatment 3:\n VidyutVanika,TUC_TAC22")
        axes[2].set_xlabel('hour', fontsize=12)
        axes[2].set_ylabel('% of imbalance reduced', fontsize=12)

        f.savefig(path, bbox_inches='tight')
    
    except Exception:
        print('Game {} could not be analyzed due to empty csv file possibly since there are no balancing actions'.format(game))
    
