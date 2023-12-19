import sys
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# List of Excel file paths (Copy the individual file paths from Windows File Explorer with SHIFT + right click -> select "Copy as path")
# Remember to include the letter 'r' in front of the path.
excel_files = {
    "simple": Path(r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_simple\output\output__DK_hourly_simple.xlsx"),
    "batt": Path(r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_batt\output\output__DK_hourly_batt.xlsx"),
    "new_cap": Path(
        r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_new_cap\output\output__DK_hourly_new_cap.xlsx"),
    "high_eff_elyz": Path(
        r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_high_eff_elyz\output\output__DK_hourly_high_eff_elyz.xlsx"),
    # More lines with pairs of scenario names and path can be added here.. (remember to separate lines by commas)
    }

# Dictionary to store data from each file
data_assets = {}
data_balance = {}

# Loop through each file
for label, file in excel_files.items():
    # Read the specified range from the specified sheet
    df = pd.read_excel(file, sheet_name='balance', usecols="B:R", skiprows=5)
    # Store the DataFrame in the dictionary
    data_balance[label] = df

    # Read the specified range from the specified sheet
    df = pd.read_excel(file, sheet_name='assets', usecols="B:AP", skiprows=5)
    # Store the DataFrame in the dictionary
    data_assets[label] = df

# Retrieve specific output

# Installed capacities

res = []

for label in excel_files:
    data = data_assets[label].query("role != 'dsch'")[['asst', 'capa']]
    data = data.set_index('asst')
    data.index.name = None
    res.append(data)

df = pd.concat(res, axis=1, join='outer').fillna(0)
df.columns = excel_files.keys()
print(df)
# Renaming and reordering index

mapping = {'Landvind': 'DK12_prim_wndN',
           'Solceller': 'DK12_prim_soPV',
           'Forbrugsfleksibilitet': 'DK12_prim_peak',
           'Brintlager': 'DK12_stor_h2pr',
           'Havvind': 'DK12_prim_wndF',
           'Elektrolyse': 'DK12_tfrm_elyz',
           'Brintturbiner': 'DK12_tfrm_ht42',
           'Batterier': 'DK12_stor_batt'
           }

index_mapping = {value: key for key, value in mapping.items()}
df = df.rename(index=index_mapping)

# Renaming columns

column_mapping = dict(simple="Basisscenario", batt="Med batterier")
df = df.rename(columns=column_mapping)
df = df.reindex(mapping.keys())

df.plot(kind="bar", color="#008080", zorder=3)
plt.grid(zorder=0)
plt.title("Kapaciteter af teknologier")
# plt.xlabel("Timer på året")
# plt.ylabel("TWh")
plt.show()

df.to_excel("results_capacities.xlsx")

# Total system costs

res = []
for label in excel_files:
    system_costs = -float(data_assets[label].loc[:, ['expV', 'expF', 'expC']].sum().sum()) / 1e9
    res.append({'scenario': label, 'total_system_costs': system_costs})

df = pd.DataFrame(res)
print(df)
df.to_excel("results_system_costs.xlsx")
sys.exit()
# Total expense for final energy demand

res = []
for label in excel_files:
    cost_elec = -float(data_balance[label].query("tchL == 'Consumption' & ener == 'elec'").cash) / 1e9
    cost_h2pr = -float(data_balance[label].query("tchL == 'Consumption' & ener == 'h2pr'").cash) / 1e9
    res.append({'scenario': label, 'cost_elec': cost_elec, 'cost_h2pr': cost_h2pr, 'cost_total': cost_elec + cost_h2pr})

df = pd.DataFrame(res)
print(df)
df.to_excel("results_total_expenses.xlsx")
