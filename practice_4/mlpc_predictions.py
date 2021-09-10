import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# abrir txt de resultados
f = open("./practice_4/data/resultados.txt", "a")

# abrir txt tabla resumen
f2 = open("./practice_4/data/resumen_resultados.txt", "a")
f2.write("Fold,MLPC"+"\n")

columna_caracteristicas = ["sexo", "longitud", "diametro", "altura",
                           "peso_total", "peso_carne", "peso_visceras", "peso_secado"]
columna_target = ["anillos"]

# leer dataset
data_abalone = pd.read_csv(f"./practice_4/data/abalone.dat",
                           names=columna_caracteristicas + columna_target)

# preprocesamiento de variable categorica a dummies
data_abalone = pd.get_dummies(data_abalone)
columna_caracteristicas_final = list(data_abalone.columns)
columna_caracteristicas_final.remove(columna_target[0])
data_abalone_caracteristicas = data_abalone[columna_caracteristicas_final]

# preprocesamiento target
data_abalone["joven"] = data_abalone[columna_target].apply(lambda row: 1 if row["anillos"] <= 14 else 0, axis=1)
data_abalone_target = data_abalone[["joven"]]
cantidad_de_clases = len(data_abalone.joven.unique())

f.write("CHARALLA OLAZO, CESAR\n")
f.write("Perceptron Multicapa\n")
f.write("\n")

## Validacion Cruzada
numero_folds = 10
kf = KFold(n_splits=numero_folds)

i = 0
tasa_aprendizaje = 0.003
maximo_iteraciones = 100000
funcion_activacion = "relu"
cantidad_capas_ocultas = 3
perceptrone_por_capa = 5
tasa_clasificacion_test_folds = []
for train_index, test_index in kf.split(data_abalone_caracteristicas):
    ## arquitectura del Perceptron Multicapa
    mlpc_clf_iteracion = MLPClassifier(hidden_layer_sizes=tuple([perceptrone_por_capa
                                                                 for i in range(cantidad_capas_ocultas)
                                                                 ]),
                                       activation=funcion_activacion,
                                       learning_rate_init=tasa_aprendizaje,
                                       max_iter=maximo_iteraciones)

    f.write(f"Fold " + str(i) + "\n")
    X_train, X_test = data_abalone_caracteristicas.iloc[train_index], data_abalone_caracteristicas.iloc[test_index]
    y_train, y_test = data_abalone_target.iloc[train_index], data_abalone_target.iloc[test_index]
    f.write("Nª Datos Entrenamiento = " + str(len(X_train)) + "\n")
    f.write("Nª Datos Test = " + str(len(X_test)) + "\n")
    f.write("Cantidad de Caracteristicas = " + str(len(X_test.columns)) + "\n")
    f.write("Cantidad de Clases = " + str(cantidad_de_clases) + "\n")
    f.write("Parametro - Funcion de Activacion = " + str(funcion_activacion) + "\n")
    f.write("Parametro - Tasa de Aprendizaje = " + str(tasa_aprendizaje) + "\n")
    f.write("Parametro - Maximo Iteraciones = " + str(maximo_iteraciones) + "\n")
    f.write("Cantidad de capas ocultas = " + str(cantidad_capas_ocultas) + "\n")
    f.write("Cantidad de perceptrones por capa = " + str(perceptrone_por_capa) + "\n")
    # entrenamiento en la iteracion
    mlpc_clf_iteracion.fit(X_train, y_train)

    predicciones_train = mlpc_clf_iteracion.predict(X_train)
    f.write("Tasa Clasificacion Train : " + str(accuracy_score(predicciones_train, y_train)) + "\n")

    predicciones_test = mlpc_clf_iteracion.predict(X_test)
    tasa_clasificacion_test_iteracion = accuracy_score(predicciones_test, y_test)
    f.write("Tasa Clasificacion Test : " + str(tasa_clasificacion_test_iteracion) + "\n\n")
    tasa_clasificacion_test_folds.append(tasa_clasificacion_test_iteracion)
    i = i +1
    f2.write(str(i) + ","+str(round(tasa_clasificacion_test_iteracion, 6))+ "\n")

np_tasa_clasificacion_test_folds = np.array(tasa_clasificacion_test_folds)
f2.write("media," + str(round(np_tasa_clasificacion_test_folds.mean(), 6)) + "\n")
f2.write("desviacion_estandar," + str(round(np_tasa_clasificacion_test_folds.std(), 6)))
f.write("\n"+ "Tasa Clasificacion Promedio en Test ---> " + str(np_tasa_clasificacion_test_folds.mean()) + "\n")

# cerrando archivo txt
f.close()
f2.close()
