import pandas as pd
import seaborn as sns
import matplotlib.patheffects as path_effects

'''
    Utility file containing color specifications and other supporting functions.
'''

highlight_palette = sns.color_palette(
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

axes_facecolor = "#e9d8a6"
figure_facecolor = "#e9d8a6"


def filter_games(cwd, games_csv, brokers):
    games = pd.read_csv(cwd/games_csv, skipinitialspace=True, delimiter=";")
    games = games.fillna("na") # used for masking

    if (brokers == "any"):
        return games.iloc[:, 1].tolist()
    else:
        broker_list = brokers.split(",")
        mask = games[broker_list].apply(lambda x: x.str.contains('na')).sum(axis=1) == 0 # mask filters all games where the desired brokers exist therefore the broker columns should contain no na's
        games = games[(mask) & (games["gameSize"] == len(broker_list))] # check that it is this exact number of brokers only
        list_games = games.iloc[:, 1].tolist() # collect identified game ids
        return list_games
    
    
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
        
def kpi3_catplot(x, y, current_palette, tf_type_df, ylabel, suptitle, destination, ylim):
    a = sns.catplot(
        data=tf_type_df,
        x=x,
        y=y,
        col="tariff-type", # creates facet grid
        kind="box",
        hue="broker",
        col_wrap=2, # number of columns in grid
        legend_out=True, # legend outside of plot
        palette=current_palette,
        dodge=False, # resizing
        sharey=False, # rescaling y axis
        showfliers=False, # remove outliers
        height=5, # figure size
        aspect=2,
    )
        
    for ax in a.axes:
        ax.set_xticklabels(tf_type_df["broker"].unique()) # correct the x ticks
        ax.tick_params(labelbottom=True) 
        add_median_labels(ax) # annotate median value
    
    if (ylim == 1):
        a.set(ylim=(0, None))
    
    a.set_ylabels(ylabel)
    a.add_legend()
    a.fig.suptitle(suptitle, y=1.02, fontsize=16)

    a.savefig(destination, bbox_inches="tight")

