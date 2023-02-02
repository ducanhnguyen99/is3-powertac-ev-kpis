import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects

def add_value_labels(ax, spacing=5):
        """Add labels to the end of each bar in a bar chart.

        Arguments:
            ax (matplotlib.axes.Axes): The matplotlib object containing the axes
                of the plot to annotate.
            spacing (int): The distance between the labels and the bars.
        """

        # For each bar: Place a label
        for rect in ax.patches:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # Number of points between bar and label. Change to your liking.
            space = spacing
            # Vertical alignment for positive values
            va = 'bottom'

            # If value of bar is negative: Place label below bar
            if y_value < 0:
                # Invert space to place label below
                space *= -1
                # Vertically align label at top
                va = 'top'

            # Use Y value as label and format number with one decimal place
            label = "{:.2f}".format(y_value)

            # Create annotation
            ax.annotate(
                label,                      # Use `label` as label
                (x_value, y_value),         # Place label at end of the bar
                xytext=(0, space),          # Vertically shift label by `space`
                textcoords="offset points", # Interpret `xytext` as offset in points
                ha='center',                # Horizontally center label
                va=va)                      # Vertically align label differently for
                                            # positive and negative values.

def kpi2_plotter(final_df, powertype, path, game, tf_transactions):
    
    powertype_pattern = r".*" if powertype == 'all' else powertype

    broker_list = tf_transactions['broker-name'].unique().tolist()
    final_broker_list = [x for x in broker_list if x != 'default broker']
    broker_df = pd.DataFrame(final_broker_list, columns = ['broker'])

    df_up = final_df[(final_df['transaction-type'] == 'PRODUCE') 
                     & (final_df['tariff-type'].str.match(powertype_pattern))][['broker'
                                                                                , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
    df_down = final_df[(final_df['transaction-type'] == 'CONSUME') 
                       & (final_df['tariff-type'].str.match(powertype_pattern))][['broker'
                                                                                  , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
                 
    df_up_reg = df_up[['broker', 'regUsed', 'p2', 'transaction-charge']].copy()
    df_up_reg = df_up_reg.groupby(by = ['broker'], as_index = False).sum()

    df_up_reg['regUsed'] = df_up_reg['regUsed'].apply(lambda x: round(x, 2))
    df_up_reg['p2'] = df_up_reg['p2'].apply(lambda x: round(x, 2))
    df_up_reg['transaction-charge'] = df_up_reg['transaction-charge'].apply(lambda x: round(x, 2))
    df_up_reg['profit'] = df_up_reg['p2'] + df_up_reg['transaction-charge']

    df_up_reg.columns = ['broker', 'upReg', 'pUp_fromBroker', 'pUp_toCustomer', 'profit']


    df_down_reg = df_down[['broker', 'regUsed', 'p2', 'transaction-charge']].copy()
    df_down_reg = df_down_reg.groupby(by = ['broker'], as_index = False).sum()

    df_down_reg['regUsed'] = df_down_reg['regUsed'].apply(lambda x: round(x, 2))
    df_down_reg['p2'] = df_down_reg['p2'].apply(lambda x: round(x, 2))
    df_down_reg['transaction-charge'] = df_down_reg['transaction-charge'].apply(lambda x: round(x, 2))
    df_down_reg['profit'] = df_down_reg['p2'] + df_down_reg['transaction-charge']

    df_down_reg.columns = ['broker', 'downReg', 'pDown_toBroker', 'pDown_fromCustomer', 'profit']

    df_merge = broker_df.merge(df_up_reg, on = ['broker'], how = 'left')
    df_merge = df_merge.merge(df_down_reg, on = ['broker'], how = 'left')

    df_up_reg['sellPrice'] = df_up_reg['pUp_fromBroker']/df_up_reg['upReg']
    df_down_reg['buyPrice'] = df_down_reg['pDown_toBroker']/df_down_reg['downReg']

    sellPrice = df_up_reg[['broker', 'sellPrice']].copy()
    buyPrice = df_down_reg[['broker', 'buyPrice']].copy()

    regPowertypes = tf_transactions[tf_transactions['transaction-regulation'] == 1]['tariff-type'].unique().tolist()
    netCostTf = tf_transactions[(tf_transactions['tariff-type'].isin(regPowertypes)) & 
                                (tf_transactions['tariff-type'].str.match(powertype_pattern)) &
                               (tf_transactions['transaction-type'].isin(['PRODUCE', 'CONSUME']))][['broker-name'
                                                                                     , 'transaction-kWh'
                                                                                     , 'transaction-charge']].groupby(by = ['broker-name'], as_index = False).sum()

    netCostTf['perKwh'] = netCostTf['transaction-charge']/netCostTf['transaction-kWh']
    netCostTf = netCostTf[['broker-name', 'perKwh']]
    netCostTf.columns = ['broker', 'perKwh']

    df_perKwh = broker_df.merge(sellPrice, on = ['broker'], how = 'left')
    df_perKwh = df_perKwh.merge(buyPrice, on = ['broker'], how = 'left')
    df_perKwh = df_perKwh.merge(netCostTf, on = ['broker'], how = 'left')

    # Use melt to reshape the dataframe
    df_melt_energy = pd.melt(df_merge, id_vars=['broker'], value_vars=['upReg', 'downReg'])
    df_melt_profit = pd.melt(df_merge, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])
    df_melt_perKwh = pd.melt(df_perKwh, id_vars=['broker'], value_vars=['sellPrice', 'buyPrice', 'perKwh'])

    # Create a bar plot

    try:
        f, axes = plt.subplots(3,1, figsize = (20,24))

        a = sns.barplot(x='broker', y='value', hue='variable', data=df_melt_energy, ax=axes[0])
        b = sns.barplot(x='broker', y='value', hue='variable', data=df_melt_profit, ax=axes[1])
        c = sns.barplot(x='broker', y='value', hue='variable', data=df_melt_perKwh, ax=axes[2])
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

    add_value_labels(a)
    add_value_labels(b)
    add_value_labels(c)

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
    


    


