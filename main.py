import tkinter as tk
from tkinter import PhotoImage, GROOVE
import pygame

class GraphicUserInterface(tk.Tk):
    """Creating the main window"""
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)# constructor 
         
        self.__configureWindow() 
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

    def __configureWindow(self):
        """ Main window configuration """

        self.title("BATTLESHIP")
        self.geometry("800x600+300+60")
        self.iconbitmap('media/icon.ico') #TODO: Revisar compatibilidad con mac
        self.resizable(False, False)
        
class MainMenu(tk.Frame):
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor
        self.__initComponents()
    
    def __initComponents(self,):
        """Widget calling"""
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupMusic()
        self.__setupEntry()
        self.__setupButton()

    def __setupButton(self):
        playButton = tk.Button(self, text="Play", command= lambda : controller.show_frame(GameScreen))
        playButton.place(x=10, y=10)
    
    def __setupCanvas(self):
        """Canvas configuration"""
        self.__menuCanva = tk.Canvas(self, width= 800, height= 600, borderwidth=0)
        self.__menuCanva.place(x=0, y=0)


    def __setupBackground(self):
        """Background configuration"""

        global bgImg #Global variable to show the image

        bgImg = PhotoImage(file= "media/menu.png")
        bgLabel = tk.Label(self.__menuCanva, image = bgImg)
        bgLabel.place(x=0, y=0)

    def __setupMusic(self):
        """Music setup"""

        #Starting pygame
        pygame.mixer.init()

        #Import Soundtrack
        pygame.mixer.music.load("sound/menuTrack.mp3")
        pygame.mixer.music.play(loops=-1) #Play the song while the user is in MainMenu

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

    def __setupCanvas(self):
        """Canvas configuration"""

        self.__boatsCanvas = tk.Canvas(self, width=372, height=372,bg="Green")
        self.__boatsCanvas.place(x=0, y=0)

        self.__gameCanvas = tk.Canvas(self, width=372, height=372, bg="Pink") 
        self.__gameCanvas.place(x=373, y=0)
