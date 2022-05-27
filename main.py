import tkinter as tk
from tkinter import PhotoImage
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
        self.geometry("800x600+198+100")
        self.iconbitmap('media/icon.ico') 
        self.resizable(False, False)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent) #constructor
        self.__initComponents()
    
    def __initComponents(self):
        """Widget calling"""
        self.__setupCanvas()
        self.__setupBackground()
        self.__setupLabel()
        self.__setupButtons()
        self.__setupMusic()
    
    def __setupCanvas(self):
        """Canvas configuration"""
        self.__menuCanva = tk.Canvas(self, width= 1024, height= 500, borderwidth=0)

    def __setupBackground(self):
        """Background configuration"""

        #Using global variables to show the images
        global bgImg

        #Background Image configuration
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
    
    def __setupLabel(self):
        """Tittle label setup"""
        tittleLabel = tk.Label(self.__menuCanva, text="BATTLESHIP", font=("Arial Black", 55), anchor="center", bg="White")
        tittleLabel.place(x=100, y=80)
    
    def __setupButtons(self):
        """Buttons setup"""

class GameScreen(tk.Frame):
    """creating the animation & fibonacci screen"""
    def __init__(self, parent, controller): #constructor
        tk.Frame.__init__(self, parent)#constructor 
        #self.__initComponents()