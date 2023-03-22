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



def kpi3_plotter(
    tf_type_count, tf_type_energy, tf_type_subs, tf_type_price, destination, brokers, game):

    my_palette = sns.color_palette(
        [
            "#005f73",
            "#0a9396",
            "#94d2bd",
            "#ee9b00",
            "#ca6702",
            "#bb3e03",
            "#ae2012",
            "#9b2226",
            "#9DC08B"
        ]
    )

    sns.set(rc={"axes.facecolor": "#e9d8a6", "figure.facecolor": "#e9d8a6"})

    a = sns.catplot(
        data=tf_type_count,
        x="broker",
        y="count",
        col="tariff-type", # creates facet grid
        kind="box",
        hue="broker",
        col_wrap=2, # number of columns in grid
        legend_out=True, # legend outside of plot
        palette=my_palette,
        dodge=False, # resizing
        sharey=False, # rescaling y axis
        showfliers=False, # remove outliers
        height=5, # figure size
        aspect=2,
    )

    for ax in a.axes:
        ax.set_xticklabels(tf_type_count["broker"].unique()) # correct the x ticks
        ax.tick_params(labelbottom=True) 
        add_median_labels(ax) # annotate median value
        
    a.set_ylabels("Published Tariffs")
    a.set(ylim=(0, None))
    
    a.add_legend()
    a.fig.suptitle("Number of Tariff Publications (Game: {0})".format(game), y=1.02, fontsize=16)

    a.savefig(destination/"{0}_{1}_tariff_publications.png".format(game, brokers), bbox_inches="tight")
    
    
    
    b = sns.catplot(
        data=tf_type_energy,
        x="broker",
        y="energy",
        col="tariff-type",
        kind="box",
        hue="broker",
        col_wrap=2,
        legend_out=True,
        palette=my_palette,
        dodge=False,
        sharey=False,
        showfliers=False,
        height=5,
        aspect=2,
    )

    for ax in b.axes:
        ax.set_xticklabels(tf_type_energy["broker"].unique())
        ax.tick_params(labelbottom=True)
        add_median_labels(ax)
        
    b.set_ylabels("Traded energy")
    b.set(ylim=(0, None))
    
    b.add_legend()
    b.fig.suptitle("Total energy traded (Game: {0})".format(game), y=1.02, fontsize=16)

    b.savefig(destination/"{0}_{1}_tariff_energy.png".format(game, brokers), bbox_inches="tight")
    
    
    
    c = sns.catplot(
        data=tf_type_subs,
        x="broker",
        y="count",
        col="tariff-type",
        kind="box",
        hue="broker",
        col_wrap=2,
        legend_out=True,
        palette=my_palette,
        dodge=False,
        sharey=False,
        showfliers=False,
        height=5,
        aspect=2,
    )

    for ax in c.axes:
        ax.set_xticklabels(tf_type_subs["broker"].unique())
        ax.tick_params(labelbottom=True)
        add_median_labels(ax)
        
    c.set_ylabels("Subscriber Days")
    c.set(ylim=(0, None))
    
    c.add_legend()
    c.fig.suptitle("Number of Subscriber Days (Game: {0})".format(game), y=1.02, fontsize=16)

    c.savefig(destination/"{0}_{1}_tariff_subs.png".format(game, brokers), bbox_inches="tight")
    
    
    
    d = sns.catplot(
        data=tf_type_price,
        x="broker",
        y="avg_price",
        col="tariff-type",
        kind="box",
        hue="broker",
        col_wrap=2,
        legend_out=True,
        palette=my_palette,
        dodge=False,
        sharey=False,
        showfliers=False,
        height=5,
        aspect=2,
    )

    for ax in d.axes:
        ax.set_xticklabels(tf_type_price["broker"].unique())
        ax.tick_params(labelbottom=True)
        add_median_labels(ax)
        
    d.set_ylabels("Price per kWh")
    
    d.add_legend()
    d.fig.suptitle("Average Price per kWh (Game: {0})".format(game), y=1.02, fontsize=16)

    d.savefig(destination/"{0}_{1}_tariff_prices.png".format(game, brokers), bbox_inches="tight")
