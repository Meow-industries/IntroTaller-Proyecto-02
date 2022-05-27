from main import GraphicUserInterface 

class Main:
	def __init__(self):
		self.__ui = GraphicUserInterface()
		self.__ui.mainloop()
			

if __name__ == '__main__':
	main = Main()