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
        self.__setupMatrix()

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

    def __setupMatrix(self): #Load the attack matrix 
        self.__gameSetup.getPapcMatrix().loadMatrix(copy.deepcopy(playerAtPc)) #the "copy" is used to create a new object.
        self.__gameSetup.getpcapMatrix().loadMatrix(copy.deepcopy(pcAtPlayer)) #the "copy" is used to create a new object.
    
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
        playButton = tk.Button(self, text="Play", font=("Helvetica", 15, 'bold'), width=10, command= lambda : controller.showFrame(GameScreen))
        playButton.place(x=325, y=280)

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
        entryLabel.place(x=350, y=205)       

    def __setupEntry(self):
        """Entry setup"""
        self.__userNameInput = tk.StringVar()
        self.__userNameInput.set("")
        nameEntry = tk.Entry(self.__menuCanva, textvariable=self.__userNameInput, font=("Helvetica", 10, "bold" ))
        nameEntry.config(width=25)
        nameEntry.place(x=300, y=230)
        
class GameScreen(tk.Frame):
    """Game Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespapc()
        self.__setupImagespcap()
        self.__setupKeyboardInput()
        
    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=384, height=384, bg="blue")
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=384, height=384) 
        self.__gameCanvas.place(x=385, y=0)

    def __setupKeyboardInput(self): #Keyboard configuration
        
        self.bind_all('<d>', lambda event: self.__move(self.__gameSetup.getPlane().moveRight))
        self.bind_all('<w>', lambda event: self.__move(self.__gameSetup.getPlane().moveUp))
        self.bind_all('<s>', lambda event: self.__move(self.__gameSetup.getPlane().moveDown))
        self.bind_all('<a>', lambda event: self.__move(self.__gameSetup.getPlane().moveLeft))
        self.bind_all('<j>', lambda event: self.__attack(self.__gameSetup.getPlane().attack)) #Ejecutar el "disparo", ademas tiene que cambiar el estado de turno

    def __attack(self, pMoveFunction):
        position = pMoveFunction()
        self.__updateVisualPapcMatrixAttack(position)
       

    def __move(self, pMoveFunction): #funcion que realiza el movimiento general del personaje
        movement = pMoveFunction()
        self.__updateVisualPapcMatrix(movement[0], movement[1])
       
            
    def __updateVisualPapcMatrix(self, oldMovement, newMovement): # funcion que actualiza dos elementos de la matriz dados movimientos
        tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg="Black").place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg="Black").place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __updateVisualPapcMatrixAttack(self, position):
        print("[0][1]:", position[0][0])
        print("[0]:", position[0])
        print("[1]:", position[1])
        print("[0][1]:",position[0][1])
        tk.Label(self.__gameCanvas, image=self.__getImage(position[1]), bg="Black").place(x=position[0][1]*32,y=position[0][0]*32)
     
    def __setupImagesFiles(self):
        self.__planeUp = PhotoImage(file="media/planeUp.png")
        self.__planeDown = PhotoImage(file="media/planeDown.png")
        self.__planeLeft = PhotoImage(file="media/planeLeft.png")
        self.__planeRight = PhotoImage(file="media/planeRight.png")
        self.__waterBlock = PhotoImage(file="media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file="media/stoneBlock.png")
        self.__missBlock = PhotoImage(file= "media/missBlock.png")
        self.__debrisBlock = PhotoImage(file= "media/debrisBlock.png")

    def __getImage(self, id): # funcion para obtener la imagen deseada dependiendo de su ID
        if id == 7 :
            return self.__stoneBlock
        elif id == 0:
            return self.__waterBlock
        elif id == 3:
            return self.__debrisBlock
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

    def __setupImagespapc(self): # Carga todas las imagenes visualmente
        
        matrixpapc = self.__gameSetup.getPapcMatrix().getMatrix()

        for i in range(0,len(matrixpapc)):
            for j in range(0,len(matrixpapc[0])):
                tk.Label(self.__gameCanvas, image=self.__getImage(matrixpapc[i][j]), bg="Black").place(x=j*32,y=i*32)
        

    def __setupImagespcap(self): # Carga todas las imagenes visualmente
        
        matrixpcap = self.__gameSetup.getpcapMatrix().getMatrix()

        for i in range(0,len(matrixpcap)):
            for j in range(0,len(matrixpcap[0])):
                tk.Label(self.__boatsCanvas, image=self.__getImage(matrixpcap[i][j]), bg="Black").place(x=j*32,y=i*32)

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
        self.__papcMatrix = PlayerAttackPcMatrix()
        
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

    def checkRightMissed(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 5

    def checkLeftMissed(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 5

    def checkUpMissed(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 5

    def checkDownMissed(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 5

class PlayerAttackPcMatrix(object):
    __instance = None

    def __new__(cls): #Haciendo uso de un singletone para tener una unica instancia de la matriz
        if cls.__instance is None:
            cls.__instance = super(PlayerAttackPcMatrix, cls).__new__(cls)
            cls.__matrix = []
        return cls.__instance

    def loadMatrix(cls, papcMatrix): # cargando la matriz 
        cls.__matrix = papcMatrix

    def getMatrix(cls): # funcion que devulve la matriz
        return cls.__matrix

    def updatePosition(cls, pOld, pNew, oldID, newID): #Update the logic matriz when the player moves
        cls.__matrix[pOld[0]][pOld[1]] = oldID 
        cls.__matrix[pNew[0]][pNew[1]] = newID 
        return (pOld, oldID), (pNew, newID)
    
    def updateAttack(cls, pNew, newID): #Update the logic matriz when the player attack
        cls.__matrix[pNew[0]][pNew[1]] = newID
        return pNew, newID

class Turn: # Another singletone to modify and return the "Turn" value
    __instance = None
    def __new__(cls): #Haciendo uso de un singletone para tener una unica instancia del turno
        if cls.__instance is None:
            cls.__instance = super(Turn, cls).__new__(cls)
            cls.__turn = True
        return cls.__instance

    def setTurn(cls, state): # turn modification 
        cls.__turn = state

    def getTurn(cls): # return the turn value
        return cls.__turn

class AtkPlane:
    def __init__(self): #class constructor
        self.__x = 6
        self.__y = 0
        self.moves = 0
        self.__countX = 0
        self.__countDebris = 0
        self.__countBoat = 0
        self.__check = ToCheck()
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__turn = Turn()

    def getCoords(self):
        return self.__x, self.__y

    def setupFxSound(self, fxID):
        if fxID == 1:
            __explotionFx = pygame.mixer.Sound("sound/explotionSound.mp3")
            __explotionFx.play() 
        else:
            __missFx = pygame.mixer.Sound("sound/missSound.mp3")
            __missFx.play() 

    def moveLeft(self):
        if self.__check.checkLeftDebris(self.__x, self.__y): 
            if self.__countDebris != 0: 
                self.__oldID = 3
            else: 
                self.__oldID = 0
                self.__countDebris += 1
        
        elif self.__check.checkLeftMissed(self.__x, self.__y):
            if self.__countX != 0: 
                self.__oldID = 5
            else:
                self.__oldID = 0
                self.__countX += 1

        else:
            if self.__countX != 0: 
                self.__oldID = 5
                self.__countX = 0
            
            elif self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0

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
            if self.__countDebris != 0: 
                self.__oldID = 3
            else: 
                self.__oldID = 0
                self.__countDebris += 1

        elif self.__check.checkRightMissed(self.__x, self.__y):
            if self.__countX != 0: 
                self.__oldID = 5
            else:
                self.__oldID = 0
                self.__countX += 1
        
        else:
            if self.__countX != 0: 
                self.__oldID = 5
                self.__countX = 0
            
            elif self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0

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
            if self.__countDebris != 0: 
                self.__oldID = 3
            else: 
                self.__oldID = 0
                self.__countDebris += 1

        elif self.__check.checkUpMissed(self.__x, self.__y):
            if self.__countX != 0: 
                self.__oldID = 5
            else:
                self.__oldID = 0
                self.__countX += 1

        else:
            if self.__countX != 0: 
                self.__oldID = 5
                self.__countX = 0
            
            elif self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0

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
            if self.__countDebris != 0: 
                self.__oldID = 3
            else: 
                self.__oldID = 0
                self.__countDebris += 1

        elif self.__check.checkDownMissed(self.__x, self.__y):
            if self.__countX != 0: 
                self.__oldID = 5
            else: 
                self.__oldID = 0
                self.__countX += 1

        else:
            if self.__countX != 0: 
                self.__oldID = 5
                self.__countX = 0
            
            elif self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0

            else: 
                self.__oldID = 0

        oldX = self.__x
        self.__ID = 4.2

        if not self.__check.checkLimitDown(self.__x, self.__y):
            self.__x += 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)
    
    def doNothing(self):
        cont = 0
        cont += 1

    def attack(self):
        self.moves += 1 #Movement cont
        
        if self.__ID == 4.1: #Player looks up
            if self.__check.checkUpMissed(self.__x, self.__y):
                self.doNothing()

            elif self.__check.checkUpBoat(self.__x, self.__y):  
                self.__turn.setTurn(True)
                newX = self.__x - 1
                self.__ID = 3
                self.setupFxSound(1)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
            
            else:
                self.__turn.setTurn(False)
                newX = self.__x - 1
                self.__ID = 5
                self.setupFxSound(0)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)

        if self.__ID == 4.2: #Player looks down
            if self.__check.checkDownMissed(self.__x, self.__y):
                self.doNothing()

            elif self.__check.checkDownBoat(self.__x, self.__y): 
                self.__turn.setTurn(True)
                newX = self.__x + 1
                self.__ID = 3
                self.setupFxSound(1)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
            else:
                self.__turn.setTurn(False)
                newX = self.__x + 1
                self.__ID = 5
                self.setupFxSound(0)
                return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)

        if self.__ID == 4.3:
            if self.__check.checkRightMissed(self.__x, self.__y):
                self.doNothing()

            elif self.__check.checkRightBoat(self.__x, self.__y): #Player looks up
                self.__turn.setTurn(True)
                newY = self.__y + 1
                self.__ID = 3
                self.setupFxSound(1)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
            else:
                self.__turn.setTurn(False)
                newY = self.__y + 1
                self.__ID = 5
                self.setupFxSound(0)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
        
        if self.__ID == 4.4:
            if self.__check.checkLeftMissed(self.__x, self.__y):
                self.doNothing()

            elif self.__check.checkLeftBoat(self.__x, self.__y): #Player looks up
                self.__turn.setTurn(True)
                newY = self.__y - 1
                self.__ID = 3
                self.setupFxSound(1)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
            else:
                self.__turn.setTurn(False)
                newY = self.__y - 1
                self.__ID = 5
                self.setupFxSound(0)
                return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)

class PcAttackPlayerMatrix(object):
    __instance = None

    def __new__(cls): #Haciendo uso de un singletone para tener una unica instancia de la matriz
        if cls.__instance is None:
            cls.__instance = super(PcAttackPlayerMatrix, cls).__new__(cls)
            cls.__matrix = []
        return cls.__instance

    def loadMatrix(cls, pcapMatrix): # cargando la matriz 
        cls.__matrix = pcapMatrix

    def getMatrix(cls): # funcion que devuelve la matriz
        return cls.__matrix

    def updatePosition(cls, pOld, pNew, oldID, newID): #Update the logic matriz when the player moves
        cls.__matrix[pOld[0]][pOld[1]] = oldID 
        cls.__matrix[pNew[0]][pNew[1]] = newID 
        return (pOld, oldID), (pNew, newID)
    
    def updateAttack(cls, pNew, newID): #Update the logic matriz when the player attack
        cls.__matrix[pNew[0]][pNew[1]] = newID
        return pNew, newID

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__atkPlane = AtkPlane()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__pcapMatrix = PcAttackPlayerMatrix() 

    def getPapcMatrix(self): #funcion que sirve de medio para acceder a la clase playerAttackPcMatrix()
        return self.__papcMatrix

    def getPlane(self):
        return self.__atkPlane
    
    def getCheck(self):
        return self.__check

    def getState(self):
        return self.__turn
    
    def getpcapMatrix(self):
        return self.__pcapMatrix