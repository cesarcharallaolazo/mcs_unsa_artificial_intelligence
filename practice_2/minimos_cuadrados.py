import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# abrir txt de resultados
f = open("./practice_2/data/resultados_1.txt", "a")
f.write("------------- RESOLUCION 1 -------------\n")


def dibujar_cualquier_linea(pendiente, intercepto):
    axes = plt.gca()
    x_valores = np.array(axes.get_xlim())
    y_valores = intercepto + pendiente * x_valores
    plt.plot(x_valores, y_valores, "--", label=f'pendiente {pendiente}, intercepto {intercepto}')
    plt.legend()


# leer csv de observaciones
data = pd.read_csv("./practice_2/data/puntos_pc2.csv")

# ** calculando valores / metodo minimo cuadrados

data["X^2"] = data["X"] * data["X"]
data["X*Y"] = data["X"] * data["Y"]

f.write("CHARALLA OLAZO, CESAR\n")
f.write("Mínimos Cuadrados\n")
f.write("\n")

f.write("Datos Utilizados\n")
f.write(data[["X", "Y"]].to_string(index=False))
f.write("\n\n")

f.write("Suma de valores de X : " + str(round(np.sum(data["X"]), 6)) + "\n")
f.write("Suma de valores de Y : " + str(round(np.sum(data["Y"]), 6)) + "\n")
f.write("Suma de valores de X*Y : " + str(round(np.sum(data["X*Y"]), 6)) + "\n")
f.write("Suma de valores de X^2 : " + str(round(np.sum(data["X^2"]), 6)) + "\n")
f.write("N (observaciones) : " + str(data.shape[0]) + "\n")
f.write("\n")

W1 = (data.shape[0] * np.sum(data["X*Y"])
      - np.sum(data["X"]) * np.sum(data["Y"])) / (data.shape[0] * np.sum(data["X^2"])
                                                  - (np.sum(data["X"])) ** 2)
f.write("Pendiente : " + str(round(W1, 6)) + "\n")

W0 = (np.sum(data["Y"]) - W1 * np.sum(data["X"])) / data.shape[0]
f.write("Intercepto : " + str(round(W0, 6)) + "\n")

# dibujando linea de regresion final de minimos cuadrados
plt.scatter(data["X"], data["Y"])
dibujar_cualquier_linea(pendiente=round(W1, 6), intercepto=round(W0, 6))
# dibujar_cualquier_linea(pendiente=29, intercepto=72)
plt.show()

# cerrando archivo txt
f.close()
