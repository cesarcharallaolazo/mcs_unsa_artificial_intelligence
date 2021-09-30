from random import uniform, choices, sample
import numpy as np

# Parametros iniciales
tamano_enjambre = 100
tamano_fuente_comida = int(tamano_enjambre / 2)
numero_abejas_obreras = int(tamano_enjambre / 2)
numero_abejas_observadoras = int(tamano_enjambre / 2)
limite_inferior = -10
limite_superior = 10
numero_iteraciones = 5000
dimensiones = 2
limite_a_descartar = tamano_fuente_comida * dimensiones


def calcular_funcion_objetivo(x, y):
    # return(x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2 # ejemplo de clase pasada AG
    # return 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y  # matyas function
    return (1.5 - x + x * y) ** 2 + (2.25 - x + x * (y ** 2)) ** 2 + (2.625 - x + x * (y ** 3)) ** 2  # beale function
    # return 2 * (x ** 2) - 1.05 * (x ** 4) + (x ** 6) / 6 + x * y + y ** 2  # three-hump camel function
    # return (1 + ((x + y + 1) ** 2) * (19 - 14 * x + 3 * (x ** 2) - 14 * y + 6 * x * y + 3 * (y ** 2))) * (30 + ((2 * x - 3 * y) ** 2) * (18 - 32 * x + 12 * (x ** 2) + 48 * y - 36 * x * y + 27 * (y ** 2)))  # goldstein-price function


def calcular_fitness(x, y):
    f = calcular_funcion_objetivo(x, y)
    return 1 / (1 + f) if f >= 0 else 1 + abs(f)


def fuente_seleccion_greedy_fit(x1, y1, x2, y2, trial):
    fit_anterior = calcular_fitness(x1, y1)
    fit_nuevo = calcular_fitness(x2, y2)
    trial_nuevo = trial + 1
    return [x2, y2, 0] if fit_nuevo > fit_anterior else [x1, y1, trial_nuevo]


def verificar_limites(numero, limite_inf=limite_inferior, limite_sup=limite_superior):
    if numero < limite_inf:
        return limite_inf
    elif numero > limite_sup:
        return limite_sup
    else:
        return numero


def calcular_nueva_fuente_comida(fuente_actual, fuente_partner, indice_dimension):
    phi = uniform(-1, 1)
    if indice_dimension == 0:
        dimension_0 = fuente_actual[0] + phi * (fuente_actual[0] - fuente_partner[0])
        return verificar_limites(dimension_0), fuente_actual[1]
    if indice_dimension == 1:
        dimension_1 = fuente_actual[1] + phi * (fuente_actual[1] - fuente_partner[1])
        return fuente_actual[0], verificar_limites(dimension_1)


def fase_optimizacion_abejas_obreras(cantidad_abejas_obreras, poblacion_fuente_comida, trials_poblacion_fuente_comida):
    n_p = cantidad_abejas_obreras
    opciones_indice_fuente_comida = [_ for _ in range(len(poblacion_fuente_comida))]
    poblacion_fuente_comida_aux = poblacion_fuente_comida.copy()
    for i in range(n_p):
        fuente_comida = poblacion_fuente_comida_aux[i]
        indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
        while i == indice_partner_fuente_comida:
            indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
        seleccion_aleatoria_dimension_fuente_comida = choices([0, 1], k=1)[0]
        x_nuevo, y_nuevo = calcular_nueva_fuente_comida(fuente_comida,
                                                        poblacion_fuente_comida_aux[indice_partner_fuente_comida],
                                                        seleccion_aleatoria_dimension_fuente_comida)
        x_final, y_final, trials_poblacion_fuente_comida[i] \
            = fuente_seleccion_greedy_fit(fuente_comida[0], fuente_comida[1], x_nuevo, y_nuevo,
                                          trials_poblacion_fuente_comida[i])
        poblacion_fuente_comida[i] = [x_final, y_final]

    # calcular vector de probabilidades para la fase de abejas observadoras
    vector_fitness = [calcular_fitness(poblacion_fuente_comida[i][0], poblacion_fuente_comida[i][1]) for i in
                      range(len(poblacion_fuente_comida))]
    max_fitness = max(vector_fitness)
    vector_probabilidad = [0.9 * (fit / max_fitness) + 0.1 for fit in vector_fitness]
    return poblacion_fuente_comida, trials_poblacion_fuente_comida, vector_probabilidad


def fase_optimizacion_abejas_observadoras(cantidad_abejas_observadoras, poblacion_fuente_comida,
                                          trials_poblacion_fuente_comida, vector_probabilidad):
    n_p = cantidad_abejas_observadoras
    opciones_indice_fuente_comida = [_ for _ in range(len(poblacion_fuente_comida))]
    poblacion_fuente_comida_aux = poblacion_fuente_comida.copy()
    m, indice_fuente_comida = 0, 0
    # for i in range(n_p):
    while m < n_p:
        aleatorio = uniform(0, 1)
        if aleatorio < vector_probabilidad[indice_fuente_comida]:
            fuente_comida = poblacion_fuente_comida_aux[indice_fuente_comida]
            indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
            while indice_fuente_comida == indice_partner_fuente_comida:
                indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
            seleccion_aleatoria_dimension_fuente_comida = choices([0, 1], k=1)[0]
            x_nuevo, y_nuevo = calcular_nueva_fuente_comida(fuente_comida,
                                                            poblacion_fuente_comida_aux[indice_partner_fuente_comida],
                                                            seleccion_aleatoria_dimension_fuente_comida)
            x_final, y_final, trials_poblacion_fuente_comida[indice_fuente_comida] \
                = fuente_seleccion_greedy_fit(fuente_comida[0], fuente_comida[1], x_nuevo, y_nuevo,
                                              trials_poblacion_fuente_comida[indice_fuente_comida])
            poblacion_fuente_comida[indice_fuente_comida] = [x_final, y_final]
            m = m + 1
        indice_fuente_comida = indice_fuente_comida + 1
        if indice_fuente_comida == len(poblacion_fuente_comida):
            indice_fuente_comida = 0
    return poblacion_fuente_comida, trials_poblacion_fuente_comida


def fase_optimizacion_abejas_scout(poblacion_fuente_comida, trials_poblacion_fuente_comida,
                                   limite, fuente_descartadas, iteracion_general):
    tamano_poblacion = len(poblacion_fuente_comida)
    aleatoriedad_escogimiento = sample([_ for _ in range(tamano_poblacion)], k=tamano_poblacion)
    candidatos_a_descartar = []
    for ix in aleatoriedad_escogimiento:
        if trials_poblacion_fuente_comida[ix] > limite:
            candidatos_a_descartar.append(ix)

    if len(candidatos_a_descartar) == 1:
        ix_a_eliminar = candidatos_a_descartar[0]
        # guardar y reemplazar fuente de comida a eliminar
        fuente_descartadas[f"iteracion_{str(iteracion_general)}"]["fuente_comida"] \
            = poblacion_fuente_comida[ix_a_eliminar]
        fuente_descartadas[f"iteracion_{str(iteracion_general)}"]["trials"] \
            = trials_poblacion_fuente_comida[ix_a_eliminar]
        poblacion_fuente_comida[ix_a_eliminar] = generar_nueva_fuente_comida()
        trials_poblacion_fuente_comida[ix_a_eliminar] = 0
        return poblacion_fuente_comida, trials_poblacion_fuente_comida, fuente_descartadas
    elif len(candidatos_a_descartar) >= 2:
        max = trials_poblacion_fuente_comida[candidatos_a_descartar[0]]
        ix_a_eliminar = candidatos_a_descartar[0]
        for i in range(len(candidatos_a_descartar)):
            temp_max = trials_poblacion_fuente_comida[candidatos_a_descartar[i]]
            if max < temp_max:
                max = temp_max
                ix_a_eliminar = candidatos_a_descartar[i]
        # guardar y reemplazar fuente de comida a eliminar
        fuente_descartadas[f"iteracion_{str(iteracion_general)}"]["fuente_comida"] \
            = poblacion_fuente_comida[ix_a_eliminar]
        fuente_descartadas[f"iteracion_{str(iteracion_general)}"]["trials"] \
            = trials_poblacion_fuente_comida[ix_a_eliminar]
        poblacion_fuente_comida[ix_a_eliminar] = generar_nueva_fuente_comida()
        trials_poblacion_fuente_comida[ix_a_eliminar] = 0
        return poblacion_fuente_comida, trials_poblacion_fuente_comida, fuente_descartadas
    else:  # no hay fuente de comida a descartar
        return poblacion_fuente_comida, trials_poblacion_fuente_comida, fuente_descartadas


def generar_nueva_fuente_comida(limit_inf=limite_inferior, limit_sup=limite_superior):
    return [uniform(limit_inf, limit_sup), uniform(limit_inf, limit_sup)]


# Poblacion inicial
def crear_poblacion_inicial_fuente_comida(n=tamano_fuente_comida):
    return [generar_nueva_fuente_comida() for _ in range(n)]


# Iteraciones Generales
poblacion_fuente_comida = crear_poblacion_inicial_fuente_comida(tamano_fuente_comida)
trials_poblacion = [0 for _ in range(tamano_fuente_comida)]
fuente_descartadas = {}
for iter in range(numero_iteraciones):
    # print("ITERACION ---> ", iter)
    fuente_descartadas[f"iteracion_{str(iter)}"] = {}
    poblacion_fuente_comida, trials_poblacion, vector_probabilidad \
        = fase_optimizacion_abejas_obreras(numero_abejas_obreras, poblacion_fuente_comida, trials_poblacion)
    poblacion_fuente_comida, trials_poblacion = \
        fase_optimizacion_abejas_observadoras(numero_abejas_observadoras, poblacion_fuente_comida,
                                              trials_poblacion, vector_probabilidad)
    poblacion_fuente_comida, trials_poblacion, fuente_descartadas = \
        fase_optimizacion_abejas_scout(poblacion_fuente_comida, trials_poblacion,
                                       limite_a_descartar, fuente_descartadas, iter)
    # print(fuente_descartadas)

optima_fuente_comida = {}
optima_fuente_comida["fitness"] = -np.inf
optima_fuente_comida["fuente_comida"] = []
optima_fuente_comida["trials"] = -1
for key in fuente_descartadas.keys():
    if fuente_descartadas[key] != {}:
        fuente_comida = fuente_descartadas[key]['fuente_comida']
        fitness = calcular_fitness(fuente_comida[0], fuente_comida[1])
        print(key, fuente_descartadas[key],
              "fitness", fitness)
        if fitness > optima_fuente_comida["fitness"]:
            optima_fuente_comida["fitness"] = fitness
            optima_fuente_comida["fuente_comida"] = fuente_comida
            optima_fuente_comida["trials"] = fuente_descartadas[key]['trials']

print("SOLUCION OPTIMA !!!")
print(optima_fuente_comida)
