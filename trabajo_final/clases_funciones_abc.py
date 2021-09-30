from clases_artificial_bee_colony import ClassArtificialBeeColony


class BealeFunctionABC(ClassArtificialBeeColony):

    def calcular_funcion_objetivo(self, x, y):
        # beale function
        return (1.5 - x + x * y) ** 2 + (2.25 - x + x * (y ** 2)) ** 2 + (2.625 - x + x * (y ** 3)) ** 2


class ThreeHumpCamelFunctionABC(ClassArtificialBeeColony):

    def calcular_funcion_objetivo(self, x, y):
        # three-hump camel function
        return 2 * (x ** 2) - 1.05 * (x ** 4) + (x ** 6) / 6 + x * y + y ** 2


class MatyasFunctionABC(ClassArtificialBeeColony):

    def calcular_funcion_objetivo(self, x, y):
        # matyas function
        return 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y


class GoldsteinPriceFunctionABC(ClassArtificialBeeColony):

    def calcular_funcion_objetivo(self, x, y):
        # goldstein-price function
        return (1 + ((x + y + 1) ** 2) * (19 - 14 * x + 3 * (x ** 2) - 14 * y + 6 * x * y + 3 * (y ** 2))) * (
                30 + ((2 * x - 3 * y) ** 2) * (18 - 32 * x + 12 * (x ** 2) + 48 * y - 36 * x * y + 27 * (y ** 2)))


class ExampleFunctionABC(ClassArtificialBeeColony):

    def calcular_funcion_objetivo(self, x, y):
        # ejemplo de clase pasada AG
        return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2
