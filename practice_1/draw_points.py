import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets


def dibujar_cualquier_linea(pendiente, intercepto):
    axes = plt.gca()
    x_valores = np.array(axes.get_xlim())
    y_valores = intercepto + pendiente * x_valores
    plt.plot(x_valores, y_valores, "--", label=f'pendiente {pendiente}, intercepto {intercepto}')
    plt.legend()


X, Y = datasets.make_regression(n_samples=8, n_features=1, noise=20, random_state=325)
X_lista = [round(elemento[0], 2) for elemento in X]
Y_lista = [round(elemento, 2) for elemento in Y]

# *** guardar puntos generados
df_puntos = pd.DataFrame({"X": X_lista, "Y": Y_lista})
df_puntos.to_csv("./practice_1/data/puntos_pc1.csv", index=False)


# *** dibujar puntos generados
## dibujo 1
for j in range(len(X_lista)):
    print(f"punto_{j + 1}", (X_lista[j], Y_lista[j]))
plt.scatter(X_lista, Y_lista)
plt.show()

## dibujo 2
plt.scatter(X_lista, Y_lista)
dibujar_cualquier_linea(pendiente=24, intercepto=40)
plt.show()


