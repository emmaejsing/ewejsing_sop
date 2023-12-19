import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

path = Path(r"C:\Users\ewejs\local_peers_data\scenarios\DK_hourly_simple\output\output__DK_hourly_simple.xlsx")
df = pd.read_excel(path, sheet_name="volu_h", usecols="N:LXM", index_col=None, skiprows=6, nrows=1, header=None).T

df.columns = ["volumen"]
df["volumen"] = df["volumen"] / 1e6

df.plot(lw=2, color="#008080")
plt.title("Udvikling af brintlager")
plt.xlabel("Timer på året")
plt.ylabel("TWh")
plt.grid()
plt.show()
plt.savefig("brintlager.png")
