from random import uniform, choices, sample
import numpy as np


class ClassArtificialBeeColony():
    dimensiones = 2

    def __init__(self, tamano_enjambre, limite_inferior, limite_superior, numero_iteraciones, poblacion_inicial):
        # Parametros iniciales
        self.tamano_enjambre = tamano_enjambre
        self.tamano_fuente_comida = int(tamano_enjambre / 2)
        self.numero_abejas_obreras = int(tamano_enjambre / 2)
        self.numero_abejas_observadoras = int(tamano_enjambre / 2)
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.numero_iteraciones = numero_iteraciones
        self.limite_a_descartar = self.tamano_fuente_comida * self.dimensiones
        self.poblacion_inicial = poblacion_inicial
        self.poblacion_inicial_print = poblacion_inicial.copy()

    def calcular_fitness(self, x, y):
        f = self.calcular_funcion_objetivo(x, y)
        return 1 / (1 + f) if f >= 0 else 1 + abs(f)

    def fuente_seleccion_greedy_fit(self, x1, y1, x2, y2, trial):
        fit_anterior = self.calcular_fitness(x1, y1)
        fit_nuevo = self.calcular_fitness(x2, y2)
        trial_nuevo = trial + 1
        return [x2, y2, 0] if fit_nuevo > fit_anterior else [x1, y1, trial_nuevo]

    def verificar_limites(self, numero):
        if numero < self.limite_inferior:
            return self.limite_inferior
        elif numero > self.limite_superior:
            return self.limite_superior
        else:
            return numero

    def calcular_nueva_fuente_comida(self, fuente_actual, fuente_partner, indice_dimension):
        phi = uniform(-1, 1)
        if indice_dimension == 0:
            dimension_0 = fuente_actual[0] + phi * (fuente_actual[0] - fuente_partner[0])
            return self.verificar_limites(dimension_0), fuente_actual[1]
        if indice_dimension == 1:
            dimension_1 = fuente_actual[1] + phi * (fuente_actual[1] - fuente_partner[1])
            return fuente_actual[0], self.verificar_limites(dimension_1)

    def fase_optimizacion_abejas_obreras(self, cantidad_abejas_obreras, poblacion_fuente_comida,
                                         trials_poblacion_fuente_comida):
        n_p = cantidad_abejas_obreras
        opciones_indice_fuente_comida = [_ for _ in range(len(poblacion_fuente_comida))]
        poblacion_fuente_comida_aux = poblacion_fuente_comida.copy()
        for i in range(n_p):
            fuente_comida = poblacion_fuente_comida_aux[i]
            indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
            while i == indice_partner_fuente_comida:
                indice_partner_fuente_comida = choices(opciones_indice_fuente_comida, k=1)[0]
            seleccion_aleatoria_dimension_fuente_comida = choices([0, 1], k=1)[0]
            x_nuevo, y_nuevo = self.calcular_nueva_fuente_comida(fuente_comida,
                                                                 poblacion_fuente_comida_aux[
                                                                     indice_partner_fuente_comida],
                                                                 seleccion_aleatoria_dimension_fuente_comida)
            x_final, y_final, trials_poblacion_fuente_comida[i] \
                = self.fuente_seleccion_greedy_fit(fuente_comida[0], fuente_comida[1], x_nuevo, y_nuevo,
                                                   trials_poblacion_fuente_comida[i])
            poblacion_fuente_comida[i] = [x_final, y_final]

        # calcular vector de probabilidades para la fase de abejas observadoras
        vector_fitness = [self.calcular_fitness(poblacion_fuente_comida[i][0], poblacion_fuente_comida[i][1]) for i in
                          range(len(poblacion_fuente_comida))]
        max_fitness = max(vector_fitness)
        vector_probabilidad = [0.9 * (fit / max_fitness) + 0.1 for fit in vector_fitness]
        return poblacion_fuente_comida, trials_poblacion_fuente_comida, vector_probabilidad

    def fase_optimizacion_abejas_observadoras(self, cantidad_abejas_observadoras, poblacion_fuente_comida,
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
                x_nuevo, y_nuevo = self.calcular_nueva_fuente_comida(fuente_comida,
                                                                     poblacion_fuente_comida_aux[
                                                                         indice_partner_fuente_comida],
                                                                     seleccion_aleatoria_dimension_fuente_comida)
                x_final, y_final, trials_poblacion_fuente_comida[indice_fuente_comida] \
                    = self.fuente_seleccion_greedy_fit(fuente_comida[0], fuente_comida[1], x_nuevo, y_nuevo,
                                                       trials_poblacion_fuente_comida[indice_fuente_comida])
                poblacion_fuente_comida[indice_fuente_comida] = [x_final, y_final]
                m = m + 1
            indice_fuente_comida = indice_fuente_comida + 1
            if indice_fuente_comida == len(poblacion_fuente_comida):
                indice_fuente_comida = 0
        return poblacion_fuente_comida, trials_poblacion_fuente_comida

    def fase_optimizacion_abejas_scout(self, poblacion_fuente_comida, trials_poblacion_fuente_comida,
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
            poblacion_fuente_comida[ix_a_eliminar] = self.generar_nueva_fuente_comida()
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
            poblacion_fuente_comida[ix_a_eliminar] = self.generar_nueva_fuente_comida()
            trials_poblacion_fuente_comida[ix_a_eliminar] = 0
            return poblacion_fuente_comida, trials_poblacion_fuente_comida, fuente_descartadas
        else:  # no hay fuente de comida a descartar
            return poblacion_fuente_comida, trials_poblacion_fuente_comida, fuente_descartadas

    def generar_nueva_fuente_comida(self):
        return [uniform(self.limite_inferior, self.limite_superior),
                uniform(self.limite_inferior, self.limite_superior)]

    # Poblacion inicial
    # def crear_poblacion_inicial_fuente_comida(self):
    #     return [self.generar_nueva_fuente_comida() for _ in range(self.tamano_fuente_comida)]
    def crear_poblacion_inicial_fuente_comida(self):
        return self.poblacion_inicial

    def ejecutar_iteraciones(self):
        # Iteraciones Generales
        poblacion_fuente_comida = self.crear_poblacion_inicial_fuente_comida()
        trials_poblacion = [0 for _ in range(self.tamano_fuente_comida)]
        fuente_descartadas = {}
        for iter in range(self.numero_iteraciones):
            # print("ITERACION ---> ", iter)
            fuente_descartadas[f"iteracion_{str(iter)}"] = {}
            poblacion_fuente_comida, trials_poblacion, vector_probabilidad \
                = self.fase_optimizacion_abejas_obreras(self.numero_abejas_obreras, poblacion_fuente_comida,
                                                        trials_poblacion)
            poblacion_fuente_comida, trials_poblacion = \
                self.fase_optimizacion_abejas_observadoras(self.numero_abejas_observadoras, poblacion_fuente_comida,
                                                           trials_poblacion, vector_probabilidad)
            poblacion_fuente_comida, trials_poblacion, fuente_descartadas = \
                self.fase_optimizacion_abejas_scout(poblacion_fuente_comida, trials_poblacion,
                                                    self.limite_a_descartar, fuente_descartadas, iter)

        optima_fuente_comida = {}
        optima_fuente_comida["solucion/fuente_comida"] = []
        optima_fuente_comida["trials"] = -1
        optima_fuente_comida["valor_funcion"] = -np.inf
        optima_fuente_comida["fitness"] = -np.inf
        for key in fuente_descartadas.keys():
            if fuente_descartadas[key] != {}:
                fuente_comida = fuente_descartadas[key]['fuente_comida']
                fitness = self.calcular_fitness(fuente_comida[0], fuente_comida[1])
                print(key, fuente_descartadas[key],
                      "fitness", fitness)
                if fitness > optima_fuente_comida["fitness"]:
                    optima_fuente_comida["solucion/fuente_comida"] = fuente_comida
                    optima_fuente_comida["trials"] = fuente_descartadas[key]['trials']
                    optima_fuente_comida["valor_funcion"] = self.calcular_funcion_objetivo(fuente_comida[0],
                                                                                           fuente_comida[1])
                    optima_fuente_comida["fitness"] = fitness
            else:
                print(key, " --> no hay solucion de fuente de comida para abejas scout")

        print("------------- POBLACION INICIAL!!! -------------")
        print("Poblacion Inicial -->", self.poblacion_inicial_print)
        print("------------- SOLUCION OPTIMA FINAL!!! -------------")
        print(optima_fuente_comida)
