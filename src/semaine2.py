import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Set Plotly renderer to display directly in supported environments
pio.renderers.default = 'svg'  # Options: 'browser', 'svg', 'notebook', etc.

class Vehicle:
    def __init__(self, soc_arrival, soc_departure, battery_capacity, arrival_hour, departure_hour):
        self.soc = soc_arrival * battery_capacity
        self.soc_target = soc_departure * battery_capacity
        self.battery_capacity = battery_capacity
        self.arrival_hour = arrival_hour
        self.departure_hour = departure_hour

    def is_connected(self, hour):
        return self.arrival_hour <= hour < self.departure_hour or self.departure_hour < self.arrival_hour <= hour

    def charge(self, amount):
        chargeable = min(amount, self.battery_capacity - self.soc)
        self.soc += chargeable
        return chargeable

    def discharge(self, amount):
        dischargeable = min(amount, self.soc - self.soc_target)
        self.soc -= dischargeable
        return dischargeable

    def get_soc_percent(self):
        return round((self.soc / self.battery_capacity) * 100, 1)

class EnergySystem:
    def __init__(self, house_demand, pv_production, max_power):
        self.house_demand = house_demand
        self.pv_production = pv_production
        self.max_power = max_power

    def get_demand(self, hour):
        return self.house_demand[hour]

    def get_pv(self, hour):
        return self.pv_production[hour]

class Simulation:
    def __init__(self, vehicle, system):
        self.vehicle = vehicle
        self.system = system
        self.hours = list(range(24))
        self.v2h = [0]*24
        self.charge = [0]*24
        self.soc = []
        self.blocked = [0]*24

    def run_day(self):
        for h in self.hours:
            soc_before = self.vehicle.soc
            if self.vehicle.is_connected(h):
                if self.vehicle.soc > self.vehicle.soc_target:
                    v2h_power = min(self.system.get_demand(h), self.system.max_power)
                    self.v2h[h] = self.vehicle.discharge(v2h_power)
                else:
                    self.blocked[h] = 1

                surplus_pv = self.system.get_pv(h) - self.system.get_demand(h)
                if surplus_pv > 0:
                    self.charge[h] = self.vehicle.charge(min(surplus_pv, self.system.max_power))
            self.soc.append(self.vehicle.get_soc_percent())

    def export_results(self):
        return pd.DataFrame({
            "Hour": self.hours,
            "House Demand": self.system.house_demand,
            "PV Production": self.system.pv_production,
            "V2H Energy": self.v2h,
            "Charge from PV": self.charge,
            "SoC (%)": self.soc,
            "Blocked (Insufficient SoC)": self.blocked
        })

    def plot_results(self, df):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df["Hour"], y=df["House Demand"], name="House Demand", marker_color="lightgray"))
        fig.add_trace(go.Bar(x=df["Hour"], y=df["V2H Energy"], name="V2H Energy", marker_color="green"))
        fig.add_trace(go.Bar(x=df["Hour"], y=df["Charge from PV"], name="Charge", marker_color="red"))
        fig.add_trace(go.Bar(x=df["Hour"], y=df["PV Production"], name="PV", marker_color="orange"))
        fig.add_trace(go.Scatter(x=df["Hour"], y=df["SoC (%)"], mode="lines+markers", name="SoC", marker_color="blue"), secondary_y=True)
        fig.update_layout(title="V2H Daily Simulation (OOP Version)", xaxis_title="Hour", yaxis_title="Energy (kWh)",
                          barmode="overlay")
        fig.update_yaxes(title_text="State of Charge (%)", secondary_y=True)
        fig.show()

# --------- TEST & VISUALISATION SEULE ---------
if __name__ == "__main__":
    vehicle = Vehicle(soc_arrival=0.5, soc_departure=0.6, battery_capacity=70, arrival_hour=18, departure_hour=7)
    house_demand = [0.5]*6 + [1.0]*2 + [2.5]*4 + [1.5]*4 + [2.0]*6 + [0.5]*2
    pv_production = [0]*6 + [1.0]*3 + [2.5]*5 + [1.5]*4 + [0.5]*6
    system = EnergySystem(house_demand=house_demand, pv_production=pv_production, max_power=11)

    sim = Simulation(vehicle, system)
    sim.run_day()
    df = sim.export_results()
    sim.plot_results(df)  # ✅ Affiche le graphique Plotly