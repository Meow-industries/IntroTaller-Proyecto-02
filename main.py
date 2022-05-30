import tkinter as tk
from tkinter import PhotoImage, GROOVE
import pygame, copy
from lib.gameBoards import playerAtPc, pcAtPlayer

class GraphicUserInterface(tk.Tk):
    """Creating the main window"""
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)# constructor 
         
        #Widtet calling 
        self.__configureWindow() 
        self.__topMenu()
        self.__setupMusic()
        self.__setup_papcMatrix()
        self.__gameSetup = GameSetup()

        # creating a container
        self.__container = tk.Frame(self) 
        self.__container.pack(side = "top", fill = "both", expand = True)
        self.__container.grid_rowconfigure(0, weight = 1)
        self.__container.grid_columnconfigure(0, weight = 1)


        # creating an empty list to add the frames
        self.frames = {} 
  
        # movement through pages 
        for screenFrame in (MainMenu, GameScreen):
  
            frame = screenFrame(self.__container, self)
  
            """save the frame"""
            self.frames[screenFrame] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
    
        self.showFrame(MainMenu)

    """showing the frame"""
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def __setup_papcMatrix(self): #Load the attack matrix 
        self.__gameSetup.getpapcMatrix().loadMatrix(copy.deepcopy(playerAtPc)) #the "copy" is used to create a new object.
    
    def __configureWindow(self):
        """ Main window configuration """

        self.title("BATTLESHIP")
        self.geometry("773x409+300+60")
        self.iconbitmap('media/icon.ico') #TODO: Revisar compatibilidad con mac
        self.resizable(False, False)

    def __setupMusic(self):
        """Music setup"""

        #Starting pygame
        pygame.mixer.init()

        #Import Soundtrack
        pygame.mixer.music.load("sound/menuTrack.mp3")
        pygame.mixer.music.play(loops=-1) #Play the song while the user is in MainMenu
    

    def __setupPause(self):
        """Funtion to pause the music"""

        pygame.mixer.music.pause() #Pause the song 

    def __setupPlay(self):
        """Function to resume the music"""

        pygame.mixer.music.play() #Play the song 
        
    def __topMenu(self):  
        """top menu configuration"""

        menubar = tk.Menu(self, foreground='black', activeforeground='black')  
        file = tk.Menu(menubar, tearoff=1, foreground='black') 
        file.add_command(label="About Developers")
        file.add_command(label="Read Tutorial!")
        file.add_separator()  
        file.add_command(label="Salir", command=self.quit)  
        menubar.add_cascade(label="Help", menu=file)  
        
        about = tk.Menu(menubar, tearoff=0)  
        about.add_command(label="Save")  
        about.add_command(label="Load") 
        menubar.add_cascade(label="Game", menu=about) 
        
        hallOfFame = tk.Menu(menubar, tearoff=0)  
        hallOfFame.add_command(label="Go!") 
        menubar.add_cascade(label="Hall Of Fame", menu=hallOfFame) 

        music = tk.Menu(menubar, tearoff=0)
        music.add_command(label="Play", command = self.__setupPlay)  
        music.add_command(label="Mute", command= self.__setupPause)  
        menubar.add_cascade(label="Music", menu=music)
        
        self.config(menu=menubar) 

class MainMenu(tk.Frame):
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor
        self.__initComponents(controller)

    def __initComponents(self, controller):
        """Widget calling"""
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupEntry()
        self.__setupButton(controller)

    def __setupButton(self,controller):
        """Play Button configuration"""
        playButton = tk.Button(self, text="Play", command= lambda : controller.showFrame(GameScreen))
        playButton.place(x=10, y=10)


    def __setupCanvas(self):
        """Canvas configuration"""
        self.__menuCanva = tk.Canvas(self, width=800, height=600, borderwidth=0)
        self.__menuCanva.place(x=0, y=0)

    def __setupBackground(self):
        """Background configuration"""

        global bgImg #Global variable to show the image

        bgImg = PhotoImage(file= "media/menu.png")
        bgLabel = tk.Label(self.__menuCanva, image = bgImg)
        bgLabel.place(x=0, y=0)

    def __setupEntry(self):
        """Entry setup"""
        self.__userNameInput = tk.StringVar()
        self.__userNameInput.set("Ingrese su nombre")
        nameEntry = tk.Entry(self.__menuCanva, textvariable=self.__userNameInput, font=("Helvetica", 10, "bold" ))
        nameEntry.config(width=30)
        nameEntry.place(x=300, y=300)
        
class GameScreen(tk.Frame):
    """Game Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__initComponents()
    
    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()

    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=384, height=384)
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=384, height=384) 
        self.__gameCanvas.place(x=385, y=0)

    def __setupImagesFiles(self):
        self.__planeUp = PhotoImage(file="media/planeUp.jpg")
        self.__planeDown = PhotoImage(file="media/planeDown.jpg")
        self.__planeLeft = PhotoImage(file="media/planeLeft.jpg")
        self.__planeRight = PhotoImage(file="media/planeRight.jpg")
        self.__waterBlock = PhotoImage(file="media/waterBlock.jpg")
        self.__woodBlock = PhotoImage(file="media/woodBlock.png")

    def __getImage(self, id): # funcion para obtener la imagen deseada dependiendo de su ID
        if id == 7 :
            return self.__woodBlock
        elif id == 0:
            return self.__waterBlock
        elif id == 4.1:
            return self.__planeUp
        elif id == 4.2:
            return self.__planeDown
        elif id == 4.3:
            return self.__planeRight
        elif id == 4.4:
            return self.__planeLeft
            
class playerAttackPcMatrix(object):
    __instance = None

    def __new__(cls): #Haciendo uso de un singletone para tener una unica instancia de la matriz
        if cls.__instance is None:
            cls.__instance = super(playerAttackPcMatrix, cls).__new__(cls)
            cls.__matrix = []
        return cls.__instance

    def loadMatrix(cls, papcMatrix): # cargando la matriz 
        cls.__matrix = papcMatrix

    def getMatrix(cls): # funcion que devulve la matriz
        return cls.__matrix

    def updatePosition(cls, pOld, pNew,oldID, newID): # funcion que actualiza la matriz a nivel logico
        cls.__matrix[pOld[0]][pOld[1]] = oldID 
        cls.__matrix[pNew[0]][pNew[1]] = newID 
        return (pOld, oldID), (pNew, newID)

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__papcMatrix = playerAttackPc()

    def getpapcMatrix(self): #funcion que sirve de medio para acceder a la clase Matrix()
        return self.__papcMatrix

