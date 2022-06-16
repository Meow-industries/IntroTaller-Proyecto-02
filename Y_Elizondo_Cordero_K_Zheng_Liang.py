"""
##########################################################
#                                                        #      
#            Instituto Tecnológico de Costa Rica         #
#          Área Académica de Ing. en Computadores        #
#                                                        #
#             Proyecto Programado Número dos             #
#                                                        #
#                       Estudiantes:                     #
#          Yherland Elizondo Cordero - 2022289492        #
#               Kun Kin Zheng Liang - 2022205015         #
#                                                        #
#       Taller de programación - Ing. en Computadores    #
#                                                        #
##########################################################
"""

from main import GraphicUserInterface 

class Main:
	def __init__(self):
		self.__ui = GraphicUserInterface()
		self.__ui.mainloop()
			
if __name__ == '__main__':
	main = Main()