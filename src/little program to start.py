import matplotlib.pyplot as plt

# --- General EV parameters ---
battery_capacity_kwh = 70
min_participation_soc = 0.20
max_participation_soc = 0.80
charge_power_kw = 11
num_evs_per_parking = 10

# --- Use Cases: each is a full parking with 10 EVs ---
use_cases = {
    "home": {
        "arrival": 18,
        "departure": 8,
        "initial_soc": 0.40,
        "target_soc": 0.90
    },
    "work": {
        "arrival": 8,
        "departure": 16,
        "initial_soc": 0.30,
        "target_soc": 0.60
    },
    "shopping": {
        "arrival": 10,
        "departure": 13,
        "initial_soc": 0.70,
        "target_soc": 0.75
    }
}

# --- Store results for graph ---
total_up_flex = 0
total_down_flex = 0
labels = []
up_values = []
down_values = []

for uc_name, uc in use_cases.items():
    arrival = uc["arrival"]
    departure = uc["departure"]
    initial_soc = uc["initial_soc"]
    target_soc = uc["target_soc"]

    if departure < arrival:
        connected_hours = (24 - arrival) + departure
    else:
        connected_hours = departure - arrival

    initial_energy = initial_soc * battery_capacity_kwh
    target_energy = target_soc * battery_capacity_kwh
    required_energy = target_energy - initial_energy
    max_energy = max_participation_soc * battery_capacity_kwh
    min_energy = min_participation_soc * battery_capacity_kwh

    up_flex = max(0, max_energy - target_energy)
    down_flex = max(0, initial_energy - min_energy)

    max_possible_energy = charge_power_kw * connected_hours
    up_flex = min(up_flex, max_possible_energy)
    down_flex = min(down_flex, max_possible_energy)

    total_uc_up = up_flex * num_evs_per_parking
    total_uc_down = down_flex * num_evs_per_parking

    total_up_flex += total_uc_up
    total_down_flex += total_uc_down

    labels.append(uc_name.capitalize())
    up_values.append(total_uc_up)
    down_values.append(total_uc_down)

    print(f"\n--- {uc_name.upper()} ---")
    print(f"Connected time: {connected_hours} h")
    print(f"Initial SoC: {initial_soc*100:.0f}%, Target SoC: {target_soc*100:.0f}%")
    print(f"Required energy per EV: {required_energy:.2f} kWh")
    print(f"Upward flexibility: {up_flex:.2f} kWh/EV → Total: {total_uc_up:.2f} kWh")
    print(f"Downward flexibility: {down_flex:.2f} kWh/EV → Total: {total_uc_down:.2f} kWh")

# --- Summary ---
print("\n====== TOTAL FLEXIBILITY (sum of all parkings) ======")
print(f"➡️  Total Upward Flexibility: {total_up_flex:.2f} kWh")
print(f"⬅️  Total Downward Flexibility: {total_down_flex:.2f} kWh")

# --- Plot chart ---
x = range(len(labels))
plt.figure(figsize=(8, 5))
plt.bar(x, up_values, label="Upward Flexibility")
plt.bar(x, down_values, bottom=up_values, label="Downward Flexibility")
plt.xticks(x, labels)
plt.ylabel("Flexibility (kWh)")
plt.title("Flexibility Potential per Use Case (10 EVs each)")
plt.legend()
plt.tight_layout()
plt.show()

