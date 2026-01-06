import matplotlib
matplotlib.use("Agg")  # backend no interactivo

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/v_kpi4.csv")

# Ordenar por popularidad descendente
df = df.sort_values("total_popularity", ascending=False)

# Quedarse con los top N géneros para que el gráfico sea legible
top_n = 6
df_top = df.head(top_n)

# Agrupar el resto como "Otros"
others_popularity = df.iloc[top_n:]["total_popularity"].sum()

df_pie = pd.concat([
    df_top,
    pd.DataFrame([{
        "genre_name": "Otros",
        "total_popularity": others_popularity
    }])
])

# Crear gráfico de torta
plt.figure(figsize=(8, 8))
plt.pie(
    df_pie["total_popularity"],
    labels=df_pie["genre_name"],
    autopct="%1.1f%%",
    startangle=140
)

plt.title("Distribución de popularidad por género")

plt.tight_layout()

# Guardar imagen
plt.savefig("screenshots/kpi_04_genres_popularity_pie.png", dpi=150)

# Cerrar figura
plt.close()
