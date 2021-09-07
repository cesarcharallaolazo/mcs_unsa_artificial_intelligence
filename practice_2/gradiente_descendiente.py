import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# abrir txt de resultados
f = open("./practice_2/data/resultados_2.txt", "a")
f.write("------------- RESOLUCION 2 -------------\n")


def dibujar_cualquier_linea(pendiente, intercepto):
    axes = plt.gca()
    x_valores = np.array(axes.get_xlim())
    y_valores = intercepto + pendiente * x_valores
    plt.plot(x_valores, y_valores, "--", label=f'pendiente {pendiente}, intercepto {intercepto}')
    plt.legend()


# leer csv de observaciones
data = pd.read_csv("./practice_2/data/puntos_pc2.csv")

# ** calculando valores / metodo gradiente descendiente

f.write("CHARALLA OLAZO, CESAR\n")
f.write("Gradiente Descendiente\n")
f.write("\n")

f.write("Datos Utilizados\n")
f.write(data[["X", "Y"]].to_string(index=False))
f.write("\n\n")

# pendiente e intercepto iniciales aleatorios
w1 = 29
w0 = 72
iteraciones = 1000
tasa_aprendizaje = 0.001
for i in range(iteraciones):
    f.write("Iteracion --> " + str(i + 1) + "\n")
    f.write("Pendiente anterior = " + str(w1) + "\n")
    f.write("Intercepto anterior = " + str(w0) + "\n")
    f.write("Tasa de aprendizaje = " + str(tasa_aprendizaje) + "\n")
    y_esperado = data["Y"]
    y_iteracion = w1 * data["X"] + w0
    derivada_intercepto = np.sum(-2 * (y_esperado - y_iteracion))
    derivada_pendiente = np.sum(-2 * (y_esperado - y_iteracion) * data["X"])
    tamano_paso_pendiente = tasa_aprendizaje * derivada_pendiente
    tamano_paso_intercepto = tasa_aprendizaje * derivada_intercepto
    pendiente_nueva = w1 - tamano_paso_pendiente
    intercepto_nuevo = w0 - tamano_paso_intercepto
    f.write("Derivada intercepto = " + str(derivada_intercepto) + "\n")
    f.write("Derivada pendiente = " + str(derivada_pendiente) + "\n")
    f.write("Pendiente nueva = " + str(pendiente_nueva) + "\n")
    f.write("Intercepto nuevo = " + str(intercepto_nuevo) + "\n")
    f.write("\n")
    w1 = pendiente_nueva
    w0 = intercepto_nuevo

# dibujando linea de regresion final de gradiente descendiente
plt.scatter(data["X"], data["Y"])
dibujar_cualquier_linea(pendiente=round(w1, 4), intercepto=round(w0, 4))
plt.show()

# cerrando archivo txt
f.close()
