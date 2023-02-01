import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def kpi1_plotter(final_df, powertype, imbalance, path):
    
    imb_pattern = r".*" if imbalance == 'both' else 'PRODUCE' if imbalance == 'up' else 'CONSUME'
    powertype_pattern = r".*" if powertype == 'all' else powertype

    kpi1_imb_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) ][['ts', 'totalImbalance']].copy()
    kpi1_imb_up['totalImbalance'] = abs(kpi1_imb_up['totalImbalance'])
    kpi1_imb_up = kpi1_imb_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_reg_up = final_df[(final_df['transaction-type'].str.match(imb_pattern)) 
                           & (final_df['tariff-type'].str.match(powertype_pattern))][['ts', 'regUsed']].copy()
    kpi1_reg_up['regUsed'] = abs(kpi1_reg_up['regUsed'])
    kpi1_reg_up = kpi1_reg_up.groupby(by = ['ts'], as_index = False).sum().copy()

    kpi1_perc = kpi1_imb_up.merge(kpi1_reg_up, on = ['ts'], how = 'left')

    kpi1_perc['hour'] = kpi1_perc['ts'] % 24
    kpi1_perc['perc'] = kpi1_perc['regUsed'] / kpi1_perc['totalImbalance']

    f = plt.figure(figsize=(16,4))

    sns.boxplot(x='hour', y='perc', data=kpi1_perc)
    print(kpi1_perc['regUsed'].sum()/kpi1_perc['totalImbalance'].sum())
    
    f.savefig(path)
    
