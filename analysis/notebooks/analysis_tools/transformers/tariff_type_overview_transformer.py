import pandas as pd
import numpy as np

'''
    Transformer for KPI3 tariff type KPIs with command line arguments. Returns for each tariff type the publish-count, energy-amount, subs-
    number in days and avg_price per kWh.
'''

def unique_published_tariff_count(transactions):
    # calculate number of unique tariff ids published, in case of given customer-name shows the actually subscribed number of tariffs for that customer group
    counted = pd.DataFrame(
        transactions[["broker-name", "tariff-type", "tariff-id"]]
        .groupby(by=["broker-name", "tariff-type"])["tariff-id"]
        .nunique())
    counted = counted.reset_index()
    counted.columns = ["broker", "tariff-type", "count"]
    return counted

def traded_energy(transactions):
    # calculate the energy traded
    sum_energy = pd.DataFrame(
        transactions[["broker-name", "tariff-type", "transaction-kWh"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum())
    sum_energy = sum_energy.reset_index()
    sum_energy.columns = ["broker", "tariff-type", "energy"]
    sum_energy["energy"] = sum_energy["energy"].apply(lambda x: abs(x))
    return sum_energy

def subscriber_days(transactions):
    # calculate the number of subscriber days
    subscribers = transactions[
        [
            "timeslot",
            "broker-name",
            "tariff-id",
            "tariff-type",
            "customer-name",
            "customer-count",
        ]
    ][transactions["customer-count"] > 0].copy()
    subscribers = subscribers.drop_duplicates(keep="first")
    subscribers = (
        subscribers[["customer-count", "broker-name", "tariff-type"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum()
    )
    subscribers = subscribers.reset_index()
    subscribers.columns = ["broker", "tariff-type", "count"]
    subscribers["count"] = subscribers["count"].apply(lambda x: round(x / 24, 2))
    return subscribers

def average_price_per_kwh(transactions):
    # calculate the average price per kWh
    price_per_kwh = transactions[transactions["transaction-type"] != "PUBLISH"].copy()

    # set energy amount of curtailment transactions to 0, as no energy is bought or sold
    price_per_kwh["transaction-kWh"] = np.where(
        (price_per_kwh["transaction-regulation"] == 1)
        & (price_per_kwh["transaction-type"] == "PRODUCE"),
        0,
        price_per_kwh["transaction-kWh"],
        )
    price_per_kwh = pd.DataFrame(
        price_per_kwh[["broker-name", "tariff-type", "transaction-kWh", "transaction-charge"]]
        .groupby(by=["broker-name", "tariff-type"])
        .sum()
    )
    price_per_kwh = price_per_kwh.reset_index()
    price_per_kwh.columns = ["broker", "tariff-type", "energy", "price"]
    price_per_kwh["energy"] = price_per_kwh["energy"].apply(lambda x: abs(x)) # absolute value because price already indicates the direction
    price_per_kwh["avg_price"] = price_per_kwh["price"] / price_per_kwh["energy"]
    price_per_kwh = price_per_kwh.drop(columns=["energy", "price"])
    return price_per_kwh