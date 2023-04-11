from typing import NewType
from pandas import DataFrame

TariffTransactionFrame = NewType('TariffTransactionFrame', DataFrame)
""" Schema exported by TariffTransaction exporter
    Fields:
        timeslot: int
        broker-name: str
        tariff-id: long
        tariff-type: str
        transaction-kWh: float
        customer-name: str
        customer-count: float
"""

# problem: the columns change depending on which brokers are involved
BalancingActionFrame = NewType('BalancingActionFrame', DataFrame)
""" Schema exported by BalancingAction exporter
    Fields:
        ts: int
        pPlus: long	
        pMinus: long	
        totalImbalance: int	
        rmBase: long	
        rmActual: long	
        brokerX: str	
        netLoadX: int
        regOfferedX: long	
        regUsedX: long	
        baseCostX: long	
        p1X: long	
        p2X: long	
"""


TariffCountFrame = NewType('TariffCountFrame', DataFrame)
""" Number of (unique) tariffs per broker and tariff type
    Fields:
        broker: str
        tariff-type: str
        count: long
"""


TariffEnergyFrame = NewType('TariffEnergyFrame', DataFrame)
""" Amount of energy per broker and tariff type
    Fields:
        broker: str
        tariff-type: str
        energy: long
"""

TariffSubscriberFrame = NewType('TariffSubscriberFrame', DataFrame)
""" Amount of subscriber days per broker and tariff type
    Fields:
        broker: str
        tariff-type: str
        count: long
"""

TariffPriceFrame = NewType('TariffPriceFrame', DataFrame)
""" Average price per kwh per broker and tariff type
    Fields:
        broker: str
        tariff-type: str
        avg_price: long
"""

TariffRegulationTransactionFrame = NewType('TariffRegulationTransactionFrame', DataFrame)
""" Tariff transactions (energy and charge per timeslot) per broker, tariff-type and transaction-type
    Fields:
        timeslot: int
        broker-name: str
        tariff-type: str
        transaction-type: str
        transaction-kWh: long
        transaction-charge: long
"""

PivotBalancingActionFrame = NewType('PivotBalancingActionFrame', DataFrame)
""" Certain Balancing actions per broker and timeslot
    Fields:
        ts: int
        pPlus: long
        pMinus: long
        totalImbalance: int
        broker: str
        netLoad: int
        regOffered: long
        regUsed: long
        baseCost: long
        p1: long
        p2: long	
"""

MatchedTransactionFrame = NewType('MatchedTransactionFrame', DataFrame)
""" Balancing Actions and corresponding Tariff Transaction per broker and timeslot
    Fields:
        ts: int
        broker: str
        tariff-type: str
        transaction-type: str
        transaction-kWh: long
        transaction-charge: long
        pPlus: long
        pMinus: long
        totalImbalance: int
        netLoad: int
        regOffered: long
        regUsed: long
        baseCost: long
        p1: long
        p2: long	
"""

ImbalanceAmountFrame = NewType('ImbalanceAmountFrame', DataFrame)
""" Total imbalance per timeslot
    Fields:
        ts: int
        totalImbalance: int
"""

RegulationAmountFrame = NewType('RegulationAmountFrame', DataFrame)
""" Total regulation per timeslot
    Fields:
        ts: int
        regUsed: long
"""

ImbalanceRegulationFrame = NewType('ImbalanceRegulationFrame', DataFrame)
""" Total regulation and imbalance and therefore reduced imbalance per hour
    Fields:
        ts: int
        regUsed: long
        totalImbalance: int
        hour: int
        perc: long
"""

EnergyProfitFrame = NewType('EnergyProfitFrame', DataFrame)
""" Total energy traded and profit during balancing per broker
    Fields:
        broker: str
        regUsed: long
        p2: long
        transaction-charge: long
        profit: long
"""

melt_energy_up_and_down_per_broker = pd.melt(energy_and_profit_up_and_down, id_vars=['broker'], value_vars=['upReg', 'downReg'])
melt_profit_up_and_down_per_broker = pd.melt(energy_and_profit_up_and_down, id_vars=['broker'], value_vars=['pUp_fromBroker', 'profit_x', 'pDown_toBroker', 'profit_y'])

EnergyRegulationMeltFrame = NewType('EnergyRegulationMeltFrame', DataFrame)
""" Energy per broker from both up- and down-regulation
    Fields:
        broker: str
        upReg: long
        downReg: long
"""

ProfitRegulationMeltFrame = NewType('ProfitRegulationMeltFrame', DataFrame)
""" Payments and profit per broker from both up- and down-regulation
    Fields:
        broker: str
        pUp_fromBroker: long
        profit_x: long
        pDown_toBroker: long 
        profit_y: long
"""