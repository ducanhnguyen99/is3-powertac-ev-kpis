import pandas as pd
import numpy as np

'''
    Transformer for KPI1 imbalance reduced through balancing actions with command line arguments. Returns the dataframe showing the % share of 
    imbalance reduced through balancing action in each timeslot.
'''

def kpi1_transformer(final_df, tarifftype, imbalance):
    
    # map the command line arguments and aggregate per timeslot
    
    imb_pattern = r".*" if imbalance == 'both' else 'PRODUCE' if imbalance == 'up' else 'CONSUME'
    tarifftype_pattern = r".*" if tarifftype == 'all' else tarifftype

    kpi1_imb_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) ][['ts', 'totalImbalance']].copy()
    kpi1_imb_up['totalImbalance'] = abs(kpi1_imb_up['totalImbalance'].astype(int))
    kpi1_imb_up = kpi1_imb_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_reg_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) 
                           & (final_df['tariff-type'].str.match(tarifftype_pattern))][['ts', 'regUsed']].copy()
    kpi1_reg_up['regUsed'] = abs(kpi1_reg_up['regUsed'])
    kpi1_reg_up = kpi1_reg_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_perc = kpi1_imb_up.merge(kpi1_reg_up, on = ['ts'], how = 'left')

    # calculate the percentage of imbalance reduced in all timeslots reduced to a 24-hour interval
    kpi1_perc['hour'] = kpi1_perc['ts'] % 24
    kpi1_perc['perc'] = kpi1_perc['regUsed'] / kpi1_perc['totalImbalance']
    
    return kpi1_perc