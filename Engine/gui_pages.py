"""
-------------------------------
IMPORTS
-------------------------------
"""
import signal, json, time
import tkinter as tk
import multiprocessing as mp

from Engine import chessboard
from Engine import gameState

from Engine.GUI import gui_widgets as widgets
from Engine.lichess import lichessInterface_new as interface


"""
-------------------------------
VARIABLES
-------------------------------
"""
eventQueue = mp.Queue()
gameQueue = mp.Queue()

eventstream = None
gamestream = None

terminated = False


"""
-------------------------------
PAGE CLASSES
-------------------------------
"""

class StartupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="MagiChess", font="times", fontsize=25, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #startup buttons
        signinButton = widgets.createButton(self, function=lambda: controller.show_frame(SigninPage),
                                           text="Sign in to LiChess.org", bgcolor="sky blue")
        signinButton.pack(pady=10)
        
        exitButton = widgets.createButton(self, function=quit_program,
                                          text="Exit", bgcolor="seashell3")    
        exitButton.pack()




class SigninPage(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		header = widgets.createLabel(self, text="Sign in to LiChess", font="times", fontsize=14, fontweight="bold")
		header.pack(padx=10, pady=10)

		""" username/password entries
		usernameLabel = widgets.createLabel(self, text="Username", font="times", fontsize=11, fontweight="normal")
		usernameLabel.pack()
		usernameEntry = widgets.createEntry(self, bgcolor="beige")
		usernameEntry.pack()

		passwordLabel = widgets.createLabel(self, text="Password", font="times", fontsize=11, fontweight="normal")
		passwordLabel.pack()
		passwordEntry = widgets.createEntry(self, bgcolor="beige", show="*")
		passwordEntry.pack()
		"""


		""" buttons """
		loginButton = widgets.createButton(self, function=lambda: self.submit(controller=controller, username="degugj"),
		text="Login as degugj", bgcolor="seashell3")
		loginButton.pack(pady=4)

		returnButton = widgets.createButton(self, function=lambda: controller.show_frame(StartupPage),
		text="Return", bgcolor="seashell3")
		returnButton.pack(pady=7)

	""" submit username/password for validation """
	def submit(self, controller, username, password=None):
		valid = 1

		# login as degugj
		if valid:
			controller.show_frame(MainMenuPage, user=username)

			# create and start an event stream process
			global eventstream
			eventstream = mp.Process(target = event_stream, args = (eventQueue,))
			eventstream.start()

		else:
			print("User not found. Invalid username/password")
		return




class MainMenuPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
    def welcomeHeader(self, username):
        header = widgets.createLabel(self, text="Welcome to MagiChess, " + username, font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
    def menuButtons(self, controller):
        """ main menu options """
        playbotButton = widgets.createButton(self, function=lambda: controller.show_frame(PlayBotPage),
                                             text="Play Bot", bgcolor="sky blue")
        playbotButton.pack(pady=5)
        
        playrandButton = widgets.createButton(self, function=lambda: controller.show_frame(PlayRandomPage),
                                             text="Seek an Opponent", bgcolor="sky blue")
        playrandButton.pack(pady=5)
        
        playfriendButton = widgets.createButton(self, function=lambda: controller.show_frame(ChallengePage),
                                             text="Challenge a Friend", bgcolor="sky blue")
        playfriendButton.pack(pady=5)
        
        exitButton = widgets.createButton(self, function=quit_program,
                                             text="Exit MagiChess", bgcolor="seashell3")
        exitButton.pack(pady=5)
        
     


""" main menu pages """
class PlayBotPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Play a Bot", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
class PlayRandomPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Seeking Opponent...", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)
        
        #return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack()
        
    def seekOpponent(self):
        """
        send request to LiChess server to seek an opponent
        """
        
        return
        
class ChallengePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        header = widgets.createLabel(self, text="Search Opponent Name", font="times", fontsize=14, fontweight="bold")
        header.pack(padx=10, pady=10)

        # name input and search button
        usernameEntry = widgets.createEntry(self, bgcolor="beige") 
        usernameEntry.pack(pady=10)
        challengeButton = widgets.createButton(self, function=lambda: self.challenge(controller, usernameEntry.get()),
                                                text="Challenge", bgcolor="sky blue")
        challengeButton.pack(pady=10)


        # return to main menu
        returnButton = widgets.createButton(self, function=lambda: controller.show_frame(MainMenuPage),
                                            text="Return to Main Menu", bgcolor="sky blue")
        returnButton.pack(pady=10)


    def challenge(self, controller, username=""):

        if username == "":
            print("User not found")
        else:

            # challenge user and set gameid
            gameid = interface.challenge_user(username)
            print(gameid)

            if not gameid:
                print("Unable to complete challenge")
            else:

                interface.change_gameid(gameid)

                # wait until challenger accepts challenge
                accepted = False
                while not accepted:
                    event = eventQueue.get()
                    if event["type"] == "gameStart":
                        if event["game"]["id"] == gameid:
                            accepted = True

                initialGameStreamProcess = mp.Process(target=initialgame_stream)
                initialGameStreamProcess.start()
                
                ingame(username, controller)

        return


"""
-------------------------------
FUNCTIONS
-------------------------------
"""

""" ingame: runs while user is currently in a game
	params:
		challengerName: name of player that user is playing
	return:
"""
def ingame(challengerName, controller):

    # create a game stream
    global gamestream
    gamestream = mp.Process(target=game_stream, args=(gameQueue,))
    gamestream.start()

    # create a game state
    gamestate = gameState.GameState(gameQueue=gameQueue)

    # start chessboard game window and wait until chessboard window is closed
    chessboard.init_chessboard(challengerName, gamestate)




""" event_stream: seperate process for event stream
	params:
		eventQueue: responses from LiChess event stream will be placed in queue
	return:
"""
def event_stream(eventQueue):
    iterator = 0
    while not terminated:
        try:
            time.sleep(3)
            # api call to start an event stream
            response = interface.create_eventstream()
            lines = response.iter_lines()

            # iterate through the response message
            for line in lines:
                # place response events in control queue
                if line:
                    event = json.loads(line.decode('utf-8'))
                    eventQueue.put_nowait(event)
                else:
                    eventQueue.put_nowait({"type": "ping"})
            

        except:
            pass
    return




""" game_stream: seperate process for game stream
    params:
    return:
"""
def game_stream(gameQueue):
    temp = None
    while not terminated:
        response = interface.create_gamestream()
        lines = response.iter_lines()
        time.sleep(3)
        #iterate through the response message
        for line in lines:
            if line:
                event = json.loads(line.decode('utf-8'))
                gameQueue.put_nowait(event)

    return


def initialgame_stream():
    response = interface.create_gamestream()




""" quit_program: terminates all processes and closes window
	params:
	return:
"""
def quit_program():
    global terminated
    global eventstream
    global gamestream

    terminated = True
    if eventstream != None:
        eventstream.terminate()
        eventstream.join()
    if gamestream != None:
        gamestream.terminate()
        gamestream.join()
    print("Quit Program")
    exit()

""" maps signal, SIGINT (keyboard interrupts), to quit_program """
signal.signal(signal.SIGINT, quit_program)

