"""
-------------------------------
IMPORTS
-------------------------------
"""
import tkinter as tk

from Engine.GUI import gui_widgets as widgets
from Engine import gui_pages as pages

"""
-------------------------------
VARIABLES AND DEFINITIONS
-------------------------------
"""
# width and height of gui window
WIDTH = 600
HEIGHT = 400

"""
-------------------------------
FUNCTIONS
-------------------------------
"""

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, default="Engine/GUI/icon.bmp")

        #frame of window
        container = tk.Frame(self)
        container.pack(side="top")
        
        #centralize container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #dictionary of frames
        self.frames = {}
        
        for F in (pages.StartupPage, pages.SigninPage, pages.MainMenuPage, pages.PlayBotPage, pages.PlayRandomPage,
                  pages.ChallengePage):
            
            #create startup page frame and update frame dictionary
            frame = F(container, self)
            self.frames[F] = frame
            
            #grid the frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    
        #show startup page frame
        self.show_frame(pages.StartupPage)
        
    """
    show desired frame, 'page'
    params: page
    """    
    def show_frame(self, page, user=""):
        frame = self.frames[page]
        
        #checks for username input
        if user != "":
            #main menu frame functions
            frame.welcomeHeader(user)
            frame.menuButtons(self)
            
        frame.tkraise()
    

"""
-------------------------------
MAIN
-------------------------------
"""
def main():
    
    #GUI window
    mainWindow = MainApp()
    mainWindow.title("MagiChess")
    mainWindow.geometry(f"{WIDTH}x{HEIGHT}")   #main window dimensions

    # map closing 'window closing' event to quit_program function
    mainWindow.protocol("WM_DELETE_WINDOW", pages.quit_program)

    # program will terminate and close GUI if no loop (terminal only)
    mainWindow.mainloop()


if __name__ == '__main__':
    main();


