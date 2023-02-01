import numpy as np
import pandas as pd

def tf_ba_transformer(tf_transactions, balancing_actions):
    
    # tariff transactions
    tf_reg = tf_transactions[tf_transactions['transaction-regulation'] == 1].copy()

    tf_reg = tf_reg[['timeslot'
                    , 'broker-name'
                    , 'tariff-type'
                    , 'transaction-type'
                    , 'transaction-kWh'
                    , 'transaction-charge']]
    tf_reg_agg = tf_reg.groupby(by = ['timeslot'
                                , 'broker-name'
                                , 'tariff-type'
                                , 'transaction-type'], as_index=False).sum().copy()
    final_tf = tf_reg_agg[tf_reg_agg['transaction-kWh'] != 0].copy()

    # balancing actions
    column_sets = [
        ['ts', 'totalImbalance', 'default broker', 'netLoad', 'regOffered', 'regUsed', 'baseCost', 'p1', 'p2'],
        ['ts', 'totalImbalance', 'CrocodileAgent2020', 'netLoad.1', 'regOffered.1', 'regUsed.1','baseCost.1', 'p1.1', 'p2.1'],
        ['ts', 'totalImbalance', 'COLDPOWER2021', 'netLoad.2', 'regOffered.2', 'regUsed.2', 'baseCost.2', 'p1.2', 'p2.2'],
        ['ts', 'totalImbalance', 'VidyutVanika', 'netLoad.3', 'regOffered.3', 'regUsed.3', 'baseCost.3', 'p1.3', 'p2.3'],
        ['ts', 'totalImbalance', 'IS3', 'netLoad.4', 'regOffered.4', 'regUsed.4', 'baseCost.4', 'p1.4', 'p2.4'],
        ['ts', 'totalImbalance', 'TUC_TAC', 'netLoad.5', 'regOffered.5', 'regUsed.5', 'baseCost.5', 'p1.5', 'p2.5'],
        ['ts', 'totalImbalance', 'Mertacor2021', 'netLoad.6', 'regOffered.6', 'regUsed.6', 'baseCost.6', 'p1.6', 'p2.6']
    ]

    default_broker = balancing_actions[column_sets[0]]
    croc_agent = balancing_actions[column_sets[1]]
    coldpower = balancing_actions[column_sets[2]]
    vv = balancing_actions[column_sets[3]]
    is3 = balancing_actions[column_sets[4]]
    tuc_tac = balancing_actions[column_sets[5]]
    mertacor = balancing_actions[column_sets[6]]

    df_sets = [default_broker, croc_agent, coldpower, vv, is3, tuc_tac, mertacor]

    for df in df_sets:
        df.columns = ['ts', 'totalImbalance', 'broker', 'netLoad', 'regOffered', 'regUsed', 'baseCost', 'p1', 'p2']

    final_ba = pd.concat(df_sets)
    final_ba = final_ba[final_ba["regUsed"] != 0 ]
    
    # merge datasets
    final_df = final_ba.merge(final_tf, left_on=['ts', 'broker'], right_on=['timeslot', 'broker-name'])
    
    return final_df
