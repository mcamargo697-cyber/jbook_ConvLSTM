# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. PARÁMETROS
# =========================================================
SECTOR = "X6By5"
GRID_STEP_PLOT = 100   # dibujar una línea de malla cada 100 celdas

# Ruta al npz de la grilla base
ruta_grid_base = rf"C:\Users\Victus\Documents\RedesNeuronales\6_RNN_Batimetrias\ConvLSTM\X6By5\1_MallasInterpoladas_X6By5\grid_base_X6By5_5m.npz"

# Ruta a uno de los campos interpolados ya guardados
ruta_npz_interpolado = rf"C:\Users\Victus\Documents\RedesNeuronales\6_RNN_Batimetrias\ConvLSTM\X6By5\1_MallasInterpoladas_X6By5\batimetria_interpolada_X6By5_20240618.npz"

# Carpeta de salida
carpeta_salida = rf"C:\Users\Victus\Documents\RedesNeuronales\6_RNN_Batimetrias\ConvLSTM\jbook_LSMTConv\docs\images"
os.makedirs(carpeta_salida, exist_ok=True)

nombre_figura = "campo_interpolado_con_malla_base.png"


# =========================================================
# 2. LEER NPZ DE MALLA BASE
# =========================================================
grid_data = np.load(ruta_grid_base)

gx = grid_data["gx"]               # coordenadas x de la malla en sistema rotado
gy = grid_data["gy"]               # coordenadas y de la malla en sistema rotado
mask_grid = grid_data["mask_grid"] # máscara 2D de celdas válidas
centroide = grid_data["centroide"] # centroide del polígono
u = grid_data["u"]                 # eje dirección canal
v = grid_data["v"]                 # eje perpendicular

# Reconstruir coordenadas reales X,Y de la malla completa
X_real = centroide[0] + gx * v[0] + gy * u[0]
Y_real = centroide[1] + gx * v[1] + gy * u[1]


# =========================================================
# 3. LEER CAMPO INTERPOLADO
# =========================================================
campo_data = np.load(ruta_npz_interpolado)

z_grid = campo_data["z_grid"]

# Extraer metadatos si existen
fecha = campo_data["fecha"][0] if "fecha" in campo_data else "sin_fecha"
source_type = campo_data["source_type"][0] if "source_type" in campo_data else "NA"


# =========================================================
# 4. GRAFICAR CAMPO + MALLA ESPACIADA
# =========================================================
fig, ax = plt.subplots(figsize=(12, 8))

# Campo interpolado
pcm = ax.pcolormesh(
    X_real,
    Y_real,
    z_grid,
    shading="auto"
)
cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label("Cota / profundidad")

# Dibujar submalla espaciada
nrows, ncols = gx.shape

# Líneas "horizontales"
for i in range(0, nrows, GRID_STEP_PLOT):
    ax.plot(
        X_real[i, :],
        Y_real[i, :],
        linewidth=0.5,
        alpha=0.6
    )

# Líneas "verticales"
for j in range(0, ncols, GRID_STEP_PLOT):
    ax.plot(
        X_real[:, j],
        Y_real[:, j],
        linewidth=0.5,
        alpha=0.6
    )

# Bordes finales para cerrar la submalla visual
ax.plot(X_real[-1, :], Y_real[-1, :], linewidth=0.5, alpha=0.6)
ax.plot(X_real[:, -1], Y_real[:, -1], linewidth=0.5, alpha=0.6)

# Formato
ax.set_title(f"Campo batimétrico interpolado sobre la malla regular\nFecha: {fecha} | Tipo: {source_type}")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_aspect("equal")

plt.tight_layout()

# Guardar figura
ruta_salida_fig = os.path.join(carpeta_salida, nombre_figura)
plt.savefig(ruta_salida_fig, dpi=300, bbox_inches="tight")
plt.show()

print(f"Figura guardada en:\n{ruta_salida_fig}")





