import tkinter as tk
from tkinter import PhotoImage
import pygame, copy, random
from lib.gameBoards import playerAtPc, pcAtPlayer

#Constantes
BLACK = 'Black'
WIDTH = 384
HEIGHT = 384
HELVETICA = 'Helvetica'

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
        for screenFrame in (MainMenu, setupBoatScreen, GameScreen, TutorialScreen):
  
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

        menubar = tk.Menu(self, foreground=BLACK, activeforeground=BLACK)  
        file = tk.Menu(menubar, tearoff=1, foreground=BLACK) 
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
        playButton = tk.Button(self, text="Play", font=(HELVETICA, 15, 'bold'), width=10, command= lambda : controller.showFrame(setupBoatScreen))
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
        entryLabel = tk.Label(self.__menuCanva, text="Username: ", font=(HELVETICA, 10, 'bold'))
        entryLabel.place(x=350, y=205)       

    def __setupEntry(self):
        """Entry setup"""
        self.__userNameInput = tk.StringVar()
        self.__userNameInput.set("")
        nameEntry = tk.Entry(self.__menuCanva, textvariable=self.__userNameInput, font=(HELVETICA, 10, "bold" ))
        nameEntry.config(width=25)
        nameEntry.place(x=300, y=230)

class setupBoatScreen(tk.Frame):
    """Setup boat screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespcap()
        self.__setupKeyboardInput()    
        self.__setupLabel()

    def __setupCanvas(self):
        """Canvas configuration"""

        self.__infoCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="blue")
        self.__infoCanvas.place(x=385, y=0)

        self.__setupCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT) 
        self.__setupCanvas.place(x=0, y=0)

        self.__countBoatCanvas = tk.Canvas(self, width=122, height=30, bg=BLACK) 
        self.__countBoatCanvas.place(x=323, y=0)

    def __setupLabel(self): 
        self.__boat = tk.Label(self.__countBoatCanvas, text='Bote 1', font=(HELVETICA, 12), bg=BLACK, fg='white')
        self.__boat.place(x=5, y=5)

    def __setupKeyboardInput(self): #Keyboard configuration
        self.bind_all('<Right>', lambda event: self.__move(self.__gameSetup.getArrow().moveRight))
        self.bind_all('<Up>', lambda event: self.__move(self.__gameSetup.getArrow().moveUp))
        self.bind_all('<Down>', lambda event: self.__move(self.__gameSetup.getArrow().moveDown))
        self.bind_all('<Left>', lambda event: self.__move(self.__gameSetup.getArrow().moveLeft))
        self.bind_all('<k>', lambda event: self.__placeBoat(self.__gameSetup.getPlane().attack)) #place boat

    def __move(self, pMoveFunction): 
        movement = pMoveFunction()
        self.__updateVisualPcapMatrix(movement[0], movement[1])

    def __placeBoat(self, pMoveFunction):#TODO: hay que cambiar la logica de esta parte
        position = pMoveFunction()
        self.__updateVisualPcapMatrixPlaceBoat(position)
    
    def __updateVisualPcapMatrix(self, oldMovement, newMovement): 
        tk.Label(self.__setupCanvas, image=self.__getImage(oldMovement[1]), bg=BLACK).place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__setupCanvas, image=self.__getImage(newMovement[1]), bg=BLACK).place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)
    
    def __updateVisualPcapMatrixPlaceBoat(self, position):
        tk.Label(self.__setupCanvas, image=self.__getImage(position[1]), bg=BLACK).place(x=position[0][1]*32,y=position[0][0]*32)
       
    def __setupImagesFiles(self):
        self.__arrowUp = PhotoImage(file= "media/arrowUp.png")
        self.__arrowDown = PhotoImage(file= "media/arrowDown.png")
        self.__arrowRight = PhotoImage(file= "media/arrowRight.png")
        self.__arrowLeft = PhotoImage(file= "media/arrowLeft.png")
        self.__waterBlock = PhotoImage(file= "media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file= "media/stoneBlock.png")
        
    def __getImage(self, id):
        if id == 9.1:
            return self.__arrowUp
        elif id == 9.2:
            return self.__arrowDown    
        elif id == 9.3: 
            return self.__arrowRight
        elif id == 9.4: 
            return self.__arrowLeft     
        elif id == 7: 
            return self.__stoneBlock
            #hacen falta todos los de los barcos
        else: 
            return self.__waterBlock
            
    def __setupImagespcap(self):
        matrixpcap = self.__gameSetup.getpcapMatrix().getMatrix()
        
        for i in range(0,len(matrixpcap)):
            for j in range(0,len(matrixpcap[0])):
                tk.Label(self.__setupCanvas, image=self.__getImage(matrixpcap[i][j]), bg=BLACK).place(x=j*32,y=i*32)

class GameScreen(tk.Frame):
    """Game Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__turn = Turn()
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespapc()
        self.__setupImagespcap()
        self.__setupKeyboardInput()
        
    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="blue")
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT) 
        self.__gameCanvas.place(x=385, y=0)

        self.__countCanvas = tk.Canvas(self, width=122, height=30, bg=BLACK) 
        self.__countCanvas.place(x=323, y=0)

    def __setupKeyboardInput(self): #Keyboard configuration
        self.bind_all('<d>', lambda event: self.__move(self.__gameSetup.getPlane().moveRight))
        self.bind_all('<w>', lambda event: self.__move(self.__gameSetup.getPlane().moveUp))
        self.bind_all('<s>', lambda event: self.__move(self.__gameSetup.getPlane().moveDown))
        self.bind_all('<a>', lambda event: self.__move(self.__gameSetup.getPlane().moveLeft))
        self.bind_all('<j>', lambda event: self.__attack(self.__gameSetup.getPlane().attack)) #Ejecutar el "disparo", ademas tiene que cambiar el estado de turno

    def __attack(self, pMoveFunction):
        if self.__turn.getTurn():
            position = pMoveFunction()
            self.__updateVisualPapcMatrixAttack(position)
        else:
            position = self.__gameSetup.getComputer().attack()
            self.__updateVisualPcapMatrix(position)

    def __move(self, pMoveFunction): #funcion que realiza el movimiento general del personaje
        if self.__turn.getTurn():
            movement = pMoveFunction()
            self.__updateVisualPapcMatrix(movement[0], movement[1])
            
    def __updateVisualPapcMatrix(self, oldMovement, newMovement): # funcion que actualiza dos elementos de la matriz dados movimientos
        tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg=BLACK).place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg=BLACK).place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __updateVisualPapcMatrixAttack(self, position):
        tk.Label(self.__gameCanvas, image=self.__getImage(position[1]), bg=BLACK).place(x=position[0][1]*32,y=position[0][0]*32)
    
    def __updateVisualPcapMatrix(self, position):
        tk.Label(self.__boatsCanvas, image=self.__getImage(position[1]), bg=BLACK).place(x=position[0][1]*32,y=position[0][0]*32)

    def __setupImagesFiles(self):
        self.__planeUp = PhotoImage(file= "media/planeUp.png")
        self.__planeDown = PhotoImage(file= "media/planeDown.png")
        self.__planeLeft = PhotoImage(file= "media/planeLeft.png")
        self.__planeRight = PhotoImage(file= "media/planeRight.png")
        self.__waterBlock = PhotoImage(file= "media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file= "media/stoneBlock.png")
        self.__missBlock = PhotoImage(file= "media/missBlock.png")
        self.__debrisBlock = PhotoImage(file= "media/debrisBlock.png")
        self.__playerBoat = PhotoImage(file = "media/roadBoatHor.png")
    
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
        elif id == -1:
            return self.__playerBoat
        else:
            return self.__waterBlock

    def __setupImagespapc(self): # Carga todas las imagenes visualmente
        
        matrixpapc = self.__gameSetup.getPapcMatrix().getMatrix()

        for i in range(0,len(matrixpapc)):
            for j in range(0,len(matrixpapc[0])):
                tk.Label(self.__gameCanvas, image=self.__getImage(matrixpapc[i][j]), bg=BLACK).place(x=j*32,y=i*32)
        
    def __setupImagespcap(self): # Carga todas las imagenes visualmente
        
        matrixpcap = self.__gameSetup.getpcapMatrix().getMatrix()

        for i in range(0,len(matrixpcap)):
            for j in range(0,len(matrixpcap[0])):
                tk.Label(self.__boatsCanvas, image=self.__getImage(matrixpcap[i][j]), bg=BLACK).place(x=j*32,y=i*32)

class TutorialScreen(tk.Frame):
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__initComponents()
        
    def __initComponents(self):
        self.__setupCanvas()

    def __setupCanvas(self):
        self.__tutorialCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.__tutorialCanvas.place(x=0, y=0)
  
class ToCheck:
    def __init__(self):
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__pcapMatrix = PcAttackPlayerMatrix()
        
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

    def checkCoordDisp(self, cord, history): # function to check if the random coord is avialable
        self.__estado = False
        for verify in history:
            if verify == cord:
                self.__estado = True
                break
        return self.__estado
    
    def checkHorBoatsLeft(self, pX, pY):#TODO:
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 1.2
    
    def checkVerBoatsLeft(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 1.1

    def checkHorBoatsRight(self, pX, pY):#TODO:
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 1.2
    
    def checkVerBoatsRight(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 1.1

    def checkHorBoatsUp(self, pX, pY):#TODO:
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 1.2
    
    def checkVerBoatsUp(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 1.1
    
    def checkHorBoatsDown(self, pX, pY):#TODO:
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 1.2
    
    def checkVerBoatsDown(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 1.1

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

class Arrow: #TODO:
    def __init__(self):
        self.__x = 6
        self.__y = 0
        #self.__countBoat = 0
        self.__RIGHT = False
        self.__LEFT = False
        self.__UP = False
        self.__DOWN = False
        self.__check = ToCheck()
        self.__pcapMatrix = PcAttackPlayerMatrix()
    
    def setupFxSound(self):
        __constructionFx = pygame.mixer.Sound("sound/contructionSound.mp3")
        __constructionFx.play() 
    
    def moveLeft(self):
        if self.__check.checkVerBoatsLeft(self.__x, self.__y):
                self.__oldID = 1.1
        elif self.__check.checkHorBoatsLeft(self.__x, self.__y):
                self.__oldID = 1.2
        else: 
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 9.4

        if not self.__check.checkLimitLeft(self.__x, self.__y):
            self.__LEFT = True
            self.__DOWN, self.__UP, self.__RIGHT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__y -= 1
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)

    def moveRight(self):
        if self.__check.checkLimitUp(self.__x, self.__y) and self.__check.checkLimitDown(self.__x, self.__y):
            self.__oldID = 7
        elif self.__check.checkVerBoatsRight(self.__x, self.__y):
            self.__oldID = 1.1
        elif self.__check.checkHorBoatsRight(self.__x, self.__y):
            self.__oldID = 1.2
        else: 
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 9.3

        if not self.__check.checkLimitRight(self.__x, self.__y):
            self.__RIGHT = True
            self.__DOWN, self.__UP, self.__LEFT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__y += 1
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)
    
    def moveUp(self):
        if self.__check.checkVerBoatsUp(self.__x, self.__y):
                self.__oldID = 1.1
        elif self.__check.checkHorBoatsUp(self.__x, self.__y):
                self.__oldID = 1.2
        else: 
            self.__oldID = 0

        oldX = self.__x
        self.__ID = 9.1

        if not self.__check.checkLimitUp(self.__x, self.__y):
            self.__UP = True
            self.__DOWN, self.__RIGHT, self.__LEFT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__x -= 1
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)

    def moveDown(self):
        if self.__check.checkVerBoatsDown(self.__x, self.__y):
                self.__oldID = 1.1
        elif self.__check.checkHorBoatsDown(self.__x, self.__y):
                self.__oldID = 1.2
        else: 
            self.__oldID = 0

        oldX = self.__x
        self.__ID = 9.2

        if not self.__check.checkLimitDown(self.__x, self.__y):
            self.__DOWN = True
            self.__UP, self.__RIGHT, self.__LEFT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__x += 1
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)
        

    def setBoat(self): 
        if self.__UP or self.__DOWN: 
            pass
        else: 
            pass
    

class AtkPlane:
    def __init__(self): #class constructor
        self.__x = 6
        self.__y = 0
        self.__moves = 0
        self.__countX = 0
        self.__countDebris = 0
        self.__countBoat = 0
        self.__check = ToCheck()
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__turn = Turn()
    
    #def getCoords(self):
    #return self.__x, self.__y

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

    def attack(self):
        self.__moves += 1 #Movement cont
        if not self.__check.checkLimitUp(self.__x, self.__y):
            if self.__ID == 4.1: #Player looks up
                if self.__check.checkUpBoat(self.__x, self.__y):  
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

        if not self.__check.checkLimitDown(self.__x, self.__y):
            if self.__ID == 4.2: #Player looks down
                if self.__check.checkDownBoat(self.__x, self.__y): 
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

        if not self.__check.checkLimitRight(self.__x, self.__y):
            if self.__ID == 4.3: #player looks right
                if self.__check.checkRightBoat(self.__x, self.__y): #Player looks up
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
        
        if not self.__check.checkLimitLeft(self.__x, self.__y):
            if self.__ID == 4.4: # player looks left
                if self.__check.checkLeftBoat(self.__x, self.__y): #Player looks up
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

class PcAttackPlayerMatrix(object):#TODO:
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
        cls.__result = [pNew,newID]
        return cls.__result

class Computer:
    def __init__(self):
        self.__pcapMatrix = PcAttackPlayerMatrix()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__history = []

    def generateCoords(self):
        self.__x = random.randint(1,10)
        self.__y = random.randint(1,10)
        self.__randomCoord = [self.__x, self.__y]
        return self.__randomCoord

    def addHistory(self):
        self.__history.append(self.__randomCoord)

    def getHistory(self):
        return self.__history 

    def attack(self):
        self.__matrix = self.__pcapMatrix.getMatrix()
        self.__coords = self.generateCoords()

        if not self.__check.checkCoordDisp(self.__coords, self.__history):
            if self.__matrix[self.__x][self.__y] == -1:
                self.__ID = 3
            else:
                self.__ID = 5 
            self.__history.append(self.__coords)
            self.__turn.setTurn(True)
            print("coords: ", self.__coords, "History: ",self.__history)
            return self.__pcapMatrix.updateAttack(self.__coords, self.__ID)
        else:
            return self.attack()

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor TODO:
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__atkPlane = AtkPlane()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__pcapMatrix = PcAttackPlayerMatrix() 
        self.__computerAttack = Computer()
        self.__arrow = Arrow()

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

    def getComputer(self):
        return self.__computerAttack
    
    def getArrow(self):
        return self.__arrow