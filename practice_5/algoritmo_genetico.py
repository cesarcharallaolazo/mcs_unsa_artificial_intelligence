from random import uniform, choices, randint, randrange, random
import pdb

# Parametros iniciales
probabilidad_cruzamiento = 0.7
probabilidad_mutacion = 0.05
# Cruzamiento BLX-Alpha
alpha = 0.5
rango_beta = (-alpha, 1 + alpha)
# Mutacion Uniforme
cantidad_iteraciones = 5000


# Poblacion inicial
def crear_un_individuo_inicial():
    # el individuo consta de 2 ejes X , Y / consideramos las restricciones
    individuo = [uniform(-10, 10) for _ in range(2)]
    return individuo


def crear_poblacion_inicial(tamano_poblacion):
    poblacion = [(f"ind_{i + 1}", crear_un_individuo_inicial()) for i in range(tamano_poblacion)]
    # print(poblacion)
    # print("siguiente !!")
    return poblacion


def calcular_aptitud_un_individuo(individuo):
    return (individuo[0] + 2 * individuo[1] - 7) ** 2 + (2 * individuo[0] + individuo[1] - 5) ** 2


def calcular_aptitud_poblacion(poblacion):
    return [(individuo[0], calcular_aptitud_un_individuo(individuo[1])) for individuo in poblacion]


def escoger_ganador(individuo1, individuo2):
    fitness1 = calcular_aptitud_un_individuo(individuo1)
    fitness2 = calcular_aptitud_un_individuo(individuo2)
    if fitness1 <= fitness2:  # estamos en un problema de minimizacion
        return 0, fitness1
    else:
        return 1, fitness2


def creacion_mating_pool(poblacion, numero_selecciones):
    seleccion_torneo = []
    for _ in range(numero_selecciones):
        par = choices(poblacion, k=2)
        indice_relativo_individuo, fitness = escoger_ganador(par[0][1], par[1][1])
        indice_individuo = par[indice_relativo_individuo][0]
        par.append(("resultado --> ", indice_individuo, par[indice_relativo_individuo][1], "fitness", fitness))
        seleccion_torneo.append(par)
    # print(seleccion_torneo)
    return seleccion_torneo


def applicar_blx(padre1, padre2, beta1, beta2):
    c1 = padre1[0] + beta1 * (padre2[0] - padre1[0])
    c2 = padre1[1] + beta2 * (padre2[1] - padre1[1])
    return [c1, c2]


def seleccion_padres_cruzamiento_mutacion(mating_pool, numero_hijos_a_generar):
    # ganadores_torneo = []
    # for par in mating_pool:
    #     ganadores_torneo.append(par[2][1])  # obtenemos el indice del individuo ganador
    # pdb.set_trace()
    lista_hijos_generados = []
    for ix in range(numero_hijos_a_generar):
        par_padres = choices(mating_pool, k=2)
        par_padres = [par_padres[0][2], par_padres[1][2]]
        # cruzamiento
        hay_cruzamiento = True if random() < probabilidad_cruzamiento else False
        # mutacion
        hay_mutacion = True if random() < probabilidad_mutacion else False
        padre1 = par_padres[0][2]  # recuperar coordenadas
        padre2 = par_padres[1][2]  # recuperar coordenadas
        fitness1 = par_padres[0][4]
        fitness2 = par_padres[1][4]
        if hay_cruzamiento:
            beta1 = uniform(rango_beta[0], rango_beta[1])
            beta2 = uniform(rango_beta[0], rango_beta[1])
            hijo_generado = applicar_blx(padre1, padre2, beta1, beta2)
        if hay_mutacion:
            posicion = 0 if random() < 0.5 else 1
            if not hay_cruzamiento:
                if fitness1 < fitness2:
                    hijo_generado = padre1
                else:
                    hijo_generado = padre2
            hijo_generado[posicion] = uniform(-10, 10)
        if not hay_cruzamiento and not hay_mutacion:
            if fitness1 < fitness2:
                hijo_generado = padre1
            else:
                hijo_generado = padre2
        lista_hijos_generados.append((f"ind_{ix + 1}", hijo_generado))
    return lista_hijos_generados


def generar_iteraciones(iteraciones):
    print()
    print("Iteracion 1")
    mating_pool_inicial = creacion_mating_pool(crear_poblacion_inicial(20), 20)
    nueva_generacion = seleccion_padres_cruzamiento_mutacion(mating_pool_inicial,
                                                             numero_hijos_a_generar=20)
    for i in range(iteraciones - 1):
        print()
        print(f"Iteracion {i+1+1}")
        mating_pool_iteracion = creacion_mating_pool(nueva_generacion, 20)
        nueva_generacion = seleccion_padres_cruzamiento_mutacion(mating_pool_iteracion,
                                                                 numero_hijos_a_generar=20)
        # print(nueva_generacion)
    return nueva_generacion


solucion_iteraciones = generar_iteraciones(cantidad_iteraciones)
for individuo_final in solucion_iteraciones:
    print(individuo_final[0], individuo_final[1], "fitness", calcular_aptitud_un_individuo(individuo_final[1]))
# print(solucion_iteraciones)
