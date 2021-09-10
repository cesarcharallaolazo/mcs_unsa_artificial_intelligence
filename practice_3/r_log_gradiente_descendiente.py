import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def sigmoide(x):
    return 1 / (1 + np.exp(-x))


# abrir txt de resultados
f = open("./practice_3/data/resultados.txt", "a")


def dibujar_cualquier_sigmoide(pendiente, intercepto, minimo_punto=-10, maximo_punto=10):
    x = np.linspace(minimo_punto, maximo_punto, 100)
    z = 1 / (1 + np.exp(-(pendiente * x + intercepto)))
    plt.xlabel("horas_estudio")
    plt.ylabel("Sigmoide (horas_estudio)")
    plt.plot(x, z, "--", label=f'pendiente {pendiente}, intercepto {intercepto}')
    plt.legend()


# leer csv de observaciones
data = pd.read_csv("./practice_3/data/puntos_pc3.csv")

# seleccionar datos de entrenamiento (22) y de test (6) aleatoriamente
X_train, X_test, y_train, y_test = train_test_split(data["horas_estudio"], data["aprobado"],
                                                    test_size=6 / 28, random_state=12)

# pendiente/intercepto/parametros iniciales aleatorios
w1 = 15.2567
w0 = -8.4984
iteraciones = 100000
tasa_aprendizaje = 0.001
umbral = 0.5

# *** calculando valores Regresion Logistica / metodo gradiente descendiente

f.write("CHARALLA OLAZO, CESAR\n\n")
f.write("Gradiente Descendiente - Regresion Logistica\n")
f.write("Pendiente anterior = " + str(w1) + "\n")
f.write("Intercepto anterior = " + str(w0) + "\n")
f.write("Tasa de aprendizaje = " + str(tasa_aprendizaje) + "\n")
f.write("Cantidad de iteraciones = " + str(iteraciones) + "\n")
f.write("Umbral = " + str(umbral) + "\n")
f.write("-> Datos de Entrenamiento\n")
f.write(pd.concat([X_train, y_train], axis=1).to_string(index=False))
f.write("\n\n")
f.write("-> Datos de Test\n")
f.write(pd.concat([X_test, y_test], axis=1).to_string(index=False))
f.write("\n\n\n")

for i in range(iteraciones):
    y_esperado = y_train
    y_iteracion = sigmoide(w1 * X_train + w0)  # y_estimado
    error = -1 * np.sum(
        np.where(y_esperado == 0,
                 (1 - y_esperado) * np.log(1 - y_iteracion),
                 y_esperado * np.log(y_iteracion))
    )
    derivada_intercepto = np.sum((y_iteracion - y_esperado))
    derivada_pendiente = np.sum((y_iteracion - y_esperado) * X_train)
    tamano_paso_pendiente = tasa_aprendizaje * derivada_pendiente
    tamano_paso_intercepto = tasa_aprendizaje * derivada_intercepto
    pendiente_nueva = w1 - tamano_paso_pendiente
    intercepto_nuevo = w0 - tamano_paso_intercepto

    f.write("Iteracion --> " + str(i + 1) + "\n")
    f.write("Pendiente anterior = " + str(w1) + "\n")
    f.write("Intercepto anterior = " + str(w0) + "\n")
    f.write("Error = " + str(error) + "\n")
    f.write("Tasa de aprendizaje = " + str(tasa_aprendizaje) + "\n")

    f.write("Derivada pendiente = " + str(derivada_pendiente) + "\n")
    f.write("Derivada intercepto = " + str(derivada_intercepto) + "\n")
    f.write("Pendiente nueva = " + str(pendiente_nueva) + "\n")
    f.write("Intercepto nuevo = " + str(intercepto_nuevo) + "\n")
    f.write("\n\n")
    w1 = pendiente_nueva
    w0 = intercepto_nuevo

## *** evaluacion de resultados
X_test = X_test.to_numpy()
y_test = y_test.to_numpy()
y_prob_estimado_test = sigmoide(w1 * X_test + w0)
y_estimado_test = np.where(y_prob_estimado_test >= umbral, 1, 0)
accuracy_test_str = np.where(y_estimado_test == y_test, "Correcto", "Incorrecto")
accuracy_test = np.sum(np.where(y_estimado_test == y_test, 1, 0)) / np.size(y_test) * 100

f.write("Test\n")
for i in range(len(X_test)):
    f.write(f"Dato Nº{i + 1} ({X_test[i]}) = {y_prob_estimado_test[i]}, "
            f"aprovado estimado = {y_estimado_test[i]}, {accuracy_test_str[i]}" + "\n")

f.write("Porcentaje de Acierto : " + str(round(accuracy_test, 2)) + "%" + "\n")

# dibujando sigmoide final de la gradiente descendiente
plt.scatter(data["horas_estudio"], data["aprobado"], c='r', marker="x")
dibujar_cualquier_sigmoide(pendiente=round(w1, 4), intercepto=round(w0, 4),
                           minimo_punto=data["horas_estudio"].min(), maximo_punto=data["horas_estudio"].max())
plt.show()

# cerrando archivo txt
f.close()
