import tkinter as tk
from tkinter import PhotoImage, messagebox
import pygame, copy, random
from lib.gameBoards import playerAtPc, pcAtPlayer

#Constantes
BLACK = 'Black'
WIDTH = 384
HEIGHT = 384
HELVETICA = 'Helvetica'

class GraphicUserInterface(tk.Tk):
    """Principal class"""
     
    def __init__(self, *args, **kwargs):# constructor
         
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

        self.frames = {} # creating an empty list to add the frames

        for screenFrame in (MainMenu, setupBoatScreen, GameScreen, TutorialScreen): # movement through pages(Frames) 
            frame = screenFrame(self.__container, self)
            self.frames[screenFrame] = frame #save the frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.showFrame(MainMenu)#First Frame to show

    def showFrame(self, cont): #Method to change the frame
        frame = self.frames[cont]
        frame.tkraise()

    def __setupMatrix(self): #Load each matrix
        self.__gameSetup.getPapcMatrix().loadMatrix(copy.deepcopy(playerAtPc)) #the "copy" is used to create a new object.
        self.__gameSetup.getpcapMatrix().loadMatrix(copy.deepcopy(pcAtPlayer)) #the "copy" is used to create a new object.
    
    def __configureWindow(self): #Main window Setup
        self.title("BATTLESHIP")
        self.geometry("773x409+300+150")
        self.iconbitmap('media/icon.ico') #TODO: Revisar compatibilidad con mac
        self.resizable(False, False)

    def __setupMusic(self): #Background music setup
        pygame.mixer.init()#Starting pygame 
        pygame.mixer.music.load("sound/menuTrack.mp3")#Import Soundtrack
        pygame.mixer.music.play(loops=-1) #Play the song while the game is running
           
    def __setupPause(self): #Pause background music
        pygame.mixer.music.pause() #Pause the song 

    def __setupPlay(self):#Play background music
        pygame.mixer.music.play() #Play the song 
    
    def __aboutDevelopers(self):#Show developers info
        messagebox.showinfo('About Developers', ' Made by:\n Yherland Elizondo Cordero - 2022289492\n Kun Kin Zheng Liang - 2022205015')

    def __topMenu(self): #Top menu configuration
        #help section
        menubar = tk.Menu(self, foreground=BLACK, activeforeground=BLACK)  
        file = tk.Menu(menubar, tearoff=1, foreground=BLACK) 
        file.add_command(label= "About Developers",command = self.__aboutDevelopers)
        file.add_command(label= "Read Tutorial!", command= lambda: self.showFrame(TutorialScreen))
        file.add_command(label= "Main Menu", command= lambda: self.showFrame(MainMenu))
        file.add_separator()  
        file.add_command(label="Salir", command= self.quit)  
        menubar.add_cascade(label="Help", menu= file)  
        #game section
        about = tk.Menu(menubar, tearoff= 0)  
        about.add_command(label= "Save")  
        about.add_command(label= "Load") 
        menubar.add_cascade(label= "Game", menu= about) 
        #hall of fame section
        hallOfFame = tk.Menu(menubar, tearoff= 0)  
        hallOfFame.add_command(label= "Go!") 
        menubar.add_cascade(label= "Hall Of Fame", menu= hallOfFame) 
        #music section
        music = tk.Menu(menubar, tearoff=0)
        music.add_command(label="Play", command = self.__setupPlay)  
        music.add_command(label="Mute", command= self.__setupPause)  
        menubar.add_cascade(label="Music", menu=music)
        
        self.config(menu=menubar) 

class MainMenu(tk.Frame):
    """Main menu screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor
        self.__initComponents(controller) #The controller argument it's used to change the frames

    def __initComponents(self, controller): #widget calling
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupEntry()
        self.__setupButton(controller)
        self.__setupLabel()
        
    def __setupButton(self,controller): # Play button configuration
        playButton = tk.Button(self, text="Play", font=(HELVETICA, 15, 'bold'), width=10, command= lambda : controller.showFrame(setupBoatScreen))
        playButton.place(x=320, y=280)

    def __setupCanvas(self): #Canva configuration
        self.__menuCanva = tk.Canvas(self, width=800, height=600, borderwidth=0)
        self.__menuCanva.place(x=0, y=0)

    def __setupBackground(self): #background image configuration
        global bgImg #Global variable to show the image
        bgImg = PhotoImage(file= "media/menu.png") 
        bgLabel = tk.Label(self.__menuCanva, image = bgImg)
        bgLabel.place(x=0, y=0)

    def __setupLabel(self): #Label configuration
        entryLabel = tk.Label(self.__menuCanva, text="Username: ", font=(HELVETICA, 10, 'bold'))
        entryLabel.place(x=350, y=205)       

    def __setupEntry(self): #Name entry configuration
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
        self.__boatNumber = BoatNumber()
        self.__initComponents(controller)
        
    def __initComponents(self, controller): #widget calling
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespcap()
        self.__setupKeyboardInput()    
        self.__setupLabel()
        self.__setupButton(controller)

    def __setupCanvas(self): #canvas configuration
        #Information canva
        self.__infoCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="blue")
        self.__infoCanvas.place(x=385, y=0)
        #Boats configuration canva
        self.__setupCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT) 
        self.__setupCanvas.place(x=0, y=0)
        #info display canva
        self.__countBoatCanvas = tk.Canvas(self, width=122, height=30, bg=BLACK) 
        self.__countBoatCanvas.place(x=323, y=0)
    
    def __setupButton(self, controller):
        playButton = tk.Button(self.__infoCanvas, text="Next", font=(HELVETICA, 15, 'bold'), width=5, command= lambda : self.__playCommand(controller))
        playButton.place(x=310, y=340) 

    def __playCommand(self, controller):
        boat =  self.__boatNumber.getBoatNumber()
        matrixToSave = self.__gameSetup.getpcapMatrix().getMatrix()

        if boat >= 4:
            self.__gameSetup.getpcapMatrix().loadMatrix(matrixToSave)
            controller.showFrame(GameScreen)
        else:
            messagebox.showinfo('Error', 'Please, place all boats')

    def __setupLabel(self): #label configuration
        boat =  self.__boatNumber.getBoatNumber()
        if boat == 1:
            self.__boat = tk.Label(self.__countBoatCanvas, text='1st Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        elif boat == 2:
            self.__boat = tk.Label(self.__countBoatCanvas, text='2nd Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        else: 
            self.__boat = tk.Label(self.__countBoatCanvas, text='3rd Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        self.__boat.place(x=30, y=5)  

    def __setupKeyboardInput(self): #Keyboard configuration
        self.bind_all('<Right>', lambda event: self.__move(self.__gameSetup.getArrow().moveRight))
        self.bind_all('<Up>', lambda event: self.__move(self.__gameSetup.getArrow().moveUp))
        self.bind_all('<Down>', lambda event: self.__move(self.__gameSetup.getArrow().moveDown))
        self.bind_all('<Left>', lambda event: self.__move(self.__gameSetup.getArrow().moveLeft))
        self.bind_all('<k>', lambda event: self.__placeBoat(self.__gameSetup.getArrow().setBoat)) 

    def __move(self, pMoveFunction):  #general movement function, receive the function to execute
        movement = pMoveFunction()
        self.__updateVisualPcapMatrix(movement[0], movement[1])

    def __placeBoat(self, pSetFunction):#boat placement logic #TODO:hay que cambiar la logica de esta parte
        place = pSetFunction() # returns (((x,y)...), id)
        self.__updateVisualPcapMatrixPlaceBoat(place, place[2])
    
    def __updateVisualPcapMatrix(self, oldMovement, newMovement): #Visual matrix update (used to show movements)
        tk.Label(self.__setupCanvas, image=self.__getImage(oldMovement[1]), bg=BLACK).place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__setupCanvas, image=self.__getImage(newMovement[1]), bg=BLACK).place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)
    
    def __updateVisualPcapMatrixPlaceBoat(self, place, exit): #Visal matrix update (used to show the boat placement)
        if exit == 1:
            self.__setupLabel()
            for coord in place[0]: 
                tk.Label(self.__setupCanvas, image=self.__getImage(place[1]), bg=BLACK).place(x=coord[1]*32,y=coord[0]*32)
    
    def __setupImagesFiles(self): #Fucntion to save all the images on RAM
        self.__arrowUp = PhotoImage(file= "media/arrowUp.png")
        self.__arrowDown = PhotoImage(file= "media/arrowDown.png")
        self.__arrowRight = PhotoImage(file= "media/arrowRight.png")
        self.__arrowLeft = PhotoImage(file= "media/arrowLeft.png")
        self.__waterBlock = PhotoImage(file= "media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file= "media/stoneBlock.png")
        self.__roadBoatHor = PhotoImage(file= "media/roadBoatHor.png")
        self.__roadBoatVer = PhotoImage(file= "media/roadBoatVert.png")

    def __getImage(self, id): #Function that return an image using the ID
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
        elif id == 1.1:
            return self.__roadBoatVer
        elif id == 1.2:
            return self.__roadBoatHor
        else: 
            return self.__waterBlock
            
    def __setupImagespcap(self): #Show the visual matrix
        matrixpcap = self.__gameSetup.getpcapMatrix().getMatrix() #Getting the matrix
        for i in range(0,len(matrixpcap)): #Using iteration to go through the array
            for j in range(0,len(matrixpcap[0])):
                tk.Label(self.__setupCanvas, image=self.__getImage(matrixpcap[i][j]), bg=BLACK).place(x=j*32,y=i*32)

class GameScreen(tk.Frame):
    """Game Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__turn = Turn()
        self.__initialScreen()  

    def __initialScreen(self):
        #Canva
        self.__initialCanva = tk.Canvas(self, width=768, height=384, bg="white")
        self.__initialCanva.place(x=0, y=0)
        #Background image
        global intImg
        intImg = PhotoImage(file= "media/intermediateScreen.png") 
        intLabel = tk.Label(self.__initialCanva, image = intImg)
        intLabel.place(x=0, y=0)
        #Button
        tk.Button(self, text="Start", font=(HELVETICA, 15, 'bold'), width=8, command= lambda : self.__initComponents()).place(x=340, y=260)
        
    def __initComponents(self): #widget calling
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespapc()
        self.__setupImagespcap()
        self.__setupKeyboardInput()
        
    def __setupCanvas(self): #canvas configuration
        """Canvas configuration"""
        #boat canvas
        self.__boatsCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="blue")
        self.__boatsCanvas.place(x=0, y=0)
        #game canvas
        self.__gameCanvas = tk.Canvas(self, width=WIDTH, height=HEIGHT) 
        self.__gameCanvas.place(x=385, y=0)
        #count canvas
        self.__countCanvas = tk.Canvas(self, width=122, height=30, bg=BLACK) 
        self.__countCanvas.place(x=323, y=0)

    def __setupKeyboardInput(self): #Keyboard configuration
        self.bind_all('<d>', lambda event: self.__move(self.__gameSetup.getPlane().moveRight))
        self.bind_all('<w>', lambda event: self.__move(self.__gameSetup.getPlane().moveUp))
        self.bind_all('<s>', lambda event: self.__move(self.__gameSetup.getPlane().moveDown))
        self.bind_all('<a>', lambda event: self.__move(self.__gameSetup.getPlane().moveLeft))
        self.bind_all('<j>', lambda event: self.__attack(self.__gameSetup.getPlane().attack)) #Ejecutar el "disparo", ademas tiene que cambiar el estado de turno

    def __attack(self, pMoveFunction): #Attack function
        if self.__turn.getTurn():
            position = pMoveFunction()
            self.__updateVisualPapcMatrixAttack(position)
        else:
            position = self.__gameSetup.getComputer().attack()
            self.__updateVisualPcapMatrix(position)

    def __move(self, pMoveFunction): #General move function, used to move the plane
        if self.__turn.getTurn():
            movement = pMoveFunction()
            self.__updateVisualPapcMatrix(movement[0], movement[1])
            
    def __updateVisualPapcMatrix(self, oldMovement, newMovement): # update visual matrix, used to move the plane in the visual matrix
        tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg=BLACK).place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg=BLACK).place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __updateVisualPapcMatrixAttack(self, position):# update visual papcmatrix, used to show the attacks
        tk.Label(self.__gameCanvas, image=self.__getImage(position[1]), bg=BLACK).place(x=position[0][1]*32,y=position[0][0]*32)
    
    def __updateVisualPcapMatrix(self, position): #update visual pcapmatrix, used to show the attacks
        tk.Label(self.__boatsCanvas, image=self.__getImage(position[1]), bg=BLACK).place(x=position[0][1]*32,y=position[0][0]*32)

    def __setupImagesFiles(self): #saving the images on RAM
        self.__planeUp = PhotoImage(file= "media/planeUp.png")
        self.__planeDown = PhotoImage(file= "media/planeDown.png")
        self.__planeLeft = PhotoImage(file= "media/planeLeft.png")
        self.__planeRight = PhotoImage(file= "media/planeRight.png")
        self.__waterBlock = PhotoImage(file= "media/waterBlock.png")
        self.__stoneBlock = PhotoImage(file= "media/stoneBlock.png")
        self.__missBlock = PhotoImage(file= "media/missBlock.png")
        self.__debrisBlock = PhotoImage(file= "media/debrisBlock.png")
        self.__playerBoat = PhotoImage(file = "media/roadBoatHor.png")
        self.__horBoat = PhotoImage(file= "media/roadBoatHor.png")
        self.__vertBoat = PhotoImage(file= "media/roadBoatVert.png")

    def __getImage(self, id): # function that return an image using the ID
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
        elif id == 1.1:
            return self.__vertBoat
        elif id == 1.2:
            return self.__horBoat
        else:
            return self.__waterBlock

    def __setupImagespapc(self): # Carga todas las imagenes visualmente #TODO: POR AQUI SE QUEDO COMENTANTO CODIGO
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
        
    def checkLimitRightPapc(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 7

    def checkLimitLeftPapc(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 7

    def checkLimitDownPapc(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 7

    def checkLimitUpPapc(self, pX, pY):
        self.__x = pX
        self.__y = pY 
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 7
    
    def checkLimitRightPcap(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 7

    def checkLimitLeftPcap(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 7

    def checkLimitDownPcap(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 7

    def checkLimitUpPcap(self, pX, pY):
        self.__x = pX
        self.__y = pY 
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 7

    def checkRightBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == 1

    def checkLeftBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 1

    def checkDownBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == 1

    def checkUpBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 1
#---------------------------------
    def checkRightBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 1

    def checkLeftBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 1

    def checkDownBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 1

    def checkUpBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 1
#======================
    def checkUpDebris(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == 3 #TODO:

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
    
    def checkPlaceCoordsDisp(self, cord, history): # function to check if the random place coord is avialable
        self.__estado = False
        for verify in history:
            if verify == cord:
                self.__estado = True
                break
        return self.__estado

    def checkHorBoatsLeft(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 1.2
    
    def checkVerBoatsLeft(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == 1.1

    def checkHorBoatsRight(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 1.2
    
    def checkVerBoatsRight(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == 1.1

    def checkHorBoatsUp(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 1.2
    
    def checkVerBoatsUp(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == 1.1
    
    def checkHorBoatsDown(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 1.2
    
    def checkVerBoatsDown(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == 1.1

    def checkLimitUpTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 2][self.__y] == 7
    
    def checkLimitDownTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 2][self.__y] == 7

    def checkLimitRightTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 2] == 7 
    
    def checkLimitLeftTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 2] == 7 

    def checkLimitUpThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 3][self.__y] == 7
    
    def checkLimitDownThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 3][self.__y] == 7

    def checkLimitRightThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 3] == 7 
    
    def checkLimitLeftThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 3] == 7 
    
    def checkBoatUpPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] in self.__values
    
    def checkBoatDownPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] in self.__values

    def checkBoatRightPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] in self.__values
    
    def checkBoatLeftPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] in self.__values
    
    def checkBoatUpTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x - 2][self.__y] in self.__values
    
    def checkBoatDownTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x + 2][self.__y] in self.__values

    def checkBoatRightTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 2] in self.__values
    
    def checkBoatLeftTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 2] in self.__values

    def checkBoatUpThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x - 3][self.__y] in self.__values
    
    def checkBoatDownThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x + 3][self.__y] in self.__values

    def checkBoatRightThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 3] in self.__values
    
    def checkBoatLeftThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        self.__values = [1.1, 1.2]
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 3] in self.__values 
        
    def checkLimitUpTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 2][self.__y] == 7
    
    def checkLimitDownTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 2][self.__y] == 7

    def checkLimitRightTwoPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 2] == 7 
    
    def checkLimitLeftTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 2] == 7 

    def checkLimitUpThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 3][self.__y] == 7
    
    def checkLimitDownThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 3][self.__y] == 7

    def checkLimitRightThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 3] == 7 
    
    def checkLimitLeftThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 3] == 7 
    
    def checkBoatUpTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 2][self.__y] == -1
    
    def checkBoatDownTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 2][self.__y] == -1

    def checkBoatRightTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 2] == -1
    
    def checkBoatLeftTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 2] == -1

    def checkBoatUpThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 3][self.__y] == -1
    
    def checkBoatDownThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 3][self.__y] == -1
        
    def checkBoatRightThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 3] == -1
    
    def checkBoatLeftThreePapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 3] == -1

    
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

class Turn(object): # Another singletone to modify and return the "Turn" value
    __instance = None
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = super(Turn, cls).__new__(cls)
            cls.__turn = True
        return cls.__instance

    def setTurn(cls, state): # turn modification 
        cls.__turn = state

    def getTurn(cls): # return the turn value
        return cls.__turn

class BoatNumber(object): # Another singletone to modify and return the "BoatNumber" value, this is used to place the boats, this class return the "type" of boats.
    __instance = None
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = super(BoatNumber, cls).__new__(cls)
            cls.__boatNumber = 1
        return cls.__instance

    def modifyBoatNumber(cls): 
        cls.__boatNumber += 1

    def getBoatNumber(cls): # return the turn value
        return cls.__boatNumber

class Arrow: 
    def __init__(self):
        self.__x = 10
        self.__y = 1
        #self.__countBoat = 0
        self.__RIGHT = False
        self.__LEFT = False
        self.__UP = False
        self.__DOWN = False
        self.__check = ToCheck()
        self.__pcapMatrix = PcAttackPlayerMatrix()
        self.__boatNumber = BoatNumber()
        self.__ID = 9.3
    
    def __setupFxSound(self):
        __constructionFx = pygame.mixer.Sound("sound/constructionSound.mp3")
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

        if not self.__check.checkLimitLeftPcap(self.__x, self.__y):
            self.__LEFT = True
            self.__DOWN, self.__UP, self.__RIGHT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__y -= 1
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)

    def moveRight(self):
        if self.__check.checkVerBoatsRight(self.__x, self.__y):
            self.__oldID = 1.1
        elif self.__check.checkHorBoatsRight(self.__x, self.__y):
            self.__oldID = 1.2 
        else: 
            self.__oldID = 0

        oldY = self.__y
        self.__ID = 9.3

        if not self.__check.checkLimitRightPcap(self.__x, self.__y):
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

        if not self.__check.checkLimitUpPcap(self.__x, self.__y):
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

        if not self.__check.checkLimitDownPcap(self.__x, self.__y):
            self.__DOWN = True
            self.__UP, self.__RIGHT, self.__LEFT = False, False, False
            print(f'UP: {self.__UP}, DOWN: {self.__DOWN}, RIGHT: {self.__RIGHT}, LEFT: {self.__LEFT}')

            self.__x += 1
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)
        

    def setBoat(self):  #TODO:
        self.__actualBoat = self.__boatNumber.getBoatNumber()
        self.__doNothing = (0, 0, 0)

        if self.__ID == 9.1 or self.__ID == 9.2:
            self.__image = 1.1
        else:
            self.__image = 1.2

        if self.__ID == 9.1: #arrowUp
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                limitCondition = self.__check.checkLimitUpPcap(self.__x, self.__y)
                if not limitCondition:
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                limitCondition = self.__check.checkLimitUpPcap(self.__x, self.__y) or self.__check.checkLimitUpTwoPcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatUpPcap(self.__x, self.__y) or self.__check.checkBoatUpTwoPcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y), (self.__x - 2, self.__y)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                limitCondition = self.__check.checkLimitUpPcap(self.__x, self.__y) or self.__check.checkLimitUpTwoPcap(self.__x, self.__y) or self.__check.checkLimitUpThreePcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatUpPcap(self.__x, self.__y) or self.__check.checkBoatUpTwoPcap(self.__x, self.__y) or self.__check.checkBoatUpThreePcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y), (self.__x - 2, self.__y), (self.__x - 3, self.__y)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                
        if self.__ID == 9.2: # arrowDown
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                limitCondition = self.__check.checkLimitDownPcap(self.__x, self.__y)
                if not limitCondition:
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                limitCondition = self.__check.checkLimitDownPcap(self.__x, self.__y) or self.__check.checkLimitDownTwoPcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatDownPcap(self.__x, self.__y) or self.__check.checkBoatDownTwoPcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y), (self.__x + 2, self.__y)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                limitCondition = self.__check.checkLimitDownPcap(self.__x, self.__y) or self.__check.checkLimitDownTwoPcap(self.__x, self.__y) or self.__check.checkLimitDownThreePcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatDownPcap(self.__x, self.__y) or self.__check.checkBoatDownTwoPcap(self.__x, self.__y) or self.__check.checkBoatDownThreePcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y), (self.__x + 2, self.__y), (self.__x + 3, self.__y)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
        
        if self.__ID == 9.3: #arrowRight
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                limitCondition = self.__check.checkLimitRightPcap(self.__x, self.__y)
                if not limitCondition:
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                limitCondition = self.__check.checkLimitRightPcap(self.__x, self.__y) or self.__check.checkLimitRightTwoPcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatRightPcap or self.__check.checkBoatRightTwoPcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1), (self.__x, self.__y + 2)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                limitCondition = self.__check.checkLimitRightPcap(self.__x, self.__y) or self.__check.checkLimitRightTwoPcap(self.__x, self.__y) or self.__check.checkLimitRightThreePcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatRightPcap(self.__x, self.__y) or self.__check.checkBoatRightTwoPcap(self.__x, self.__y) or self.__check.checkBoatRightThreePcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1), (self.__x, self.__y + 2), (self.__x, self.__y + 3)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                
        if self.__ID == 9.4: #arrowLeft
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                limitCondition = self.__check.checkLimitLeftPcap(self.__x, self.__y)
                if not limitCondition:
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                limitCondition = self.__check.checkLimitLeftPcap(self.__x, self.__y) or self.__check.checkLimitLeftTwoPcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatLeftPcap or self.__check.checkBoatLeftTwoPcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1), (self.__x, self.__y - 2)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                limitCondition = self.__check.checkLimitLeftPcap(self.__x, self.__y) or self.__check.checkLimitLeftTwoPcap(self.__x, self.__y) or self.__check.checkLimitLeftThreePcap(self.__x, self.__y)
                boatCondition = self.__check.checkBoatLeftPcap(self.__x, self.__y) or self.__check.checkBoatLeftTwoPcap(self.__x, self.__y) or self.__check.checkBoatLeftThreePcap(self.__x, self.__y)
                if not limitCondition and not boatCondition:
                    self.__setupFxSound() 
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1), (self.__x, self.__y - 2), (self.__x, self.__y - 3)], self.__image, 1)
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
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
        self.__ID = 4.3
    
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

        if not self.__check.checkLimitLeftPapc(self.__x, self.__y):
            self.__y -= 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldID, self.__ID)

    def moveRight(self):
        if self.__check.checkLimitUpPapc(self.__x, self.__y) and self.__check.checkLimitDownPapc(self.__x, self.__y):
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

        if not self.__check.checkLimitRightPapc(self.__x, self.__y) :
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

        if not self.__check.checkLimitUpPapc(self.__x, self.__y):
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

        if not self.__check.checkLimitDownPapc(self.__x, self.__y):
            self.__x += 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.__papcMatrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldID, self.__ID)

    def attack(self):
        self.__moves += 1 #Movement cont
        if not self.__check.checkLimitUpPapc(self.__x, self.__y):
            if self.__ID == 4.1: #Player looks up
                if self.__check.checkUpBoatPapc(self.__x, self.__y):  
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

        if not self.__check.checkLimitDownPapc(self.__x, self.__y):
            if self.__ID == 4.2: #Player looks down
                if self.__check.checkDownBoatPapc(self.__x, self.__y): 
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

        if not self.__check.checkLimitRightPapc(self.__x, self.__y):
            if self.__ID == 4.3: #player looks right
                if self.__check.checkRightBoatPapc(self.__x, self.__y): #Player looks up
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
        
        if not self.__check.checkLimitLeftPapc(self.__x, self.__y):
            if self.__ID == 4.4: # player looks left
                if self.__check.checkLeftBoatPapc(self.__x, self.__y): #Player looks up
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

class PcAttackPlayerMatrix(object): #TODO:
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

    def updateBoat(cls, pNewTuple, newID, exit): #TODO:
        if exit == 1:
            for pNew in pNewTuple: 
                cls.__matrix[pNew[0]][pNew[1]] = newID
            return pNewTuple, newID, 1
        else:
            return pNewTuple, newID, 0
    
class Computer: #TODO:
    def __init__(self):
        self.__pcapMatrix = PcAttackPlayerMatrix()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__history = []
        self.__placeHistory = []
    
    def setupFxSound(self, fxID):
        if fxID == 1:
            __explotionFx = pygame.mixer.Sound("sound/explotionSound.mp3")
            __explotionFx.play() 
        else:
            __missFx = pygame.mixer.Sound("sound/missSound.mp3")
            __missFx.play() 

    def generateCoords(self):
        self.__x = random.randint(1,10)
        self.__y = random.randint(1,10)
        self.__randomCoord = [self.__x, self.__y]
        return self.__randomCoord
    
    def generateOrientation(self):
        self.__orientation = random.randint(1,4)
        return self.__orientation

    def addHistory(self, coords):
        self.__history.append(coords)
    
    def addPlaceHistory(self, coords):
        self.__placeHistory.append(coords)
    
    def getPlaceHistory(self):
        return self.__placeHistory

    def getHistory(self):
        return self.__history 

    def attack(self):
        self.__matrix = self.__pcapMatrix.getMatrix()
        self.__coords = self.generateCoords()

        if not self.__check.checkCoordDisp(self.__coords, self.__history):
            if self.__matrix[self.__x][self.__y] == 1.1 or self.__matrix[self.__x][self.__y] == 1.2:
                self.setupFxSound(1)
                self.__ID = 3
            else:
                self.setupFxSound(2)
                self.__ID = 5 
            self.addHistory(self.__coords)
            self.__turn.setTurn(True)
            print("coords: ", self.__coords, "History: ",self.__history)
            return self.__pcapMatrix.updateAttack(self.__coords, self.__ID)
        else:
            return self.attack()

    def getPlaceCoord(self):
        self.__coords = self.generateCoords()
        return self.__coords
    
    def getOrientationCoord(self):
        self.__orient = self.generateOrientation()
        return self.__orient

    def placeBoats(self): #TODO: pensar como ejecutar esto diferentes veces, digamos hacerlo como en un ciclo, que pasa si no se cumple la condicion basicamente
        self.__matrix = self.__pcapMatrix.getMatrix()
        self.__randomBoat = RandomBoatNumber()
        doNothing = (0,0,0)
        if self.__randomBoat.getBoatNumber > 3:
            return doNothing#TODO: CHECK THIS

        if self.__randomBoat.getBoatNumber == 1:
            self.__coords = self.getPlaceCoord()
            if not self.__check.checkPlaceCoordsDisp(self.__coords, self.__placeHistory):
                if self.__orient == 1:#Up
                    __limitCondition = self.__check.checkLimitUpPapc(self.__coords[0], self.__coords[1])
                if not __limitCondition:
                    pass

                elif self.__orient == 2:#Right
                    pass
                elif self.__orient == 3: #Down
                    pass
                else:#Left
                    pass
            else:
                return self.placeBoats()

class RandomBoatNumber(object): 
    __instance = None
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = super(RandomBoatNumber, cls).__new__(cls)
            cls.__randomBoatNumber = 1
        return cls.__instance

    def modifyBoatNumber(cls): 
        cls.__randomBoatNumber += 1

    def getBoatNumber(cls): # return the turn value
        return cls.__randomBoatNumber

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
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