from clases_funciones_abc import *

# Beale Function
ejecutar_fun1 = BealeFunctionABC(tamano_enjambre=100,
                                 limite_inferior=-4.5,
                                 limite_superior=4.5,
                                 numero_iteraciones=5000)
ejecutar_fun1.ejecutar_iteraciones()

# # Three-Hump Camel Function
# ejecutar_fun2 = ThreeHumpCamelFunctionABC(tamano_enjambre=100,
#                                           limite_inferior=-5,
#                                           limite_superior=5,
#                                           numero_iteraciones=5000)
# ejecutar_fun2.ejecutar_iteraciones()
#
# # # Matyas Function
# ejecutar_fun3 = MatyasFunctionABC(tamano_enjambre=100,
#                                   limite_inferior=-10,
#                                   limite_superior=10,
#                                   numero_iteraciones=5000)
# ejecutar_fun3.ejecutar_iteraciones()
#
# # Goldstein-Price Function
# ejecutar_fun4 = GoldsteinPriceFunctionABC(tamano_enjambre=100,
#                                           limite_inferior=-2,
#                                           limite_superior=2,
#                                           numero_iteraciones=5000)
# ejecutar_fun4.ejecutar_iteraciones()
