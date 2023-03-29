import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_tools.utility import (add_median_labels, kpi3_catplot)
from analysis_tools.utility import (highlight_palette, axes_facecolor, figure_facecolor)

'''
    Boxplotter for KPI3 tariff type KPIs with command line arguments.
'''

def kpi3_plotter(tf_type_count, tf_type_energy, tf_type_subs, tf_type_price, destination, customers, brokers, game):

    current_palette = highlight_palette
    sns.set(rc={"axes.facecolor": axes_facecolor, "figure.facecolor": figure_facecolor})
    
    kpi3_catplot("broker"
                 , "count"
                 , highlight_palette
                 , tf_type_count
                 , "Published Tariffs"
                 , "Number of Tariff Publications (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_publications.png".format(game, brokers, customers)
                 , 1
                )
    
    kpi3_catplot("broker"
                 , "energy"
                 , highlight_palette
                 , tf_type_energy
                 , "Traded Energy"
                 , "Total energy traded (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_energy.png".format(game, brokers, customers)
                 , 1
                )
    
    kpi3_catplot("broker"
                 , "count"
                 , highlight_palette
                 , tf_type_subs
                 , "Subscriber Days"
                 , "Number of Subscriber Days (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_subs.png".format(game, brokers, customers)
                 , 1
                )
    
    kpi3_catplot("broker"
                 , "avg_price"
                 , highlight_palette
                 , tf_type_price
                 , "Price per kWh"
                 , "Average Price per kWh (Game: {0}, Customers: {1})".format(game, customers)
                 , destination/"{0}_{1}_{2}_tariff_prices.png".format(game, brokers, customers)
                 , 0
                )
    