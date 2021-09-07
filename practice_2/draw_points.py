import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets

X, Y = datasets.make_regression(n_samples=100, n_features=1, noise=35, random_state=325)
X_lista = [round(elemento[0], 6) for elemento in X]
Y_lista = [round(elemento, 6) for elemento in Y]

# *** guardar puntos generados
df_puntos = pd.DataFrame({"X": X_lista, "Y": Y_lista})
df_puntos.to_csv("./practice_2/data/puntos_pc2.csv", index=False)


# *** dibujar puntos generados
## dibujo 1
for j in range(len(X_lista)):
    print(f"punto_{j + 1}", (X_lista[j], Y_lista[j]))
plt.scatter(X_lista, Y_lista)
plt.show()
