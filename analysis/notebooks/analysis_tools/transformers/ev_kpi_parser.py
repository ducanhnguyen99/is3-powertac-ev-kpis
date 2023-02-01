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
    
    df = balancing_actions.copy()
    iterations = range(int((len(df.columns)-6)/7))

    final_ba = pd.DataFrame()

    for i in iterations:
        df_basic = df.iloc[:, [0,3]]
        df_data = df.iloc[:, 6+i*7:(i+1)*7+6]
        df_data.columns = ['broker', 'netLoad', 'regOffered', 'regUsed', 'baseCost', 'p1', 'p2']
        df_merge = pd.concat([df_basic,df_data], axis=1)
        final_ba = pd.concat([final_ba, df_merge])

    final_ba = final_ba[final_ba["regUsed"] != 0 ]
    
    # merge datasets
    final_df = final_ba.merge(final_tf, left_on=['ts', 'broker'], right_on=['timeslot', 'broker-name'])
    
    return final_df
