import pandas as pd
import numpy as np

def kpi2_transformer(final_df, powertype, game, tf_transactions):
    
    # map the command line argument
    
    powertype_pattern = r".*" if powertype == 'all' else powertype

    # get list of all brokers to show at the end
    
    broker_list = tf_transactions['broker-name'].unique().tolist()
    final_broker_list = [x for x in broker_list if x != 'default broker'] # exclude default broker
    broker_df = pd.DataFrame(final_broker_list, columns = ['broker'])
    
    # divide into up and down regulation
    df_up = final_df[(final_df['transaction-type'] == 'PRODUCE') 
                     & (final_df['tariff-type'].str.match(powertype_pattern))][['broker'
                                                                                , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
    df_down = final_df[(final_df['transaction-type'] == 'CONSUME') 
                       & (final_df['tariff-type'].str.match(powertype_pattern))][['broker'
                                                                                  , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
                 
    # get KPIs by grouping and manipulating data
    
    df_up_reg = df_up[['broker', 'regUsed', 'p2', 'transaction-charge']].copy()
    df_up_reg = df_up_reg.groupby(by = ['broker'], as_index = False).sum()

    df_up_reg['regUsed'] = df_up_reg['regUsed'].apply(lambda x: round(x, 2))
    df_up_reg['p2'] = df_up_reg['p2'].apply(lambda x: round(x, 2))
    df_up_reg['transaction-charge'] = df_up_reg['transaction-charge'].apply(lambda x: round(x, 2))
    df_up_reg['profit'] = df_up_reg['p2'] + df_up_reg['transaction-charge'] # payyment of both customer and other broker

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
    
    # average price each kWh is sold and bought by the broker on the balancing market
    
    df_up_reg['sellPrice'] = df_up_reg['pUp_fromBroker']/df_up_reg['upReg']
    df_down_reg['buyPrice'] = df_down_reg['pDown_toBroker']/df_down_reg['downReg']

    sellPrice = df_up_reg[['broker', 'sellPrice']].copy()
    buyPrice = df_down_reg[['broker', 'buyPrice']].copy()
    
    # calculate average price customer pays to the broker for that tariff type

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

    # use melt to reshape the dataframe
    df_melt_energy = pd.melt(df_merge, id_vars=['broker'], value_vars=['upReg', 'downReg'])
    df_melt_profit = pd.melt(df_merge, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])
    df_melt_perKwh = pd.melt(df_perKwh, id_vars=['broker'], value_vars=['sellPrice', 'buyPrice', 'perKwh'])
    
    return [df_melt_energy, df_melt_profit, df_melt_perKwh]