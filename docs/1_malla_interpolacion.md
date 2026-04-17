# Malla de interpolación

Interpolar los datos batimétricos sobre una malla espacial regular, con el fin de obtener una representación continua y estructurada de la batimetría para su uso en modelos espaciotemporales.

## Entradas

- Datos batimétricos en formato XYZ (coordenadas X, Y, profundidad Z).
- Polígono del área común de análisis.

## Proceso

El procedimiento implementado se desarrolla en las siguientes etapas:

1. Lectura y organización de los archivos batimétricos por fecha.
2. Definición y construcción de la malla regular como dominio de interpolación.
3. Aplicación de un método de interpolación espacial sobre los datos dispersos.
4. Asignación de valores de profundidad a cada punto de la malla.
6. Generación de una representación matricial de la batimetría para cada instante temporal.

## Salidas

- Campos batimétricos interpolados sobre la malla regular.
- Base estructurada para la generación de teselas y muestras del modelo.

## Implementación

A continuación se presenta el fragmento principal del código utilizado para la interpolación de los datos sobre la malla:

```python
from scipy.interpolate import RBFInterpolator

# Construcción del interpolador a partir de datos dispersos
interp = RBFInterpolator(
    df[['X', 'Y']].values,
    df['Z'].values,
    smoothing=0.5,
    neighbors=50
)

# Interpolación sobre la malla (solo puntos válidos)
z_validos = interp(pts_validos)

# Reconstrucción de la malla 2D completa
z_grid = np.full(gx.shape, np.nan, dtype=float)
z_grid.ravel()[mask] = z_validos

