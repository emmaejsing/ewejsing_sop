import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import sys

path = Path(r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_simple\output\output__DK_hourly_simple.xlsx")
df = pd.read_excel(path, sheet_name="efct_h", usecols="N:LXM", index_col=None, skiprows=6, header=None).T

h = pd.read_excel(path, sheet_name="efct_h", usecols="G:L", index_col=None, skiprows=5, header=0)
ix = h.ener == "elec"
data = df.loc[:, ix]

data.index = range(52 * 168)
data.columns = h.loc[ix, "tchL"]
data.columns.name = None

colors = {"Consumption": "#F1948A", "DSR": "#8E44AD", "Solceller": "#FFC300", "Landvind": "#2ECC71",
          "Havvind": "#3498DB", "Elektrolyse": "#C0392B", "Brintturbine": "#909497"}


def get_balance_plot(ax, week, hours_to_display, show_legend=True):
    start_hour = week * 7 * 24
    end_hour = start_hour + hours_to_display
    plot_data = data.iloc[start_hour:end_hour, :] / 1000
    plot_data.index = range(hours_to_display)

    plot_data.plot(kind="bar", stacked=True, color=colors, ax=ax, rot=0, legend=show_legend, zorder=3)
    if show_legend:
        ax.legend(loc='upper left', ncol=3)
    ax.set_title(f"Elproduktion og -forbrug time for time (uge {week})")
    ax.set_xlabel("Time")
    ax.set_ylabel("GW")
    ax.set_ylim(-35, 35)
    ax.grid(zorder=0)
    return ax


fig, axs = plt.subplots(1, 2, figsize=(16, 9))
get_balance_plot(week=25, hours_to_display=24, ax=axs[0])
get_balance_plot(week=19, hours_to_display=24, ax=axs[1], show_legend=False)

plt.savefig("24_hour_energy_balance.png")
plt.show()
