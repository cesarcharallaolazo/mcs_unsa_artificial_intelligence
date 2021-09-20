from random import uniform, choices, random

# abrir txt de resultados
f = open("./practice_5/data/resultados.txt", "a")

# Parametros iniciales
cantidad_individuos = 20
genes_por_individuo = 2
individuos_por_torneo = 2
probabilidad_cruzamiento = 0.7
probabilidad_mutacion = 0.05
# Cruzamiento BLX-Alpha
alpha = 0.5
rango_beta = (-alpha, 1 + alpha)
# Mutacion Uniforme
cantidad_iteraciones = 5000

f.write("* CESAR AUGUSTO CHARALLA OLAZO" + "\n")
f.write("* Parámetros" + "\n")
f.write("=============" + "\n")
f.write("* Cantidad de Individuos = " + str(cantidad_individuos) + "\n")
f.write("* Cantidad de Genes por Individuo = " + str(genes_por_individuo) + "\n")
f.write("* Selección por torneo = " + str(individuos_por_torneo) + "\n")
f.write("* Probabilidad de Cruzamiento" + str(probabilidad_cruzamiento) + "\n")
f.write("* Cruzamiento BLX-Alpha, Alpha = " + str(alpha) + "\n")
f.write("* Probabilidad de Mutación = " + str(probabilidad_mutacion) + "\n")
f.write("* Mutación Uniforme" + "\n")
f.write("* Cantidad de Iteraciones = " + str(cantidad_iteraciones) + "\n")


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
    return seleccion_torneo


def applicar_blx(padre1, padre2, beta1, beta2):
    c1 = padre1[0] + beta1 * (padre2[0] - padre1[0])
    c2 = padre1[1] + beta2 * (padre2[1] - padre1[1])
    return [c1, c2]


def seleccion_padres_cruzamiento_mutacion(mating_pool, numero_hijos_a_generar):
    lista_hijos_generados = []
    f.write(f"\nSelección de Padres" + "\n")
    for ix in range(numero_hijos_a_generar):
        par_padres = choices(mating_pool, k=2)
        par_padres = [par_padres[0][2], par_padres[1][2]]
        f.write(f"{par_padres[0][1]} - {par_padres[1][1]} => {par_padres[0][2]} - {par_padres[1][2]}" + "\n")
        # cruzamiento
        hay_cruzamiento = True if random() < probabilidad_cruzamiento else False
        # mutacion
        hay_mutacion = True if random() < probabilidad_mutacion else False
        padre1 = par_padres[0][2]  # recuperar coordenadas
        padre2 = par_padres[1][2]  # recuperar coordenadas
        fitness1 = par_padres[0][4]
        fitness2 = par_padres[1][4]
        if hay_cruzamiento:
            f.write(f"Cruzamiento" + "\n")
            beta1 = uniform(rango_beta[0], rango_beta[1])
            f.write(f"Beta 1 = " + str(beta1) + "\n")
            beta2 = uniform(rango_beta[0], rango_beta[1])
            f.write(f"Beta 2 = " + str(beta2) + "\n")
            hijo_generado = applicar_blx(padre1, padre2, beta1, beta2)
            f.write(str(hijo_generado) + "\n")
        else:
            f.write(f"Sin Cruzamiento" + "\n")
        if hay_mutacion:
            f.write(f"Mutación" + "\n")
            posicion = 0 if random() < 0.5 else 1
            if not hay_cruzamiento:
                if fitness1 < fitness2:
                    hijo_generado = padre1
                else:
                    hijo_generado = padre2
            hijo_generado[posicion] = uniform(-10, 10)
            f.write(str(hijo_generado) + "\n")
        else:
            f.write(f"Sin Mutación" + "\n")
        if not hay_cruzamiento and not hay_mutacion:
            if fitness1 < fitness2:
                hijo_generado = padre1
            else:
                hijo_generado = padre2
            f.write(str(hijo_generado) + "\n")
        lista_hijos_generados.append((f"ind_{ix + 1}", hijo_generado))
        f.write("\n")
    return lista_hijos_generados


def generar_iteraciones(iteraciones):
    f.write("\nPoblación Inicial" + "\n")
    poblacion_inicial = crear_poblacion_inicial(cantidad_individuos)
    for individuo in poblacion_inicial:
        f.write(f"{individuo[0]} --> " + str(individuo[1]) + "\n")
    f.write("\nCalcular la Aptitud para cada Individudo" + "\n")
    for individuo in poblacion_inicial:
        f.write(f"{individuo[0]} --> " + str(individuo[1]) + " fitness "
                + str(calcular_aptitud_un_individuo(individuo[1])) + "\n")

    mating_pool_inicial = creacion_mating_pool(poblacion_inicial, cantidad_individuos)
    f.write("\n*** Iteracion 1 ***" + "\n")
    f.write("Creación de Mating Pool" + "\n")
    for torneo_ in mating_pool_inicial:
        f.write(f"{torneo_[0][0]} - {torneo_[1][0]} => {torneo_[2][1]} => {torneo_[2][2]}" + "\n")

    nueva_generacion = seleccion_padres_cruzamiento_mutacion(mating_pool_inicial,
                                                             numero_hijos_a_generar=cantidad_individuos)
    for i in range(iteraciones - 1):
        f.write("\nNueva Población" + "\n")
        for individuo in nueva_generacion:
            f.write(f"{individuo[0]} --> " + str(individuo[1]) + "\n")
        f.write("\nCalcular la Aptitud para cada Individudo" + "\n")
        for individuo in nueva_generacion:
            f.write(f"{individuo[0]} --> " + str(individuo[1]) + " fitness "
                    + str(calcular_aptitud_un_individuo(individuo[1])) + "\n")

        mating_pool_iteracion = creacion_mating_pool(nueva_generacion, cantidad_individuos)
        f.write(f"\n*** Iteracion {i + 1 + 1} ***" + "\n")
        f.write("Creación de Mating Pool" + "\n")
        for torneo in mating_pool_inicial:
            f.write(f"{torneo[0][0]} - {torneo[1][0]} => {torneo[2][1]} => {torneo[2][2]}" + "\n")

        nueva_generacion = seleccion_padres_cruzamiento_mutacion(mating_pool_iteracion,
                                                                 numero_hijos_a_generar=cantidad_individuos)
    return nueva_generacion


solucion_iteraciones_final = generar_iteraciones(cantidad_iteraciones)
for individuo_final in solucion_iteraciones_final:
    print(individuo_final[0], individuo_final[1], "fitness", calcular_aptitud_un_individuo(individuo_final[1]))

f.write("\n\nPoblación Final" + "\n")
for individuo in solucion_iteraciones_final:
    f.write(f"{individuo[0]} --> " + str(individuo[1]) + "\n")
f.write("\nCalcular la Aptitud para cada Individudo" + "\n")
for individuo in solucion_iteraciones_final:
    f.write(f"{individuo[0]} --> " + str(individuo[1]) + " fitness "
            + str(calcular_aptitud_un_individuo(individuo[1])) + "\n")
