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


def kpi3_plotter(df_melt_count, df_melt_energy, df_melt_subs, path, game):
        
    count_dict = {'BATTERY_STORAGE count': 'Battery Storage', 'PRODUCTION count': 'Production', 'STORAGE count': 'Storage'
                          , 'CONSUMPTION count': 'Consumption', 'THERMAL_STORAGE_CONSUMPTION count' : 'Thermal Storage Consumption'
                          , 'SOLAR_PRODUCTION count' : 'Solar Production', 'WIND_PRODUCTION count': 'Wind Production'}
    energy_dict = {'BATTERY_STORAGE energy': 'Battery Storage', 'PRODUCTION energy': 'Production', 'STORAGE energy': 'Storage'
                          , 'CONSUMPTION energy': 'Consumption', 'THERMAL_STORAGE_CONSUMPTION energy' : 'Thermal Storage Consumption'
                          , 'SOLAR_PRODUCTION energy' : 'Solar Production', 'WIND_PRODUCTION energy': 'Wind Production'}

    #sns.set_style("white")
    my_palette = sns.color_palette(['#005f73', '#0a9396', '#94d2bd'
                                , '#ee9b00', '#ca6702', '#bb3e03'
                                , '#ae2012', '#9b2226', '#9DC08B'
                                , '#9DC08B', '#9DC08B'])

    sns.set(rc={'axes.facecolor':'#e9d8a6', 'figure.facecolor':'#e9d8a6'})

    f, axes = plt.subplots(3,1, figsize = (16,15))
    
    f.subplots_adjust(top=0.85, bottom=0.15, left=0.2, hspace=2)
    f.patch.set_linewidth(6)
    f.patch.set_edgecolor('#609966')
    
    

    a = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_count, ax = axes[0], showfliers = False, palette=my_palette)
    b = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_energy, ax = axes[1], showfliers = False, palette=my_palette)
    c = sns.boxplot(x='broker', y='value', hue='variable', data=df_melt_subs, ax = axes[2], showfliers = False, palette=my_palette)
                                   
    h, l = a.get_legend_handles_labels()
    new_labels = [count_dict[item] for item in l] 
    a.legend(h, new_labels )

    h, l = b.get_legend_handles_labels()
    new_labels = [energy_dict[item] for item in l]
    b.legend(h, new_labels)

    h, l = c.get_legend_handles_labels()
    new_labels = [count_dict[item] for item in l]
    c.legend(h, new_labels)

    add_median_labels(a)
    add_median_labels(b)
    add_median_labels(c)

    axes[0].set(ylabel="Number of tariffs offered")
    axes[1].set(ylabel="Total Energy traded")
    axes[2].set(ylabel="Number of subscriber days")

    mid = (f.subplotpars.right + f.subplotpars.left)/2

    axes[0].set_title("Number of tariffs offered per tariff type")
    axes[1].set_title("Total Energy traded per tariff type")
    axes[2].set_title("Number of subscriber days per tariff type")

    f.suptitle('Tariff type overview (Game: {0})'.format(game), y = 1.02, fontsize = 16, x = mid)

    f.tight_layout()
    
    f.savefig(path, bbox_inches='tight')
     