import pandas as pd
import numpy as np


def kpi3_transformer(tf_transactions, game):
    tf_type_dist = tf_transactions[['timeslot', 'broker-name', 'tariff-id', 'tariff-type'
                                    , 'transaction-kWh', 'customer-name', 'customer-count']].copy()


    tf_type_count = pd.DataFrame(tf_type_dist[['broker-name', 'tariff-type', 'tariff-id']]
                                 .groupby(by = ['broker-name', 'tariff-type'])['tariff-id'].nunique())
    tf_type_count = tf_type_count.reset_index()
    tf_type_count.columns = ['broker', 'tariff-type', 'count']

    tf_type_count = tf_type_count.pivot(columns='tariff-type', index='broker')
    tf_type_count.columns = tf_type_count.columns.swaplevel().map(' '.join)
    tf_type_count = tf_type_count.replace(np.nan,0)
    tf_type_count = tf_type_count.reset_index()

    tf_types_count = tf_type_count.loc[:, tf_type_count.columns != "broker"]
    df_melt_count = pd.melt(tf_type_count, id_vars=['broker'], value_vars=tf_types_count.columns.tolist())


    #tf_type_dist = tf_type_dist[tf_type_dist['customer-name'] == 'residential_ev']
    tf_type_energy = pd.DataFrame(tf_type_dist[['broker-name', 'tariff-type', 'transaction-kWh']]
                                  .groupby(by = ['broker-name', 'tariff-type']).sum())
    tf_type_energy = tf_type_energy.reset_index()
    tf_type_energy.columns = ['broker', 'tariff-type', 'energy']
    tf_type_energy['energy'] = tf_type_energy['energy'].apply(lambda x: abs(x))

    tf_type_energy = tf_type_energy.pivot(columns='tariff-type', index='broker')
    tf_type_energy.columns = tf_type_energy.columns.swaplevel().map(' '.join)
    tf_type_energy = tf_type_energy.replace(np.nan,0)
    tf_type_energy = tf_type_energy.reset_index()

    tf_types_energy = tf_type_energy.loc[:, tf_type_energy.columns != "broker"]
    df_melt_energy = pd.melt(tf_type_energy, id_vars=['broker'], value_vars=tf_types_energy.columns.tolist())


    # after checking: each customer appears in each timeslot atleast once
    tf_type_subs = tf_type_dist[['timeslot'
                                    , 'broker-name', 'tariff-id'
                                    , 'tariff-type', 'customer-name'
                                    , 'customer-count']
                                  ][tf_type_dist['customer-count'] > 0].copy()
    tf_type_subs = tf_type_subs.drop_duplicates(keep='first')
    tf_type_subs = tf_type_subs[['customer-count', 'broker-name', 'tariff-type']].groupby(by = ['broker-name', 'tariff-type']).sum()
    tf_type_subs = tf_type_subs.reset_index()
    tf_type_subs.columns = ['broker', 'tariff-type', 'count']
    tf_type_subs['count'] = tf_type_subs['count'].apply(lambda x: round(x/24, 2))

    tf_type_subs = tf_type_subs.pivot(columns='tariff-type', index='broker')
    tf_type_subs.columns = tf_type_subs.columns.swaplevel().map(' '.join)
    tf_type_subs = tf_type_subs.replace(np.nan,0)
    tf_type_subs = tf_type_subs.reset_index()

    tf_types_subs = tf_type_subs.loc[:, tf_type_subs.columns != "broker"]
    df_melt_subs = pd.melt(tf_type_subs, id_vars=['broker'], value_vars=tf_types_subs.columns.tolist())
    
    return [df_melt_count, df_melt_energy, df_melt_subs]