import tkinter as tk
from tkinter import PhotoImage, GROOVE
import pygame, copy
from lib.gameBoards import playerAtPc, pcAtPlayer

class GraphicUserInterface(tk.Tk):
    """Creating the main window"""
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)# constructor 

        self.__gameSetup = GameSetup()
        #Widtet calling 
        self.__configureWindow() 
        self.__topMenu()
        self.__setupMusic()
        self.__setupPapcMatrix()
        

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

    def __setupPapcMatrix(self): #Load the attack matrix 
        self.__gameSetup.getPapcMatrix().loadMatrix(copy.deepcopy(playerAtPc)) #the "copy" is used to create a new object.
    
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
        self.__gameSetup = GameSetup()
        self.__setupImages()

    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()

    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=384, height=384)
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=384, height=384) 
        self.__gameCanvas.place(x=385, y=0)
    
    def __updateVisualPapcMatrix(self, oldMovement, newMovement): # funcion que actualiza dos elementos de la matriz dados movimientos
        tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg="Black").place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg="Black").place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)
    
    def __setupImagesFiles(self):
        self.__planeUp = PhotoImage(file="media/planeUp.png")
        self.__planeDown = PhotoImage(file="media/planeDown.png")
        self.__planeLeft = PhotoImage(file="media/planeLeft.png")
        self.__planeRight = PhotoImage(file="media/planeRight.png")
        self.__waterBlock = PhotoImage(file="media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file="media/stoneBlock.png")
        self.__roadBoat = PhotoImage(file="media/roadBoat.png")

    def __getImage(self, id): # funcion para obtener la imagen deseada dependiendo de su ID
        if id == 7 :
            return self.__stoneBlock
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
        elif id == 9:
            return self.__roadBoat
        else:
            return self.__waterBlock

    def __setupImages(self): # Carga todas las imagenes visualmente
        
        matrix = self.__gameSetup.getPapcMatrix().getMatrix()

        for i in range(0,len(matrix)):
            for j in range(0,len(matrix[0])):
                tk.Label(self.__gameCanvas, image=self.__getImage(matrix[i][j]), bg="Black").place(x=j*32,y=i*32)
class ToCheck:
    def __init__(self):
        self.__papcMatrix = playerAttackPcMatrix()
        
    def checkLimitRight(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 7

    def checkLimitLeft(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 7

    def checkLimitDown(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 7

    def checkLimitUp(self, pX, pY):
        self.__x = pX
        self.__y = pY 
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 7
    
    def checkRightBoat(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 1

    def checkLeftBoat(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 1

    def checkDownBoat(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 1

    def checkUpBoat(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 1 

    def checkUpDebris(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 3

    def checkDownDebris(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 3

    def checkLeftDebris(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 3

    def checkRightDebris(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 3
        
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

class AtkPlane:
    def __init__(self): #class constructor
        self.__x = 6
        self.__y = 0
        self.__moves = 0
        self.__check = ToCheck()
        self.__papcMatrix = playerAttackPcMatrix()
    
    def moveLeft(self):
        if self.__check.checkLimitUp(self.__x, self.__y) and self.__check.checkLimitDown(self.__x, self.__y):
            self.__oldID = 7

        elif self.__check.checkUpDebris(self.__x, self.__y) or self.__check.checkDownDebris(self.__x, self.__y):
            self.__oldID = 3

        elif self.__check.checkLeftDebris(self.__x, self.__y) or self.__check.checkRightDebris(self.__x, self.__y):
            self.__oldID = 3
        else:
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 4.4

        if not self.__check.checkLimitLeft(self.__x, self.__y):
            self.__y -= 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((self.__x, self.__oldID), (self.__x, self.__oldID), self.__oldID, self.__ID)






class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__papcMatrix = playerAttackPcMatrix()
        #self.__atkBoat = 
    def getPapcMatrix(self): #funcion que sirve de medio para acceder a la clase playerAttackPcMatrix()
        return self.__papcMatrix

