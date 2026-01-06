import matplotlib
matplotlib.use("Agg") 

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/v_kpi_02_roi_by_genre.csv")
df = df.sort_values("avg_roi")

plt.figure(figsize=(10, 6))
plt.barh(df["genre_name"], df["avg_roi"])
plt.title("ROI promedio por género")
plt.xlabel("ROI promedio")
plt.ylabel("Género")
plt.tight_layout()

plt.savefig("screenshots/kpi_02_roi_by_genre.png", dpi=150)
plt.close()