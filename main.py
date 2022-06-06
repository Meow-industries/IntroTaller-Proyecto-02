from time import sleep
import tkinter as tk
from tkinter import PhotoImage
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
        for screenFrame in (MainMenu, GameScreen, TutorialScreen):
  
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
        self.geometry("773x409+300+150")
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
        file.add_command(label= "About Developers")
        file.add_command(label= "Read Tutorial!", command= lambda: self.showFrame(TutorialScreen))
        file.add_command(label= "Main Menu", command= lambda: self.showFrame(MainMenu))
        file.add_separator()  
        file.add_command(label="Salir", command= self.quit)  
        menubar.add_cascade(label="Help", menu= file)  
        
        about = tk.Menu(menubar, tearoff= 0)  
        about.add_command(label= "Save")  
        about.add_command(label= "Load") 
        menubar.add_cascade(label= "Game", menu= about) 
        
        hallOfFame = tk.Menu(menubar, tearoff= 0)  
        hallOfFame.add_command(label= "Go!") 
        menubar.add_cascade(label= "Hall Of Fame", menu= hallOfFame) 

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
        self.__setupLabel()
        
    def __setupButton(self,controller):
        """Play Button configuration"""
        playButton = tk.Button(self, text="Play", width=30, height=2, command= lambda : controller.showFrame(GameScreen))
        playButton.place(x=300, y=240)


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

    def __setupLabel(self):
        entryLabel = tk.Label(self.__menuCanva, text="Username: ", font=("Helvetica", 10, 'bold'))
        entryLabel.place(x=250, y=200)       

    def __setupEntry(self):
        """Entry setup"""
        self.__userNameInput = tk.StringVar()
        self.__userNameInput.set("")
        nameEntry = tk.Entry(self.__menuCanva, textvariable=self.__userNameInput, font=("Helvetica", 10, "bold" ))
        nameEntry.config(width=30)
        nameEntry.place(x=300, y=200)
        
class GameScreen(tk.Frame):
    """Game Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImages()
        self.__setupKeyboardInput()
        
    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=384, height=384)
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=384, height=384) 
        self.__gameCanvas.place(x=385, y=0)

    def __setupKeyboardInput(self): #Keyboard configuration
        if self.__gameSetup.getPlane().getTurn():
            self.bind_all('<d>', lambda event: self.__move(self.__gameSetup.getPlane().moveRight))
            self.bind_all('<w>', lambda event: self.__move(self.__gameSetup.getPlane().moveUp))
            self.bind_all('<s>', lambda event: self.__move(self.__gameSetup.getPlane().moveDown))
            self.bind_all('<a>', lambda event: self.__move(self.__gameSetup.getPlane().moveLeft))
            self.bind_all('<j>', lambda event: self.__attack(self.__gameSetup.getPlane().attack)) #Ejecutar el "disparo", ademas tiene que cambiar el estado de turno
        else:
            #aqui llamariamos al turno de la compu, cambiaria el estado
            print("turno rival")
            sleep(1.5)
            
    def __attack(self, pMoveFunction):
        position = pMoveFunction()
        self.__updateVisualPapcMatrixAttack(position)

    def __move(self, pMoveFunction):#funcion que realiza el movimiento general del personaje
        movement = pMoveFunction()
        self.__updateVisualPapcMatrix(movement[0], movement[1])

    def __updateVisualPapcMatrix(self, oldMovement, newMovement): # funcion que actualiza dos elementos de la matriz dados movimientos
        tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg="Black").place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg="Black").place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __updateVisualPapcMatrixAttack(self, position):
        tk.Label(self.__gameCanvas, image=self.__getImage(position), bg="Black").place(x=position*32,y=position*32)
     
    def __setupImagesFiles(self):
        self.__planeUp = PhotoImage(file="media/planeUp.png")
        self.__planeDown = PhotoImage(file="media/planeDown.png")
        self.__planeLeft = PhotoImage(file="media/planeLeft.png")
        self.__planeRight = PhotoImage(file="media/planeRight.png")
        self.__waterBlock = PhotoImage(file="media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file="media/stoneBlock.png")
        self.__missBlock = PhotoImage(file= "media/missBlock.png")

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
        elif id == 5:
            return self.__missBlock
        else:
            return self.__waterBlock

    def __setupImages(self): # Carga todas las imagenes visualmente
        
        matrix = self.__gameSetup.getPapcMatrix().getMatrix()

        for i in range(0,len(matrix)):
            for j in range(0,len(matrix[0])):
                tk.Label(self.__gameCanvas, image=self.__getImage(matrix[i][j]), bg="Black").place(x=j*32,y=i*32)

class TutorialScreen(tk.Frame):
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()

    def __setupCanvas(self):
        self.__tutorialCanvas = tk.Canvas(self, width=384, height=384)
        self.__tutorialCanvas.place(x=0, y=0)

        
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

    def checkRightMiss(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 5

    def checkLeftMiss(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 5

    def checkUpMiss(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 5

    def checkDownMiss(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 5

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

    def updatePosition(cls, pOld, pNew,oldID, newID): #Update the logic matriz when the player moves
        cls.__matrix[pOld[0]][pOld[1]] = oldID 
        cls.__matrix[pNew[0]][pNew[1]] = newID 
        return (pOld, oldID), (pNew, newID)
    
    def updateAttack(cls, pNew, newID): #Update the logic matriz when the player attack
        cls.__matrix[pNew[0]][pNew[1]] = newID
        return newID

class AtkPlane:
    def __init__(self): #class constructor
        self.__x = 6
        self.__y = 0
        self.moves = 0
        self.turn = True
        self.__check = ToCheck()
        self.__papcMatrix = playerAttackPcMatrix()

    def getCoords(self):
        return self.__x, self.__y
        
    def getTurn(self): 
        return self.turn

    def setupSound(self, fxID):
        if fxID == 1:
            pygame.mixer.music.load("sound/explotionSound.mp3")
            pygame.mixer.music.play(loops=0) 
        else:
            pygame.mixer.music.load("sound/missSound.mp3")
            pygame.mixer.music.play(loops=0) 

    def moveLeft(self):
        if self.__check.checkLeftDebris(self.__x, self.__y): 
            self.__oldID = 3
        
        elif self.__check.checkLeftMiss(self.__x, self.__y):
            self.__oldID = 5

        else:
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 4.4

        if not self.__check.checkLimitLeft(self.__x, self.__y):
            self.__y -= 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)

    def moveRight(self):

        if self.__check.checkLimitUp(self.__x, self.__y) and self.__check.checkLimitDown(self.__x, self.__y):
            self.__oldID = 7

        elif self.__check.checkRightDebris(self.__x, self.__y):
            self.__oldID = 3

        elif self.__check.checkRightMiss(self.__x, self.__y):
            self.__oldID = 5
        else:
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 4.3

        if not self.__check.checkLimitRight(self.__x, self.__y):
            self.__y += 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)
    
    def moveUp(self):

        if self.__check.checkUpDebris(self.__x, self.__y):
            self.__oldID = 3

        elif self.__check.checkUpMiss(self.__x, self.__y):
            self.__oldID = 5

        else:
            self.__oldID = 0

        oldX = self.__x
        self.__ID = 4.1

        if not self.__check.checkLimitUp(self.__x, self.__y):
            self.__x -= 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)

    def moveDown(self):

        if self.__check.checkDownDebris(self.__x, self.__y):
            self.__oldID = 3

        elif self.__check.checkDownMiss(self.__x, self.__y):
            self.__oldID = 5

        else:
            self.__oldID = 0

        oldX = self.__x
        self.__ID = 4.2

        if not self.__check.checkLimitDown(self.__x, self.__y):
            self.__x += 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)
    
    def attack(self):
        self.moves += 1 #Movement cont
        if self.__ID  == 4.1: 
            if self.__check.checkUpBoat(self.__x, self.__y): #Player looks up
                self.turn = True
                newX = self.__x - 1
                self.__ID = 3
                self.setupSound(1)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
            else:
                self.turn = False
                newX = self.__x - 1
                self.__ID = 5
                self.setupSound(0)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)

        elif self.__ID == 4.2:
            if self.__check.checkDownBoat(self.__x, self.__y): #Player looks up
                self.turn = True
                newX = self.__x + 1
                self.__ID = 3
                self.setupSound(1)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
            else:
                self.turn = False
                newX = self.__x + 1
                self.__ID = 5
                self.setupSound(0)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)

        elif self.__ID == 4.3:
            if self.__check.checkRightBoat(self.__x, self.__y): #Player looks up
                self.turn = True
                newY = self.__y + 1
                self.__ID = 3
                self.setupSound(1)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
            else:
                self.turn = False
                newY = self.__y + 1
                self.__ID = 5
                self.setupSound(0)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
        else:
            if self.__check.checkLeftBoat(self.__x, self.__y): #Player looks up
                self.turn = True
                newY = self.__y - 1
                self.__ID = 3
                self.setupSound(1)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
            else:
                self.turn = False
                newY = self.__y - 1
                self.__ID = 5
                self.setupSound(0)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__papcMatrix = playerAttackPcMatrix()
        self.__atkPlane = AtkPlane()
        self.__check = ToCheck()

    def getPapcMatrix(self): #funcion que sirve de medio para acceder a la clase playerAttackPcMatrix()
        return self.__papcMatrix

    def getPlane(self):
        return self.__atkPlane
    
    def getCheck(self):
        return self.__check