# ✅ V2H Streamlit App – version avec sélection du jour en simulation journalière

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

battery_capacity = 70
min_soc = 0.2
max_soc = 0.8
max_charge = 11
max_discharge = 11
price_peak = 0.20
price_offpeak = 0.10
price_normal = 0.20

base_demand = [
    0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.6, 0.8, 1.2, 1.5,
    1.0, 0.8, 0.6, 0.5, 0.5, 0.6, 1.2, 1.5, 1.3, 1.0,
    0.8, 0.7, 0.6, 0.5
]

pv_production = [
    0, 0, 0, 0, 0, 0.2, 0.5, 1.2, 2.5, 4.0,
    4.5, 4.2, 3.8, 3.2, 2.0, 1.0, 0.4, 0.1, 0, 0,
    0, 0, 0, 0
]

off_peak_hours = list(range(0, 6)) + list(range(22, 24))

def default_schedule():
    return {
        day: {"arrival": 18, "departure": 7, "soc_in": 0.5, "soc_out": 0.8}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }

def init_state():
    if "vehicles" not in st.session_state:
        st.session_state.vehicles = {"VE 1": default_schedule()}
    if "selected_vehicle" not in st.session_state:
        st.session_state.selected_vehicle = "VE 1"
    if "events" not in st.session_state:
        st.session_state.events = []

init_state()

def simulate_day(soc_in, soc_out, blocked_hours=None):
    energy = soc_in * battery_capacity
    target = soc_out * battery_capacity
    soc = []
    v2h = []
    charge = []
    pv_used = []

    min_energy = min_soc * battery_capacity
    for h in range(24):
        demand = base_demand[h]
        pv = pv_production[h]
        is_peak = demand > 1.0
        is_connected = not blocked_hours or h not in blocked_hours

        v2h_now = 0
        charge_now = 0
        pv_now = 0

        if is_connected:
            if is_peak and energy > min_energy:
                v2h_now = min(demand, max_discharge, energy - min_energy)
                energy -= v2h_now
            elif (h in off_peak_hours or pv > 0) and energy < target:
                charge_from_grid = min(max_charge, target - energy)
                charge_from_pv = min(pv, charge_from_grid)
                pv_now = charge_from_pv
                charge_now = charge_from_grid
                energy += charge_now

        v2h.append(v2h_now)
        charge.append(charge_now)
        soc.append(round(energy * 100 / battery_capacity, 2))
        pv_used.append(pv_now)

    return v2h, charge, soc, pv_used

def simulate_period(schedule, days=30, events=[]):
    daily_results = []
    weekdays = list(schedule.keys())
    for i in range(days):
        day = weekdays[i % 7]
        s = schedule[day]
        blocked = [e for e in events if e["day"] == f"Day {i+1}"]
        blocked_hours = []
        for e in blocked:
            blocked_hours.extend(range(e["start_hour"], e["end_hour"]))
        v2h, charge, soc, pv_used = simulate_day(s["soc_in"], s["soc_out"], blocked_hours)
        daily_results.append({"day": day, "v2h": sum(v2h), "charge": sum(charge), "soc_end": soc[-1], "pv": sum(pv_used)})
    return daily_results

st.set_page_config(page_title="V2H Simulation", layout="wide")
st.title("🚗 V2H Simulation Dashboard")

menu = st.sidebar.radio("Menu", ["📅 Planning", "📊 Day Simulation", "📆 Weekly/Monthly View", "💶 Savings"])

ve_list = list(st.session_state.vehicles.keys())
selected = st.sidebar.selectbox("Select vehicle", ve_list)
st.session_state.selected_vehicle = selected

if st.sidebar.button("➕ Add vehicle"):
    new_name = f"VE {len(st.session_state.vehicles)+1}"
    st.session_state.vehicles[new_name] = default_schedule()
    st.session_state.selected_vehicle = new_name

if menu == "📅 Planning":
    st.subheader(f"🗓 Weekly Planning – {selected}")
    for day in st.session_state.vehicles[selected].keys():
        values = st.session_state.vehicles[selected][day]
        with st.expander(f"{day}"):
            col1, col2 = st.columns([1, 1])

            st.markdown("#### 🏁 Vehicle Departure")
            with col1:
                d = st.number_input(f"Departure hour ({day})", 0, 23, value=values["departure"], key=f"dep_{day}")
                s_out = st.slider(f"SoC on departure ({day}) (%)", 0, 100, int(values["soc_out"] * 100), step=1, key=f"soco_{day}_out")

            st.markdown("#### 🚗 Vehicle Arrival")
            with col2:
                a = st.number_input(f"Arrival hour ({day})", 0, 23, value=values["arrival"], key=f"arr_{day}")
                s_in = st.slider(f"SoC on arrival ({day}) (%)", 0, 100, int(values["soc_in"] * 100), step=1, key=f"soci_{day}_in")

            st.session_state.vehicles[selected][day] = {
                "arrival": a,
                "departure": d,
                "soc_in": s_in / 100,
                "soc_out": s_out / 100
            }

    st.markdown("---")
    st.subheader("🛒 Exceptional Events")
    with st.form("event_form"):
        d = st.text_input("Day concerned (ex: Day 5)")
        start = st.number_input("Start hour", 0, 23)
        end = st.number_input("End hour", 1, 24)
        if st.form_submit_button("Add event"):
            st.session_state.events.append({"day": d, "start_hour": start, "end_hour": end})
            st.success("Event added ✅")

elif menu == "📊 Day Simulation":
    st.subheader("📊 Daily Simulation")
    days_of_week = list(st.session_state.vehicles[selected].keys())
    chosen_day = st.selectbox("Choose a day", days_of_week)
    s = st.session_state.vehicles[selected][chosen_day]
    v2h, charge, soc, pv = simulate_day(s["soc_in"], s["soc_out"])
    df = pd.DataFrame({"Hour": range(24), "House Demand": base_demand, "V2H": v2h, "Charge": charge, "SoC": soc, "PV Used": pv})

    fig, ax1 = plt.subplots()
    ax1.bar(df["Hour"], df["House Demand"], label="House Demand", color="lightgray")
    ax1.bar(df["Hour"], df["V2H"], label="V2H", color="green")
    ax1.bar(df["Hour"] + 0.3, df["Charge"], width=0.4, label="Charge", color="red")
    ax2 = ax1.twinx()
    ax2.plot(df["Hour"], df["SoC"], label="SoC", color="blue")
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Energy (kWh)")
    ax2.set_ylabel("State of Charge (%)")
    fig.legend()
    st.pyplot(fig)
    st.dataframe(df)

elif menu == "📆 Weekly/Monthly View":
    st.subheader("📆 Period Simulation")
    days = st.selectbox("Select period", [7, 30])
    results = simulate_period(st.session_state.vehicles[selected], days, st.session_state.events)
    df = pd.DataFrame(results)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(df.index, df["v2h"], label="V2H", color="green")
    ax1.bar(df.index, df["charge"], bottom=df["v2h"], label="Charge", color="red", alpha=0.5)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df["soc_end"], label="SoC", color="blue", marker='o')
    st.pyplot(fig)

elif menu == "💶 Savings":
    st.subheader("💶 Estimated Savings")
    res = simulate_period(st.session_state.vehicles[selected], 30, st.session_state.events)
    v2h_total = sum([r["v2h"] for r in res])
    recharge_total = sum([r["charge"] for r in res])
    pv_used = sum([r["pv"] for r in res])

    save_v2h = v2h_total * price_peak
    save_charge = recharge_total * (price_normal - price_offpeak)
    st.metric("Total V2H Provided (kWh)", f"{v2h_total:.1f}")
    st.metric("Charging Energy (kWh)", f"{recharge_total:.1f}")
    st.metric("Charging from PV (kWh)", f"{pv_used:.1f}")
    st.success(f"💰 Total estimated savings: {save_v2h + save_charge:.2f} €")
