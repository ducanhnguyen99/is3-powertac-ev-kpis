import seaborn as sns
import pandas as pd
from analysis_tools.utility import (add_median_labels)
from analysis_tools.utility import (highlight_palette, axes_facecolor, figure_facecolor)
from ..types import TariffCountFrame, TariffEnergyFrame, TariffSubscriberFrame, TariffPriceFrame

'''
    Boxplotter for KPI3 tariff type KPIs with command line arguments.
'''

def tariff_type_overview_catplot(x: str, y: str, current_palette: str, kpi: pd.DataFrame, ylabel: str, suptitle: str, destination: str, ylim: int):

    a = sns.catplot(
        data=kpi,
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
        ax.set_xticklabels(kpi["broker"].unique()) # correct the x ticks
        ax.tick_params(labelbottom=True)
        add_median_labels(ax) # annotate median value

    if (ylim == 1):
        a.set(ylim=(0, None))

    a.set_ylabels(ylabel)
    a.add_legend()
    a.fig.suptitle(suptitle, y=1.02, fontsize=16)

    a.savefig(destination, bbox_inches="tight")

def tariff_type_overview_boxplots(counted: TariffCountFrame, sum_energy: TariffEnergyFrame, subscribers: TariffSubscriberFrame, price_per_kwh: TariffPriceFrame, destination: str, customers: str, brokers: str, game: str):

    sns.set(rc={"axes.facecolor": axes_facecolor, "figure.facecolor": figure_facecolor})
    
    tariff_type_overview_catplot("broker"
                 , "count"
                 , highlight_palette
                 , counted
                 , "Published Tariffs"
                 , "Number of Tariff Publications (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_publications.png".format(game, brokers, customers)
                 , 1
                )
    
    tariff_type_overview_catplot("broker"
                 , "energy"
                 , highlight_palette
                 , sum_energy
                 , "Traded Energy"
                 , "Total energy traded (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_energy.png".format(game, brokers, customers)
                 , 1
                )
    
    tariff_type_overview_catplot("broker"
                 , "count"
                 , highlight_palette
                 , subscribers
                 , "Subscriber Days"
                 , "Number of Subscriber Days (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_subs.png".format(game, brokers, customers)
                 , 1
                )
    
    tariff_type_overview_catplot("broker"
                 , "avg_price"
                 , highlight_palette
                 , price_per_kwh
                 , "Price per kWh"
                 , "Average Price per kWh (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_prices.png".format(game, brokers, customers)
                 , 0
                )
    