import pandas as pd
import numpy as np

'''
    Transformer for KPI3 tariff type KPIs with command line arguments. Returns for each tariff type the publish-count, energy-amount, subs-
    number in days and avg_price per kWh.
'''

def kpi3_transformer(tf_transactions, customers, game):
    
    # filter out customers if given
    
    if (customers != "any"):
        customer_list = customers.split(",")
        tf_transactions = tf_transactions[tf_transactions['customer-name'].isin(customer_list)]
        
    tf_type_dist = tf_transactions[
        [
            "timeslot",
            "broker-name",
            "tariff-id",
            "tariff-type",
            "transaction-kWh",
            "customer-name",
            "customer-count",
        ]
    ].copy()
    
    # calculate number of unique tariff ids published, in case of given customer-name shows the actually subscribed number of tariffs for that customer group
    
    tf_type_count = pd.DataFrame(
        tf_type_dist[["broker-name", "tariff-type", "tariff-id"]]
        .groupby(by=["broker-name", "tariff-type"])["tariff-id"]
        .nunique()
    )
    tf_type_count = tf_type_count.reset_index()
    tf_type_count.columns = ["broker", "tariff-type", "count"]

    # calculate the energy traded
    tf_type_energy = pd.DataFrame(
        tf_type_dist[["broker-name", "tariff-type", "transaction-kWh"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum()
    )
    tf_type_energy = tf_type_energy.reset_index()
    tf_type_energy.columns = ["broker", "tariff-type", "energy"]
    tf_type_energy["energy"] = tf_type_energy["energy"].apply(lambda x: abs(x))

    # calculate the number of subscriber days
    tf_type_subs = tf_type_dist[
        [
            "timeslot",
            "broker-name",
            "tariff-id",
            "tariff-type",
            "customer-name",
            "customer-count",
        ]
    ][tf_type_dist["customer-count"] > 0].copy()
    tf_type_subs = tf_type_subs.drop_duplicates(keep="first")
    tf_type_subs = (
        tf_type_subs[["customer-count", "broker-name", "tariff-type"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum()
    )
    tf_type_subs = tf_type_subs.reset_index()
    tf_type_subs.columns = ["broker", "tariff-type", "count"]
    tf_type_subs["count"] = tf_type_subs["count"].apply(lambda x: round(x / 24, 2))
    
    # calculate the average price per kWh
    tf_df = tf_transactions[tf_transactions["transaction-type"] != "PUBLISH"].copy()
    tf_df["transaction-kWh"] = np.where(
        (tf_df["transaction-regulation"] == 1)
        & (tf_df["transaction-type"] == "PRODUCE"),
        0,
        tf_df["transaction-kWh"],
    )
    tf_type_price = pd.DataFrame(
        tf_df[["broker-name", "tariff-type", "transaction-kWh", "transaction-charge"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum()
    )
    tf_type_price = tf_type_price.reset_index()
    tf_type_price.columns = ["broker", "tariff-type", "energy", "price"]
    tf_type_price["energy"] = tf_type_price["energy"].apply(lambda x: abs(x)) # absolute value because price already indicates the direction
    tf_type_price["avg_price"] = tf_type_price["price"] / tf_type_price["energy"]
    tf_type_price = tf_type_price.drop(columns=["energy", "price"])

    return [tf_type_count, tf_type_energy, tf_type_subs, tf_type_price]
