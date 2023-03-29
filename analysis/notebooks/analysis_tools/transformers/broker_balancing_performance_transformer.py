import pandas as pd
import numpy as np

'''
    Transformer for KPI2 broker balancing performance with command line arguments. Returns the melted dataframes of energy and profit to 
    show for each broker the up/down-regulated energy and profit.
'''

def kpi2_transformer(final_df, tarifftype, game, tf_transactions):
    
    # map the command line argument
    
    tarifftype_pattern = r".*" if tarifftype == 'all' else tarifftype

    # get list of all brokers to show at the end
    
    broker_list = tf_transactions['broker-name'].unique().tolist()
    final_broker_list = [x for x in broker_list if x != 'default broker'] # exclude default broker
    broker_df = pd.DataFrame(final_broker_list, columns = ['broker'])
    
    # divide into up and down regulation
    df_up = final_df[(final_df['transaction-type'] == 'PRODUCE') 
                     & (final_df['tariff-type'].str.match(tarifftype_pattern))][['broker'
                                                                                , 'regUsed', 'p2', 'transaction-charge', 'tariff-type']].copy()
    df_down = final_df[(final_df['transaction-type'] == 'CONSUME') 
                       & (final_df['tariff-type'].str.match(tarifftype_pattern))][['broker'
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
    

    # use melt to reshape the dataframe
    df_melt_energy = pd.melt(df_merge, id_vars=['broker'], value_vars=['upReg', 'downReg'])
    df_melt_profit = pd.melt(df_merge, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])
    
    return [df_melt_energy, df_melt_profit]