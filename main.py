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

import tkinter as tk
from tkinter import PhotoImage, messagebox
from turtle import color
import pygame, copy, random, json
from lib.gameBoards import playerAtPc, pcAtPlayer
from JsonManager import JsonManager

#constants
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
        self.__setupMatrix()

        # creating a container
        self.__container = tk.Frame(self) 
        self.__container.pack(side = "top", fill = "both", expand = True)
        self.__container.grid_rowconfigure(0, weight = 1)
        self.__container.grid_columnconfigure(0, weight = 1)

        self.frames = {} # creating an empty list to add the frames

        for screenFrame in (MainMenu, setupBoatScreen, GameScreen, GameOverScreen, HallOfFame): # movement through pages(Frames) 
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
           
    def __setupPause(self): #Pause background music
        pygame.mixer.music.pause() #Pause the song 

    def __setupVictorySound(self):
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load("sound/victorySound.mp3")
        pygame.mixer.music.play()

    def __setupPlay(self):#Play background music
        pygame.mixer.music.play() #Play the song 
    
    def __aboutDevelopers(self):#Show developers info
        messagebox.showinfo('BATTLESHIP', ' Made by:\n Yherland Elizondo Cordero - 2022289492\n Kun Kin Zheng Liang - 2022205015')

    def __topMenu(self): #Top menu configuration
        #help section
        menubar = tk.Menu(self, foreground=BLACK, activeforeground=BLACK)  
        file = tk.Menu(menubar, tearoff=1, foreground=BLACK) 
        file.add_command(label= "About Developers",command = self.__aboutDevelopers)
        file.add_separator()  
        file.add_command(label="Exit", command= self.quit)  
        menubar.add_cascade(label="About Developers", menu= file)  
        #game section
        about = tk.Menu(menubar, tearoff= 0)  
        about.add_command(label= "Save", command = self.__saveGame)  
        about.add_command(label= "Load", command = self.__loadGame) 
        menubar.add_cascade(label= "Game", menu= about) 
        #music section
        music = tk.Menu(menubar, tearoff=0)
        music.add_command(label="Play", command = self.__setupPlay)  
        music.add_command(label="Mute", command= self.__setupPause)  
        menubar.add_cascade(label="Music", menu=music)
        
        self.config(menu=menubar) 

    def __saveGame(self): #function to save the game 
        messagebox.showinfo('Saving Game...',  'Your game has been saved!')

        #saving the parameters on variables
        pcapMatrix = self.__gameSetup.getpcapMatrix().getMatrix()
        papcMatrix = self.__gameSetup.getPapcMatrix().getMatrix()
        turn = self.__gameSetup.getState().getTurn()
        planeMoves = self.__gameSetup.getState().getMoves()
        destroyedPcap = self.__gameSetup.getState().getDestroyedPcap()
        destroyedPapc = self.__gameSetup.getState().getDestroyedPapc()
        pcapMatrixMoves = self.__gameSetup.getState().getPcapMatrixMoves()
        name = self.__gameSetup.getState().getName()

        #usign a dictionary to save all configurations
        gameConfig = {
            "pcapMatrix": pcapMatrix,
            "papcMatrix": papcMatrix, 
            "turn": turn, 
            "moves": planeMoves,
            "destroyedPcap": destroyedPcap, 
            "destroyedPapc": destroyedPapc,
            "pcapMatrixMoves": pcapMatrixMoves,
            "name": name
        }
        #saving the dictionary on a json file
        with open("data/config.json", "w") as outfile:
            json.dump(gameConfig, outfile)

    def __loadGame(self):#fucntion to load the game
        messagebox.showinfo('Loading...',  'Your game is ready!')

        #load the content of the json file
        loadInfo = open("data/config.json")
        data = json.load(loadInfo)

        #removing the plane of the matrix and initializing the coords in [6,0]
        papcMatrix = data["papcMatrix"] #this is for delete the plane image when the game charges, also, it's used to set the initial positition
        for fila in range(len(papcMatrix)):
            for columna in range(len(papcMatrix[0])):
                if papcMatrix[fila][columna] == 4.3 or papcMatrix[fila][columna] == 4.1 or papcMatrix[fila][columna] == 4.2 or papcMatrix[fila][columna] == 4.4:
                   papcMatrix[fila][columna] = 0
        papcMatrix[6][0] = 4.3
        #Loading all the parameters saved in our program
        self.__gameSetup.getPapcMatrix().loadMatrix(papcMatrix) 
        self.__gameSetup.getpcapMatrix().loadMatrix(data["pcapMatrix"])
        self.__gameSetup.getState().setTurn(data["turn"])
        self.__gameSetup.getState().setMoves(data["moves"])
        self.__gameSetup.getPlane().setMoves(data["moves"])
        self.__gameSetup.getState().setDestroyedPcap(data["destroyedPcap"])
        self.__gameSetup.getState().setDestroyedPapc(data["destroyedPapc"])
        self.__gameSetup.getState().setPcapMatrixMoves(data["pcapMatrixMoves"])
        self.__gameSetup.getState().setName(data["name"])
        #changing the screen
        self.showFrame(GameScreen)

        
class MainMenu(tk.Frame):
    """Main menu screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor
        self.__initComponents(controller) #The controller argument it's used to change the frames
        self.__gameSetup = GameSetup()

    def __initComponents(self, controller): #widget calling
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupEntry()
        self.__setupButton(controller)
        self.__setupMusic()
        self.__setupLabel()
        
    def __setupButton(self,controller): # Play button configuration
        playButton = tk.Button(self, text="Play", font=(HELVETICA, 15, 'bold'), width=10, command= lambda : [controller.showFrame(setupBoatScreen), self.__saveUsername()])
        playButton.place(x=320, y=280)
    
    def __setupMusic(self): #Background music setup
        pygame.mixer.init()#Starting pygame 
        pygame.mixer.music.load("sound/menuTrack.mp3")#Import Soundtrack
        pygame.mixer.music.play(loops=-1) #Play the song while the game is running

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
    
    def __saveUsername(self):#function to save the name of the player 
        user = self.__userNameInput.get()
        self.__gameSetup.getState().setName(user)
        
class setupBoatScreen(tk.Frame):
    """Setup boat screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__initComponents(controller)
        
    def __initComponents(self, controller): #widget calling
        self.__setupCanvas()
        self.__setupInstructions()
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

    def __setupInstructions(self): #background image configuration
        global InsImg
        InsImg =  PhotoImage(file= "media/instructionsScreen.png")
        tk.Label(self.__infoCanvas, image= InsImg).place(x=0, y=0)
    
    def __setupButton(self, controller): #funtion to configure the Next button
        playButton = tk.Button(self.__infoCanvas, text="Next", font=(HELVETICA, 15, 'bold'), width=5, command= lambda : self.__playCommand(controller))
        playButton.place(x=310, y=340) 

    def __playCommand(self, controller): #this function execute the random boat placement 3 times, then save the matrix to refresh the screen.
        num = 0
        for execution in range(0,3):
            num += 1
            self.__gameSetup.getComputer().placeBoats() #place the 3 random boats
        papcMatrixToSave = self.__gameSetup.getPapcMatrix().getMatrix() #get the new matrix
        self.__gameSetup.getPapcMatrix().loadMatrix(papcMatrixToSave) # save the new matrix
         
        boatNumber =  self.__gameSetup.getBoatNumber().getBoatNumber() # number of boats that have been placed
        matrixToSave = self.__gameSetup.getpcapMatrix().getMatrix() # new matrix

        if boatNumber >= 4: # check how many boat have been placed 
            self.__gameSetup.getpcapMatrix().loadMatrix(matrixToSave)
            controller.showFrame(GameScreen)
        else:
            messagebox.showinfo('Error', 'Please, place all boats')

    def __setupLabel(self): #dinamic label configuration, this function update the label with the boar number
        boatNumber =  self.__gameSetup.getBoatNumber().getBoatNumber()
        if boatNumber == 1:
            self.__boat = tk.Label(self.__countBoatCanvas, text='1st Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        elif boatNumber == 2:
            self.__boat = tk.Label(self.__countBoatCanvas, text='2nd Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        elif boatNumber == 3: 
            self.__boat = tk.Label(self.__countBoatCanvas, text='3rd Boat', font=(HELVETICA, 12), bg=BLACK, fg='white')
        else: 
            self.__boat = tk.Label(self.__countBoatCanvas, text='    GO!   ', font=(HELVETICA, 12), bg=BLACK, fg='white')
        self.__boat.place(x=30, y=5)  

    def __setupKeyboardInput(self): #Keyboard configuration
        self.bind_all('<Right>', lambda event: self.__move(self.__gameSetup.getArrow().moveRight))
        self.bind_all('<Up>', lambda event: self.__move(self.__gameSetup.getArrow().moveUp))
        self.bind_all('<Down>', lambda event: self.__move(self.__gameSetup.getArrow().moveDown))
        self.bind_all('<Left>', lambda event: self.__move(self.__gameSetup.getArrow().moveLeft))
        self.bind_all('<k>', lambda event: self.__placeBoat(self.__gameSetup.getArrow().setBoat)) 

    def __move(self, pMoveFunction):  #general movement function, receive the function to execute
        movement = pMoveFunction()
        self.__updateVisualPcapMatrix(movement[0], movement[1], movement[2])

    def __placeBoat(self, pSetFunction): #function to place the boats and update the visual matrix 
        place = pSetFunction() 
        self.__updateVisualPcapMatrixPlaceBoat(place, place[2])
    
    def __updateVisualPcapMatrix(self, oldMovement, newMovement, exit): #Visual matrix update (used to show movements)
        if exit == 1: 
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

    def __getImage(self, id): #Function that return an image using the ID(number in matrix)
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
        self.__jsonManager = JsonManager()
        tk.Frame.__init__(self, parent) #constructor 
        self.__gameSetup = GameSetup()
        self.__turn = Turn()
        self.__initialScreen(controller) #Execute an intermediate screen (this allows screen updating and matrix)
        self.__players = self.__refreshJson()

    def __initialScreen(self, controller):
        #Canva
        self.__initialCanva = tk.Canvas(self, width=768, height=384, bg="white")
        self.__initialCanva.place(x=0, y=0)

        #Background image
        global intImg
        intImg = PhotoImage(file= "media/InstructionsToPlay.png") 
        intLabel = tk.Label(self.__initialCanva, image = intImg)
        intLabel.place(x=0, y=0)

        #Button, this button execute the init
        tk.Button(self, text="Start", font=(HELVETICA, 15, 'bold'), width=8, command= lambda : self.__initComponents(controller)).place(x=340, y=260)
        
    def __initComponents(self, controller): #widget calling
        self.__setupCanvas()
        self.__setupImagesFiles()
        self.__setupImagespapc()
        self.__setupImagespcap()
        self.__setupKeyboardInput(controller)
        self.__labelMove()
        
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

    def __setupWaveSound(self): #Game Over sound
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load("sound/waveSound.mp3")#Import Soundtrack
        pygame.mixer.music.play(loops=-1) #Play the song while the game is running

    def __setupVictorySound(self): #Victory sound
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load("sound/victorySound.mp3")
        pygame.mixer.music.play()

    def __labelMove(self): #label showing how many moves the player has made
        moves =  self.__gameSetup.getState().getMoves()
        self.__boat = tk.Label(self.__countCanvas, text=f'Moves: {moves}', font=(HELVETICA, 14, 'bold'), bg=BLACK, fg='white')
        self.__boat.place(x=13, y=3)
    
    def __setupKeyboardInput(self, controller): #Keyboard configuration
                self.bind_all('<d>', lambda event: self.__move(self.__gameSetup.getPlane().moveRight, controller))
                self.bind_all('<w>', lambda event: self.__move(self.__gameSetup.getPlane().moveUp, controller))
                self.bind_all('<s>', lambda event: self.__move(self.__gameSetup.getPlane().moveDown, controller))
                self.bind_all('<a>', lambda event: self.__move(self.__gameSetup.getPlane().moveLeft, controller))
                self.bind_all('<j>', lambda event: self.__attack(self.__gameSetup.getPlane().attack, controller)) #Ejecutar el "disparo", ademas tiene que cambiar el estado de turno

    def __attack(self, pMoveFunction, controller): #Attack function
        if self.__turn.getPcapMatrixMoves() < 100: #limit to prevent the stack overflow
            if self.__turn.getTurn(): #condition to use turns
                if self.__turn.getDestroyedPapc() != 6: #Player wins
                    if self.__turn.getDestroyedPcap() != 6: # Computer wins
                        position = pMoveFunction()
                        exit = position[2]
                        self.__updateVisualPapcMatrixAttack(position, exit)
                    else:
                        messagebox.showinfo('GAME OVER',  'You lose!')
                        controller.showFrame(GameOverScreen)
                        self.__setupWaveSound()
                else:
                    messagebox.showinfo('WINNER', "Oh you win. I´ll beat you next time, you´ll see!!")
                    self.updatedJson({ "name":self.__gameSetup.getState().getName(), "movements":self.__gameSetup.getState().getMoves()})
                    controller.showFrame(HallOfFame)
                    self.__setupVictorySound()
            else:
                position = self.__gameSetup.getComputer().attack()
                self.__updateVisualPcapMatrix(position)
        else:
            messagebox.showinfo('Error', 'Too much moves')
            
            controller.showFrame(GameOverScreen)
            self.__setupWaveSound()

    def __move(self, pMoveFunction, controller): #General move function, used to move the plane
        if self.__turn.getPcapMatrixMoves() < 100: #limit to prevent the stack overflow
            if self.__turn.getTurn():#condition to use turns
                if self.__turn.getDestroyedPapc() != 6: #Player wins
                    if self.__turn.getDestroyedPcap() != 6: # Computer wins
                        movement = pMoveFunction()
                        self.__updateVisualPapcMatrix(movement[0], movement[1], movement[2])
                    else: 
                        messagebox.showinfo('GAME OVER',  'You lose!')
                        controller.showFrame(GameOverScreen)  
                        self.__setupWaveSound()              
                else:
                    messagebox.showinfo('WINNER', "Oh you win. I´ll beat you next time, you´ll see!!")
                    self.updatedJson({ "name":self.__gameSetup.getState().getName(), "movements":self.__gameSetup.getState().getMoves()})
                    controller.showFrame(HallOfFame)
                    self.__setupVictorySound()
        else:
            messagebox.showinfo('Error', 'Too much moves')
            controller.showFrame(GameOverScreen)
            self.__setupWaveSound()

    def sortByMovement(self, pElement):#TODO: QUEDA COMENTAR ESTA PARTE
        return pElement['movements']
    
    def __insertPlayer(self, pDict, pElement): #inster the name to the list, then sort the list
        pDict.append(pElement)
        pDict.sort(key=self.sortByMovement)
        return pDict
    
    def __refreshJson(self):
        self.__players = self.__jsonManager.readJson('data/players.json')['results']
    
    def __savePlayers(self):
        self.__jsonManager.writeJson('data/players.json', {"results":self.__players})

    def updatedJson(self, value):
        self.__refreshJson()
        self.__players = self.__insertPlayer(self.__players, value)
        self.__savePlayers()
        

    def __updateVisualPapcMatrix(self, oldMovement, newMovement, exit): # update visual matrix, used to move the plane in the visual matrix
        if exit == 1: #used to ignore some situations
            tk.Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg=BLACK).place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
            tk.Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg=BLACK).place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __updateVisualPapcMatrixAttack(self, position, exit):# update visual papcmatrix, used to show the attacks
        if exit == 1: #used to ignore some situations
            self.__labelMove()#update the move label
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
class HallOfFame(tk.Frame):
    """Hall of fame screen"""
    def __init__(self, parent, controller): #constructor
        self.__players = []
        tk.Frame.__init__(self, parent) #constructor 
        self.__jsonManager = JsonManager()
        self.__players = self.__refreshJson()
        self.__initComponents()
    
    def __refreshJson(self):
        self.__players = self.__jsonManager.readJson('data/players.json')['results']
        return self.__players

    def __initComponents(self): #widget calling
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupFameLabels()
        self.__refreshButton()
        self.__quitButton()

    def __setupCanvas(self): #canvas configuration
        """Canvas configuration"""
        self.__hallOfFame = tk.Canvas(self, width=768, height=384, bg='white')
        self.__hallOfFame.place(x=0, y=0)

    def __setupBackground(self):
        global bgOImg
        bgOImg = PhotoImage(file= "media/hallOfFame.png") 
        bgOImgLabel = tk.Label(self.__hallOfFame, image = bgOImg)
        bgOImgLabel.place(x=0, y=0)

    def __setupFameLabels(self):
        pX = 205
        pY = 112
        cont = 0
        for player in self.__players:
            if cont > 4:
                break
            cont += 1
            hallOfName = tk.Label(self.__hallOfFame, text= player["name"], bg="black", fg="white", font=(HELVETICA, 12, 'bold'))
            hallOfName.place(x= pX, y= pY)

            hallOfMoves = tk.Label(self.__hallOfFame, text= player["movements"], bg="black", fg="white", font=(HELVETICA, 12, 'bold'))
            hallOfMoves.place(x= pX * 2.6, y= pY)
                
            pY += 37

    def __refreshButton(self):
        playButton = tk.Button(self, text="Refresh", font=(HELVETICA, 15, 'bold'), width=10, command= self.__refresh)
        playButton.place(x=168, y=290)

    def __quitButton(self):
        quitButton = tk.Button(self, text="Quit", font=(HELVETICA, 15, 'bold'), width=10, command= self.__command)
        quitButton.place(x=476, y=290)  

    def __refresh(self):
        self.__players = self.__jsonManager.readJson('data/players.json')['results']
        self.__initComponents()

    def __command(self):
        time = 2
        moves = 3
        failures = 3
        hits = 5
        time = 2.3
        messagebox.showinfo('Game Summary', f" Time played: {time} \n Moves: {moves} \n Failures: {failures} \n Hits: {hits}")
        self.quit()

class GameOverScreen(tk.Frame):
    """Game Over Screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor 
        self.__initComponents()

    def __initComponents(self): #widget calling
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupButton()
    
    def __setupCanvas(self):
        self.__gameOverCanvas = tk.Canvas(self, width=768, height=384)
        self.__gameOverCanvas.place(x=0, y=0)
    
    def __setupBackground(self):
        global bgOImg
        bgOImg = PhotoImage(file= "media/gameOverScreen.png") 
        bgOImgLabel = tk.Label(self.__gameOverCanvas, image = bgOImg)
        bgOImgLabel.place(x=0, y=0)

    def __setupButton(self):
        tk.Button(self, text="Exit", font=(HELVETICA, 15, 'bold'), width=8, command= self.quit).place(x=340, y=235)

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
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 7 or self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == 4.3

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
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == -1

    def checkLeftBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == -1

    def checkDownBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x + 1][self.__y] == -1

    def checkUpBoatPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == -1
#---------------------------------
    def checkRightBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y + 1] == -1

    def checkLeftBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x][self.__y - 1] == -1

    def checkDownBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == -1

    def checkUpBoatPcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x - 1][self.__y] == -1
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
        return self.__pcapMatrix.getMatrix()[self.__x - 2][self.__y] == 7
    
    def checkLimitDownTwoPcap(self, pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 2][self.__y] == 7

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
        return self.__pcapMatrix.getMatrix()[self.__x - 3][self.__y] == 7
    
    def checkLimitDownThreePcap(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 3][self.__y] == 7

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

    def checkLimitRightTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 2] == 7 
    
    def checkLimitLeftTwoPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 2] == 7 #TODO:

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
    
    def checkBoatUpPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x - 1][self.__y] == -1
    
    def checkBoatDownPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__pcapMatrix.getMatrix()[self.__x + 1][self.__y] == -1

    def checkBoatRightPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y + 1] == -1
    
    def checkBoatLeftPapc(self,pX, pY):
        self.__x = pX
        self.__y = pY
        return self.__papcMatrix.getMatrix()[self.__x][self.__y - 1] == -1
        
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
        return (pOld, oldID), (pNew, newID), 1
    
    def updateAttack(cls, pNew, newID): #Update the logic matriz when the player attack        
        cls.__matrix[pNew[0]][pNew[1]] = newID
        return pNew, newID, 1
    
    def updateBoats(cls, boatsTuple, newID):
        for boat in boatsTuple:
            cls.__matrix[boat[0]][boat[1]] = newID

class Turn(object): # Another singletone to modify and return the "Turn" value
    __instance = None
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = super(Turn, cls).__new__(cls)
            cls.__turn = True
            cls.__destroyedPapc = 0
            cls.__destroyedPcap = 0
            cls.__pcapMatrixMoves = 0
            cls.__moves = 0
            cls.__name = ""
        return cls.__instance

    def getName(cls):
        return cls.__name

    def setName(cls, name):
        cls.__name = name

    def setTurn(cls, state): # turn modification 
        cls.__turn = state

    def getMoves(cls):
        return cls.__moves
    
    def setMoves(cls, moves):
        cls.__moves = moves

    def modifyMoves(cls):
        cls.__moves += 1

    def getTurn(cls): # return the turn value
        return cls.__turn
    
    def setTurn(cls, turn):
        cls.__turn = turn

    def setDestroyedPapc(cls, destroyed):
        cls.__destroyedPapc = destroyed
    
    def setDestroyedPcap(cls, destroyed):
        cls.__destroyedPcap = destroyed

    def getDestroyedPapc(cls):
        return cls.__destroyedPapc
    
    def getDestroyedPcap(cls): 
        return cls.__destroyedPcap
    
    def modifyDestroyedPapc(cls):
        cls.__destroyedPapc += 1

    def modifyDestroyedPcap(cls):
        cls.__destroyedPcap += 1
    
    def getPcapMatrixMoves(cls):
        return cls.__pcapMatrixMoves
    
    def modifyPcapMatrixMoves(cls):
        cls.__pcapMatrixMoves += 1

    def setPcapMatrixMoves(cls, value):
        cls.__pcapMatrixMoves = value
        
class BoatNumber(object): # Another singletone to modify and return the "BoatNumber" value, this is used to place the boats, this class return the "type" of boats.
    __instance = None
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = super(BoatNumber, cls).__new__(cls)
            cls.__boatNumber = 1
            cls.__randomBoatNumber = 1
        return cls.__instance

    def modifyBoatNumber(cls): 
        cls.__boatNumber += 1

    def getBoatNumber(cls): # return the turn value
        return cls.__boatNumber
    
    def modifyRandomBoatNumber(cls):
        cls.__randomBoatNumber += 1

    def getRandomBoatNumber(cls):
        return cls.__randomBoatNumber

class Arrow: 
    def __init__(self):
        self.__x = 10
        self.__y = 1
        self.__countBoatVer = 0
        self.__countBoatHor = 0
        self.__check = ToCheck()
        self.__pcapMatrix = PcAttackPlayerMatrix()
        self.__boatNumber = BoatNumber()
        self.__ID = 9.3
    
    def __setupFxSound(self):
        pygame.mixer.init()
        __constructionFx = pygame.mixer.Sound("sound/constructionSound.mp3")
        __constructionFx.play() 
    
    def getCheckBoats(self, status, checkBoats):
        if status == 1: # vertical
            if checkBoats == 1: #verify vertical up
                return self.__check.checkVerBoatsUp(self.__x, self.__y)  
            if checkBoats == 2: #verify vertical down
                return self.__check.checkVerBoatsDown(self.__x, self.__y)  
            if checkBoats == 3: #verify vertical right
                return self.__check.checkVerBoatsRight(self.__x, self.__y) 
            if checkBoats == 4: #verify vertical left
                return self.__check.checkVerBoatsLeft(self.__x, self.__y) 

        if status == 2: #horizontal
            if checkBoats == 1: #verify horizontal up
                return self.__check.checkHorBoatsUp(self.__x, self.__y)  
            if checkBoats == 2: #verify horizontal down
                return self.__check.checkHorBoatsDown(self.__x, self.__y)  
            if checkBoats == 3: #verify horizontal right
                return self.__check.checkHorBoatsRight(self.__x, self.__y) 
            if checkBoats == 4: #verify horizontal left
                return self.__check.checkHorBoatsLeft(self.__x, self.__y)
    
    def getCheckLimit(self, limit):
        if limit == 1: #LmitUp
            return self.__check.checkLimitUpPcap(self.__x, self.__y)      
        if limit == 2: #LimitDown
            return self.__check.checkLimitDownPcap(self.__x, self.__y) 
        if limit == 3: #LimitRight
            return self.__check.checkLimitRightPcap(self.__x, self.__y)  
        if limit == 4: #LimitLeft
            return self.__check.checkLimitLeftPcap(self.__x, self.__y) 
    
    def doNothing(self):
        return (0, 0, 0)

    def moveUp(self):
        if self.getCheckBoats(1, 1): #vertical
            if self.__countBoatVer == 0:
                self.__oldID = 0
                self.__countBoatVer += 1
            else:
                self.__oldID = 1.1
        elif self.getCheckBoats(2, 1): #horizontal
            if self.__countBoatHor == 0: 
                self.__oldID = 0
                self.__countBoatHor += 1
            else: 
                self.__oldID = 1.2
        else: 
            if self.__countBoatVer != 0: # Si no hay barcos y tenian rastros de barcos, los dejan y vuelven a tomar el valor del cero los counts
                self.__oldID = 1.1
                self.__countBoatVer = 0
            elif self.__countBoatHor != 0: 
                self.__oldID = 1.2
                self.__countBoatHor = 0
            else:
                self.__oldID = 0
        
        oldX = self.__x
        self.__ID = 9.1

        if not self.getCheckLimit(1): #indica si hay limite
            self.__x -= 1
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else: 
            return self.doNothing()

    def moveDown(self):
        if self.getCheckBoats(1, 2): #vertical
            if self.__countBoatVer == 0:
                self.__oldID = 0
                self.__countBoatVer += 1
            else:
                self.__oldID = 1.1
        elif self.getCheckBoats(2, 2): #horizontal
            if self.__countBoatHor == 0: 
                self.__oldID = 0
                self.__countBoatHor += 1
            else: 
                self.__oldID = 1.2
        else: 
            if self.__countBoatVer != 0: # Si no hay barcos y tenian rastros de barcos, los dejan y vuelven a tomar el valor del cero los counts
                self.__oldID = 1.1
                self.__countBoatVer = 0
            elif self.__countBoatHor != 0: 
                self.__oldID = 1.2
                self.__countBoatHor = 0
            else:
                self.__oldID = 0
        
        oldX = self.__x
        self.__ID = 9.2
        
        if not self.getCheckLimit(2): #indica si hay limite
            self.__x += 1
            return self.__pcapMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()
    
    def moveRight(self):
        if self.getCheckBoats(1, 3): #vertical
            if self.__countBoatVer == 0:
                self.__oldID = 0
                self.__countBoatVer += 1
            else:
                self.__oldID = 1.1
        elif self.getCheckBoats(2, 3): #horizontal
            if self.__countBoatHor == 0: 
                self.__oldID = 0
                self.__countBoatHor += 1
            else: 
                self.__oldID = 1.2
        else: 
            if self.__countBoatVer != 0: # Si no hay barcos y tenian rastros de barcos, los dejan y vuelven a tomar el valor del cero los counts
                self.__oldID = 1.1
                self.__countBoatVer = 0
            elif self.__countBoatHor != 0: 
                self.__oldID = 1.2
                self.__countBoatHor = 0
            else:
                self.__oldID = 0
        
        oldY = self.__y
        self.__ID = 9.3
        
        if not self.getCheckLimit(3): #indica si hay limite
            self.__y += 1
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()

    def moveLeft(self):
        if self.getCheckBoats(1, 4): #vertical
            if self.__countBoatVer == 0:
                self.__oldID = 0
                self.__countBoatVer += 1
            else:
                self.__oldID = 1.1
        elif self.getCheckBoats(2, 4): #horizontal
            if self.__countBoatHor == 0: 
                self.__oldID = 0
                self.__countBoatHor += 1
            else: 
                self.__oldID = 1.2
        else: 
            if self.__countBoatVer != 0: # Si no hay barcos y tenian rastros de barcos, los dejan y vuelven a tomar el valor del cero los counts
                self.__oldID = 1.1
                self.__countBoatVer = 0
            elif self.__countBoatHor != 0: 
                self.__oldID = 1.2
                self.__countBoatHor = 0
            else:
                self.__oldID = 0
        
        oldY = self.__y
        self.__ID = 9.4
        
        if not self.getCheckLimit(4): #indica si hay limite
            self.__y -= 1
            return self.__pcapMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else: 
            return self.doNothing()

    def getLimitCondition(self, limit, direction):
        if limit == 1:
            if direction == 1: #ArrowUP
                return self.__check.checkLimitUpPcap(self.__x, self.__y)      
            if direction == 2: #ArrowDown
                return self.__check.checkLimitDownPcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkLimitRightPcap(self.__x, self.__y) 
            if direction == 4: #ArrowLeft
                return self.__check.checkLimitLeftPcap(self.__x, self.__y) 
        
        if limit == 2:
            if direction == 1: #ArrowUP
                return self.__check.checkLimitUpTwoPcap(self.__x, self.__y)      
            if direction == 2: #ArrowDown
                return self.__check.checkLimitDownTwoPcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkLimitRightTwoPcap(self.__x, self.__y) 
            if direction == 4: #ArrowLeft
                return self.__check.checkLimitLeftTwoPcap(self.__x, self.__y)
        
        if limit == 3:
            if direction == 1: #ArrowUP
                return self.__check.checkLimitUpThreePcap(self.__x, self.__y)      
            if direction == 2: #ArrowDown
                return self.__check.checkLimitDownThreePcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkLimitRightThreePcap(self.__x, self.__y) 
            if direction == 4: #ArrowLeft
                return self.__check.checkLimitLeftThreePcap(self.__x, self.__y) 


    def getBoatCondition(self, boat, direction):
        if boat == 1:
            if direction == 1: # ArrowUP
                return self.__check.checkBoatUpPcap(self.__x, self.__y)     
            if direction == 2: #ArrowDown
                return self.__check.checkBoatDownPcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkBoatRightPcap(self.__x, self.__y)
            if direction == 4: #ArrowLeft
                return self.__check.checkBoatLeftPcap(self.__x, self.__y) 
        
        if boat == 2:
            if direction == 1: # ArrowUP
                return self.__check.checkBoatUpTwoPcap(self.__x, self.__y)      
            if direction == 2: #ArrowDown
                return self.__check.checkBoatDownTwoPcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkBoatRightTwoPcap(self.__x, self.__y) 
            if direction == 4: #ArrowLeft
                return self.__check.checkBoatLeftTwoPcap(self.__x, self.__y)
        
        if boat == 3:
            if direction == 1: # ArrowUP
                return self.__check.checkBoatUpThreePcap(self.__x, self.__y)      
            if direction == 2: #ArrowDown
                return self.__check.checkBoatDownThreePcap(self.__x, self.__y)  
            if direction == 3: #ArrowRight
                return self.__check.checkBoatRightThreePcap(self.__x, self.__y) 
            if direction == 4: #ArrowLeft
                return self.__check.checkBoatLeftThreePcap(self.__x, self.__y) 

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
                if not self.getLimitCondition(1, 1):
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                
            if self.__actualBoat == 2:
                if not self.getLimitCondition(1, 1):
                    if not self.getBoatCondition(1, 1):
                        if not self.getLimitCondition(2, 1):
                            if not self.getBoatCondition(2, 1):
                                self.__setupFxSound() 
                                self.__boatNumber.modifyBoatNumber()
                                return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y), (self.__x - 2, self.__y)], self.__image, 1)
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                if not self.getLimitCondition(1, 1):
                    if not self.getBoatCondition(1, 1):
                        if not self.getLimitCondition(2, 1):
                            if not self.getBoatCondition(2, 1):
                                if not self.getLimitCondition(3, 1):
                                    if not self.getBoatCondition(3, 1):
                                        self.__setupFxSound() 
                                        self.__boatNumber.modifyBoatNumber()
                                        return self.__pcapMatrix.updateBoat([(self.__x - 1, self.__y), (self.__x - 2, self.__y), (self.__x - 3, self.__y)], self.__image, 1)
                                    else:
                                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                        return self.__doNothing
                                else:
                                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                                    return self.__doNothing
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                
        if self.__ID == 9.2: # arrowDown
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                if not self.getLimitCondition(1, 2):
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                if not self.getLimitCondition(1, 2):
                    if not self.getBoatCondition(1, 2):
                        if not self.getLimitCondition(2, 2):
                            if not self.getBoatCondition(2,2):
                                self.__setupFxSound() 
                                self.__boatNumber.modifyBoatNumber()
                                return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y), (self.__x + 2, self.__y)], self.__image, 1)
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                if not self.getLimitCondition(1, 2):
                    if not self.getBoatCondition(1, 2):
                        if not self.getLimitCondition(2, 2):
                            if not self.getBoatCondition(2, 2):
                                if not self.getLimitCondition(3, 2):
                                    if not self.getBoatCondition(3, 2):
                                        self.__setupFxSound() 
                                        self.__boatNumber.modifyBoatNumber()
                                        return self.__pcapMatrix.updateBoat([(self.__x + 1, self.__y), (self.__x + 2, self.__y), (self.__x + 3, self.__y)], self.__image, 1)
                                    else:
                                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                        return self.__doNothing
                                else:
                                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                                    return self.__doNothing
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
        
        if self.__ID == 9.3: #arrowRight
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                if not self.getLimitCondition(1, 3):
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing

            if self.__actualBoat == 2:
                if not self.getLimitCondition(1, 3):
                    if not self.getBoatCondition(1, 3):
                        if not self.getLimitCondition(2, 3):
                            if not self.getBoatCondition(2, 3):
                                self.__setupFxSound() 
                                self.__boatNumber.modifyBoatNumber()
                                return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1), (self.__x, self.__y + 2)], self.__image, 1)
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            
            if self.__actualBoat == 3:
                if not self.getLimitCondition(1, 3):
                    if not self.getBoatCondition(1, 3):
                        if not self.getLimitCondition(2, 3):
                            if not self.getBoatCondition(2, 3):
                                if not self.getLimitCondition(3, 3):
                                    if not self.getBoatCondition(3, 3):
                                        self.__setupFxSound() 
                                        self.__boatNumber.modifyBoatNumber()
                                        return self.__pcapMatrix.updateBoat([(self.__x, self.__y + 1), (self.__x, self.__y + 2), (self.__x, self.__y + 3)], self.__image, 1)
                                    else:
                                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                        return self.__doNothing
                                else:
                                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                                    return self.__doNothing
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                
        if self.__ID == 9.4: #arrowLeft
            if self.__actualBoat == 4:
                messagebox.showinfo('Error', 'Limit of boats reached. Please press Next')
                return self.__doNothing

            if self.__actualBoat == 1:
                if not self.getLimitCondition(1, 4):
                    self.__setupFxSound()
                    self.__boatNumber.modifyBoatNumber()
                    return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1)], self.__image, 1) 
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
                    
            if self.__actualBoat == 2:
                if not self.getLimitCondition(1, 4):
                    if not self.getBoatCondition(1, 4):
                        if not self.getLimitCondition(2, 4):
                            if not self.getBoatCondition(2, 4):
                                self.__setupFxSound() 
                                self.__boatNumber.modifyBoatNumber()
                                return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1), (self.__x, self.__y - 2)], self.__image, 1)
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
            if self.__actualBoat == 3:
                if not self.getLimitCondition(1, 4):
                    if not self.getBoatCondition(1, 4):
                        if not self.getLimitCondition(2, 4):
                            if not self.getBoatCondition(2, 4):
                                if not self.getLimitCondition(3, 4):
                                    if not self.getBoatCondition(3, 4):
                                        self.__setupFxSound() 
                                        self.__boatNumber.modifyBoatNumber()
                                        return self.__pcapMatrix.updateBoat([(self.__x, self.__y - 1), (self.__x, self.__y - 2), (self.__x, self.__y - 3)], self.__image, 1)
                                    else:
                                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                        return self.__doNothing
                                else:
                                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                                    return self.__doNothing
                            else:
                                messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                                return self.__doNothing
                        else:
                            messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                            return self.__doNothing
                    else:
                        messagebox.showinfo('Error', 'Boat reached. Choose another position to place your boat.')
                        return self.__doNothing            
                else:
                    messagebox.showinfo('Error', 'Limit reached. Choose another position to place your boat.')
                    return self.__doNothing
            
class AtkPlane:
    def __init__(self): #class constructor
        self.__x = 6
        self.__y = 0
        self.__moves = 0
        self.__countMissed = 0
        self.__countDebris = 0
        self.__countEnemyBoat = 0
        self.__check = ToCheck()
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__turn = Turn()
        self.__ID = 4.3
    
    def getMoves(self):
        return self.__moves
    
    def setMoves(self, moves):
        self.__moves = moves

    def setupFxSound(self, fxID):
        if fxID == 1:
            __explotionFx = pygame.mixer.Sound("sound/explotionSound.mp3")
            __explotionFx.play() 
        else:
            __missFx = pygame.mixer.Sound("sound/missSound.mp3")
            __missFx.play() 

    def getCheckDebris(self, debris):
        if debris == 1: #DebrisUp
            return self.__check.checkUpDebris(self.__x, self.__y)
        if debris == 2: #DebrisDown
            return self.__check.checkDownDebris(self.__x, self.__y)
        if debris == 3: #DebrisRight
            return self.__check.checkRightDebris(self.__x, self.__y) 
        if debris == 4: #DebrisLeft
            return self.__check.checkLeftDebris(self.__x, self.__y)

    def getCheckMissed(self, missed):
        if missed == 1: #MissedUp
            return self.__check.checkUpMissed(self.__x, self.__y)     
        if missed == 2: #MissedDown
            return self.__check.checkDownMissed(self.__x, self.__y)
        if missed == 3: #MissedRight
            return self.__check.checkRightMissed(self.__x, self.__y) 
        if missed == 4: #MissedLeft
            return self.__check.checkLeftMissed(self.__x, self.__y)

    def getCheckLimit(self, limit):
        if limit == 1: #LmitUp
            return self.__check.checkLimitUpPapc(self.__x, self.__y)      
        if limit == 2: #LimitDown
            return self.__check.checkLimitDownPapc(self.__x, self.__y) 
        if limit == 3: #LimitRight
            return self.__check.checkLimitRightPapc(self.__x, self.__y)  
        if limit == 4: #LimitLeft
            return self.__check.checkLimitLeftPapc(self.__x, self.__y) 

    def getCheckEnemyBoat(self, enemyBoat):
        if enemyBoat == 1: #EnemyBoatUp
            return self.__check.checkBoatUpPapc(self.__x, self.__y)
        if enemyBoat == 2: #EnemyBoatDown
            return self.__check.checkBoatDownPapc(self.__x, self.__y) 
        if enemyBoat == 3: #EnemyBoatRight
            return self.__check.checkBoatRightPapc(self.__x, self.__y)  
        if enemyBoat == 4: #EnemyBoatLeft
            return self.__check.checkBoatLeftPapc(self.__x, self.__y) 
    
    def doNothing(self):
        return (0, 0, 0)

    def moveUp(self):
        if self.getCheckDebris(1):
            if self.__countDebris == 0: 
                self.__oldID = 0
                self.__countDebris += 1
            else:
                self.__oldID = 3
        elif self.getCheckMissed(1):
            if self.__countMissed == 0: 
                self.__oldID = 0
                self.__countMissed += 1
            else: 
                self.__oldID = 5
        elif self.getCheckEnemyBoat(1):
            if self.__countEnemyBoat == 0:
                self.__oldID = 0
                self.__countEnemyBoat += 1
            else: 
                self.__oldID = -1 # Modificar por agua
        else: 
            if self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0
            elif self.__countMissed != 0: 
                self.__oldID = 5
                self.__countMissed = 0
            elif self.__countEnemyBoat != 0: 
                self.__oldID = -1
                self.__countEnemyBoat = 0
            else: 
                self.__oldID = 0

        oldX = self.__x
        self.__ID = 4.1

        if not self.getCheckLimit(1):
            self.__x -= 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()

    def moveDown(self):
        if self.getCheckDebris(2):
            if self.__countDebris == 0: 
                self.__oldID = 0
                self.__countDebris += 1
            else:
                self.__oldID = 3
        elif self.getCheckMissed(2):
            if self.__countMissed == 0: 
                self.__oldID = 0
                self.__countMissed += 1
            else: 
                self.__oldID = 5
        elif self.getCheckEnemyBoat(2):
            if self.__countEnemyBoat == 0:
                self.__oldID = 0
                self.__countEnemyBoat += 1
            else: 
                self.__oldID = -1
        else: 
            if self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0
            elif self.__countMissed != 0: 
                self.__oldID = 5
                self.__countMissed = 0
            elif self.__countEnemyBoat != 0: 
                self.__oldID = -1
                self.__countEnemyBoat = 0
            else: 
                self.__oldID = 0

        oldX = self.__x
        self.__ID = 4.2

        if not self.getCheckLimit(2):
            self.__x += 1
            return self.__papcMatrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()

    def moveRight(self):
        if self.getCheckLimit(1) and self.getCheckLimit(2) and self.getCheckEnemyBoat(2): 
            self.__oldID = 7
            self.__countEnemyBoat += 1
        elif self.getCheckLimit(1) and self.getCheckLimit(2): 
            self.__oldID = 7
        elif self.getCheckDebris(3):
            if self.__countDebris == 0: 
                self.__oldID = 0
                self.__countDebris += 1
            else:
                self.__oldID = 3
        elif self.getCheckMissed(3):
            if self.__countMissed == 0: 
                self.__oldID = 0
                self.__countMissed += 1
            else: 
                self.__oldID = 5
        elif self.getCheckEnemyBoat(3):
            if self.__countEnemyBoat == 0:
                self.__oldID = 0
                self.__countEnemyBoat += 1
            else: 
                self.__oldID = -1 # Modificar por agua
        else: 
            if self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0
            elif self.__countMissed != 0: 
                self.__oldID = 5
                self.__countMissed = 0
            elif self.__countEnemyBoat != 0: 
                self.__oldID = -1
                self.__countEnemyBoat = 0
            else: 
                self.__oldID = 0

        oldY = self.__y
        self.__ID = 4.3

        if not self.getCheckLimit(3):
            self.__y += 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()

    def moveLeft(self):
        if self.getCheckDebris(4):
            if self.__countDebris == 0: 
                self.__oldID = 0
                self.__countDebris += 1
            else:
                self.__oldID = 3
        elif self.getCheckMissed(4):
            if self.__countMissed == 0: 
                self.__oldID = 0
                self.__countMissed += 1
            else: 
                self.__oldID = 5
        elif self.getCheckEnemyBoat(4):
            if self.__countEnemyBoat == 0:
                self.__oldID = 0
                self.__countEnemyBoat += 1
            else: 
                self.__oldID = -1 # Modificar por agua
        else: 
            if self.__countDebris != 0: 
                self.__oldID = 3
                self.__countDebris = 0
            elif self.__countMissed != 0: 
                self.__oldID = 5
                self.__countMissed = 0
            elif self.__countEnemyBoat != 0: 
                self.__oldID = -1
                self.__countEnemyBoat = 0
            else: 
                self.__oldID = 0

        oldY = self.__y
        self.__ID = 4.4

        if not self.getCheckLimit(4):
            self.__y -= 1
            return self.__papcMatrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldID, self.__ID)
        else:
            return self.doNothing()

    def attack(self):
        if not self.__check.checkLimitUpPapc(self.__x, self.__y):
            if self.__ID == 4.1: #Player looks up
                if self.__check.checkUpBoatPapc(self.__x, self.__y):  
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(True)
                    newX = self.__x - 1
                    self.__ID = 3
                    self.__turn.modifyDestroyedPapc()
                    self.setupFxSound(1)
                    return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
                elif self.getCheckMissed(1) or self.getCheckDebris(1):
                    return (0, 0, 0)
                else:
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(False)
                    newX = self.__x - 1
                    self.__ID = 5
                    self.setupFxSound(0)
                    return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
        else: 
            return (0, 0, 0)

        if not self.__check.checkLimitDownPapc(self.__x, self.__y):
            if self.__ID == 4.2: #Player looks down
                if self.__check.checkDownBoatPapc(self.__x, self.__y): 
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(True)
                    newX = self.__x + 1
                    self.__ID = 3
                    self.__turn.modifyDestroyedPapc()
                    self.setupFxSound(1)
                    return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
                elif self.getCheckMissed(2) or self.getCheckDebris(2):
                    return (0, 0, 0)
                else:
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(False)
                    newX = self.__x + 1
                    self.__ID = 5
                    self.setupFxSound(0)
                    return self.__papcMatrix.updateAttack((newX, self.__y), self.__ID)
        else: 
            return (0, 0, 0)

        if not self.__check.checkLimitRightPapc(self.__x, self.__y):
            if self.__ID == 4.3: #player looks right
                if self.__check.checkRightBoatPapc(self.__x, self.__y): #Player looks up
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(True)
                    newY = self.__y + 1
                    self.__ID = 3
                    self.__turn.modifyDestroyedPapc()
                    self.setupFxSound(1)
                    return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
                elif self.getCheckMissed(3) or self.getCheckDebris(3):
                    return (0, 0, 0)
                else:
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(False)
                    newY = self.__y + 1
                    self.__ID = 5
                    self.setupFxSound(0)
                    return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
        else: 
            return (0, 0, 0)
        
        if not self.__check.checkLimitLeftPapc(self.__x, self.__y):
            if self.__ID == 4.4: # player looks left
                if self.__check.checkLeftBoatPapc(self.__x, self.__y): #Player looks up
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(True)
                    newY = self.__y - 1
                    self.__ID = 3
                    self.setupFxSound(1)
                    self.__turn.modifyDestroyedPapc()
                    return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
                elif self.getCheckMissed(4) or self.getCheckDebris(4):
                    return (0, 0, 0)
                else:
                    self.__moves += 1
                    self.__turn.modifyMoves()
                    self.__turn.setTurn(False)
                    newY = self.__y - 1
                    self.__ID = 5
                    self.setupFxSound(0)
                    return self.__papcMatrix.updateAttack((self.__x, newY), self.__ID)
        else: 
            return (0, 0, 0)


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
        return (pOld, oldID), (pNew, newID), 1
    
    def updateAttack(cls, pNew, newID): #Update the logic matriz when the player attack
        cls.__matrix[pNew[0]][pNew[1]] = newID
        cls.__result = [pNew, newID]
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
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__randomBoatNumber = BoatNumber()
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
        self.__x = random.randint(1, 10)
        self.__y = random.randint(1, 10)
        self.__randomCoord = [self.__x, self.__y]
        return self.__randomCoord
    
    def generateOrientation(self):
        self.__orientation = random.randint(1, 4)
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
                self.__turn.modifyDestroyedPcap()
                self.setupFxSound(1)
                self.__ID = 3
            else:
                self.setupFxSound(2)
                self.__ID = 5 
            self.__turn.modifyPcapMatrixMoves()
            self.addHistory(self.__coords)
            self.__turn.setTurn(True)
            return self.__pcapMatrix.updateAttack(self.__coords, self.__ID)
        else:
            return self.attack()

    def getPlaceCoordRandom(self):
        self.__coords = self.generateCoords()
        return self.__coords
    
    def getOrientationValue(self):
        self.__orient = self.generateOrientation()
        return self.__orient
        
    def getLimitCondition(self, limit, direction):
        if limit == 1:
            if direction == 1: #Up
                return self.__check.checkLimitUpPapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkLimitDownPapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkLimitRightPapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkLimitLeftPapc(self.__coords[0], self.__coords[1])
        if limit == 2:
            if direction == 1: #Up
                return self.__check.checkLimitUpTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkLimitDownTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkLimitRightTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkLimitLeftTwoPapc(self.__coords[0], self.__coords[1])
        if limit == 3:
            if direction == 1: #Up
                return self.__check.checkLimitUpThreePapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkLimitDownThreePapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkLimitRightThreePapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkLimitLeftThreePapc(self.__coords[0], self.__coords[1])
    
    def getBoatCondition(self, boat, direction): 
        if boat == 1:
            if direction == 1: #Up
                return self.__check.checkBoatUpPapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkBoatDownPapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkBoatRightPapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkBoatLeftPapc(self.__coords[0], self.__coords[1])
        if boat == 2:
            if direction == 1: #Up
                return self.__check.checkBoatUpTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkBoatDownTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkBoatRightTwoPapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkBoatLeftTwoPapc(self.__coords[0], self.__coords[1])
        if boat == 3:
            if direction == 1: #Up
                return self.__check.checkBoatUpThreePapc(self.__coords[0], self.__coords[1])
            if direction == 2: #Down
                return self.__check.checkBoatDownThreePapc(self.__coords[0], self.__coords[1])
            if direction == 3: #Right
                return self.__check.checkBoatRightThreePapc(self.__coords[0], self.__coords[1])
            if direction == 4: #Left
                return self.__check.checkBoatLeftThreePapc(self.__coords[0], self.__coords[1])
                
    def placeBoats(self):       
        self.__coords = self.getPlaceCoordRandom()
        self.__orientation = self.getOrientationValue()

        self.__ID = -1
        
        if self.__orientation == 1: #Up
            if not self.__check.checkPlaceCoordsDisp(self.__coords, self.__placeHistory):
                if self.__randomBoatNumber.getRandomBoatNumber() == 1:# Boat #1
                    if not self.getLimitCondition(1,1):
                        self.__randomBoatNumber.modifyRandomBoatNumber()
                        self.addPlaceHistory(self.__coords)
                        coord1 = self.__coords[0] - 1, self.__coords[1]
                        return self.__papcMatrix.updateBoats([coord1], self.__ID)
                    else:
                        return self.placeBoats()
                        
                if self.__randomBoatNumber.getRandomBoatNumber() == 2:# Boat #2
                    if not self.getLimitCondition(1,1):
                        if not self.getBoatCondition(1,1):
                            if not self.getLimitCondition(2,1):
                                if not self.getBoatCondition(2,1):
                                    self.__randomBoatNumber.modifyRandomBoatNumber()
                                    self.addPlaceHistory(self.__coords)
                                    coord1 = self.__coords[0] - 1, self.__coords[1]
                                    coord2 = self.__coords[0] - 2, self.__coords[1]
                                    return self.__papcMatrix.updateBoats([coord1, coord2], self.__ID)
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()

                if self.__randomBoatNumber.getRandomBoatNumber() == 3: # Boat #3
                    if not self.getLimitCondition(1,1):
                        if not self.getBoatCondition(1,1):
                            if not self.getLimitCondition(2,1):
                                if not self.getBoatCondition(2,1):
                                    if not self.getLimitCondition(3,1):
                                        if not self.getBoatCondition(3,1):
                                            self.__randomBoatNumber.modifyRandomBoatNumber()
                                            self.addPlaceHistory(self.__coords)
                                            coord1 = self.__coords[0] - 1, self.__coords[1]
                                            coord2 = self.__coords[0] - 2, self.__coords[1]
                                            coord3 = self.__coords[0] - 3, self.__coords[1]
                                            return self.__papcMatrix.updateBoats([coord1, coord2, coord3], self.__ID)
                                        else:
                                            return self.placeBoats()
                                    else:
                                        return self.placeBoats()
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()
            else:
                return self.placeBoats()

        if self.__orientation == 2: #Down
            if not self.__check.checkPlaceCoordsDisp(self.__coords, self.__placeHistory):
                if self.__randomBoatNumber.getRandomBoatNumber() == 1:# Boat #1
                    if not self.getLimitCondition(1,2):
                        self.__randomBoatNumber.modifyRandomBoatNumber()
                        self.addPlaceHistory(self.__coords)
                        coord1 = self.__coords[0] + 1, self.__coords[1]
                        return self.__papcMatrix.updateBoats([coord1], self.__ID)
                    else:
                        return self.placeBoats()
                        
                if self.__randomBoatNumber.getRandomBoatNumber() == 2:# Boat #2
                    if not self.getLimitCondition(1,2):
                        if not self.getBoatCondition(1,2):
                            if not self.getLimitCondition(2,2):
                                if not self.getBoatCondition(2,2):
                                    self.__randomBoatNumber.modifyRandomBoatNumber()
                                    self.addPlaceHistory(self.__coords)
                                    coord1 = self.__coords[0] + 1, self.__coords[1]
                                    coord2 = self.__coords[0] + 2, self.__coords[1]
                                    return self.__papcMatrix.updateBoats([coord1, coord2], self.__ID)
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()

                if self.__randomBoatNumber.getRandomBoatNumber() == 3: # Boat #3
                    if not self.getLimitCondition(1,2):
                        if not self.getBoatCondition(1,2):
                            if not self.getLimitCondition(2,2):
                                if not self.getBoatCondition(2,2):
                                    if not self.getLimitCondition(3,2):
                                        if not self.getBoatCondition(3,2):
                                            self.__randomBoatNumber.modifyRandomBoatNumber()
                                            self.addPlaceHistory(self.__coords)
                                            coord1 = self.__coords[0] + 1, self.__coords[1]
                                            coord2 = self.__coords[0] + 2, self.__coords[1]
                                            coord3 = self.__coords[0] + 3, self.__coords[1]
                                            return self.__papcMatrix.updateBoats([coord1, coord2, coord3], self.__ID)
                                        else:
                                            return self.placeBoats()
                                    else:
                                        return self.placeBoats()
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()
            else:
                return self.placeBoats()

        if self.__orientation == 3: #Right
            if not self.__check.checkPlaceCoordsDisp(self.__coords, self.__placeHistory):
                if self.__randomBoatNumber.getRandomBoatNumber() == 1:# Boat #1
                    if not self.getLimitCondition(1,3):
                        self.__randomBoatNumber.modifyRandomBoatNumber()
                        self.addPlaceHistory(self.__coords)
                        coord1 = self.__coords[0], self.__coords[1] + 1
                        return self.__papcMatrix.updateBoats([coord1], self.__ID)
                    else:
                        return self.placeBoats()
                        
                if self.__randomBoatNumber.getRandomBoatNumber() == 2:# Boat #2
                    if not self.getLimitCondition(1,3):
                        if not self.getBoatCondition(1,3):
                            if not self.getLimitCondition(2,3):
                                if not self.getBoatCondition(2,3):
                                    self.__randomBoatNumber.modifyRandomBoatNumber()
                                    self.addPlaceHistory(self.__coords)
                                    coord1 = self.__coords[0], self.__coords[1] + 1
                                    coord2 = self.__coords[0], self.__coords[1] + 2
                                    return self.__papcMatrix.updateBoats([coord1, coord2], self.__ID)
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()

                if self.__randomBoatNumber.getRandomBoatNumber() == 3: # Boat #3
                    if not self.getLimitCondition(1,3):
                        if not self.getBoatCondition(1,3):
                            if not self.getLimitCondition(2,3):
                                if not self.getBoatCondition(2,3):
                                    if not self.getLimitCondition(3,3):
                                        if not self.getBoatCondition(3,3):
                                            self.__randomBoatNumber.modifyRandomBoatNumber()
                                            self.addPlaceHistory(self.__coords)
                                            coord1 = self.__coords[0], self.__coords[1] + 1
                                            coord2 = self.__coords[0], self.__coords[1] + 2
                                            coord3 = self.__coords[0], self.__coords[1] + 3
                                            return self.__papcMatrix.updateBoats([coord1, coord2, coord3], self.__ID)
                                        else:
                                            return self.placeBoats()
                                    else:
                                        return self.placeBoats()
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()
            else:
                return self.placeBoats()

        if self.__orientation == 4: #Left
            if not self.__check.checkPlaceCoordsDisp(self.__coords, self.__placeHistory):
                if self.__randomBoatNumber.getRandomBoatNumber() == 1:# Boat #1
                    if not self.getLimitCondition(1,4):
                        self.__randomBoatNumber.modifyRandomBoatNumber()
                        self.addPlaceHistory(self.__coords)
                        coord1 = self.__coords[0], self.__coords[1] - 1
                        return self.__papcMatrix.updateBoats([coord1], self.__ID)
                    else:
                        return self.placeBoats()
                        
                if self.__randomBoatNumber.getRandomBoatNumber() == 2:# Boat #2
                    if not self.getLimitCondition(1,4):
                        if not self.getBoatCondition(1,4):
                            if not self.getLimitCondition(2,4):
                                if not self.getBoatCondition(2,4):
                                    self.__randomBoatNumber.modifyRandomBoatNumber()
                                    self.addPlaceHistory(self.__coords)
                                    coord1 = self.__coords[0], self.__coords[1] - 1
                                    coord2 = self.__coords[0], self.__coords[1] - 2
                                    return self.__papcMatrix.updateBoats([coord1, coord2], self.__ID)
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()

                if self.__randomBoatNumber.getRandomBoatNumber() == 3: # Boat #3
                    if  not self.getLimitCondition(1,4):
                        if  not self.getBoatCondition(1,4):
                            if  not self.getLimitCondition(2,4):
                                if  not self.getBoatCondition(2,4):
                                    if  not self.getLimitCondition(3,4):
                                        if not self.getBoatCondition(3,4):
                                            self.__randomBoatNumber.modifyRandomBoatNumber()
                                            self.addPlaceHistory(self.__coords)
                                            coord1 = self.__coords[0], self.__coords[1] - 1
                                            coord2 = self.__coords[0], self.__coords[1] - 2
                                            coord3 = self.__coords[0], self.__coords[1] - 3
                                            return self.__papcMatrix.updateBoats([coord1, coord2, coord3], self.__ID)
                                        else:
                                            return self.placeBoats()
                                    else:
                                        return self.placeBoats()
                                else:
                                    return self.placeBoats()
                            else:
                                return self.placeBoats()
                        else:
                            return self.placeBoats()
                    else:
                        return self.placeBoats()
            else:
                return self.placeBoats()
                
class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__papcMatrix = PlayerAttackPcMatrix()
        self.__atkPlane = AtkPlane()
        self.__check = ToCheck()
        self.__turn = Turn()
        self.__pcapMatrix = PcAttackPlayerMatrix() 
        self.__computerAttack = Computer()
        self.__arrow = Arrow()
        self.__boatNumber = BoatNumber()

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
    
    def getBoatNumber(self):
        return self.__boatNumber