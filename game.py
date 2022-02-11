"""This is the user side script which runs the GUI of the board game.

- Create last server side
- Test server side
"""
# -------------------------- Imports ----------------------------------
import tkinter as tk
import random
import requests
import joblib
from PIL import ImageTk, Image
import sys
import time


# --------------------- Constants -----------------------------
ROWS = 12
COLS = 12
PLAYER = 1
PIECES = []
URL = "http://127.0.0.1:5000/"

# ---------------------- Bound functions ---------------------
def throw_dice():
    number = random.randint(1, 6)

    DICE.configure(state="normal")
    DICE.delete("1.0", "end")
    DICE.insert("1.0", "Dice shows: " + str(number))
    DICE.configure(state="disabled")

    change_game_state("dice", "Dice shows: " + str(number))

def next_turn():
    change_game_state("player", PLAYER*(-1))
    BOARD.quit()

def add_piece(piece_text=None):
    change = False
    if piece_text is None:
        change = True
        piece_text = PIECE_ENTRY.get()
    piece = BOARD.create_image(0, 0, image=PIECE_IMAGES[piece_text])

    PIECES.append(piece)

    if change:
        change_game_state("new_piece", piece_text)

def drag_piece(event):
    closest = None
    min_dist = 70
    eventx, eventy = event.x, event.y

    for piece in PIECES:
        piecex, piecey = BOARD.coords(piece)
        dist = ((piecex - eventx)**2 + (piecey - eventy)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = piece
    if closest is not None:
        BOARD.coords(closest, (eventx, eventy))
        change_game_state("piece_position", f"{eventx} {eventy} {closest}")

def exit_game(event):
    change_game_state("rules", RULES.get("1.0", "end"))
    t = requests.get(URL+"end-game")
    print("exit_game", t.status_code)

    GAME.destroy()
    sys.exit()

def quit_game(event):
    GAME.destroy()
    sys.exit()

def change_game_state(key, change):
    t = requests.post(URL+"change-state", data={"key": key, "change": change})
    print("change_game_state:", t.status_code)

def set_game_state(game_state):
    RULES.delete("1.0", "end")
    RULES.insert("1.0", game_state["rules"])

    PUB_NOTES.delete("1.0", "end")
    PUB_NOTES.insert("1.0", game_state["pub_notes"])

    DICE.delete("1.0", "end")
    DICE.insert("1.0", game_state["dice"])

    if game_state["new_piece"] != "none":
        add_piece(game_state["new_piece"])

    if game_state["piece_position"] != "none":
        piecepos = game_state["piece_position"].split(" ")
        BOARD.coords(int(piecepos[2]), (int(piecepos[0]), int(piecepos[1])))


# --------------------------- Init ------------------------------------
# Create the game window
GAME = tk.Tk()
GAME.attributes("-fullscreen", True)
GAME.bind("<Escape>", quit_game)
GAME.bind("<Control-Key-1>", exit_game)

# Create the board layout
GAME.columnconfigure(0, weight=10) # Canvas
GAME.columnconfigure(1, weight=1) # assets

GAME.rowconfigure(0, weight=3) # Rules
GAME.rowconfigure(1, weight=2) # Official notes
GAME.rowconfigure(2, weight=1) # Private notes
GAME.rowconfigure(3, weight=1) # Dice
GAME.rowconfigure(4, weight=0) # Add pieces
GAME.rowconfigure(5, weight=0) # Buttons

# Create rule box with rules
RULES = tk.Text(GAME, bg="grey", width=1, height=1, cursor="circle")
RULES.grid(row=0, column=1, sticky=tk.NSEW)
RULES.bind("<Key>", lambda event: change_game_state("rules", RULES.get("1.0", "end-1c")))

# Create official noteboard
PUB_NOTES = tk.Text(GAME, bg="white", width=1, height=1, cursor="arrow")
PUB_NOTES.grid(row=1, column=1, sticky=tk.NSEW)
.bind("<Key>", lambda event: change_game_state("rules", PUB_NOTES.get("1.0", "end-1c")))

# Create private noteboard
PRIVATE_NOTES = tk.Text(GAME, bg="white", width=1, height=1, cursor="arrow")
PRIVATE_NOTES.grid(row=2, column=1, sticky=tk.NSEW)

# Create dice text box
DICE = tk.Text(GAME, bg="grey", width=1, height=1, state=tk.DISABLED, cursor="cross")
DICE.grid(row=3, column=1, sticky=tk.NSEW)

# Create piece_adder
PIECE_ENTRY = tk.Entry(GAME, bg="white")
PIECE_ENTRY.grid(row=4, column=1, sticky=tk.W)
PIECE_BTN = tk.Button(GAME, text="Add piece", command=add_piece)
PIECE_BTN.grid(row=4, column=1, sticky=tk.E)

# Create button for dice
DICE_BTN = tk.Button(GAME, text="Throw dice", command=throw_dice)
DICE_BTN.grid(row=5, column=1, sticky=tk.W)

# Create button for next turn
TURN_BTN = tk.Button(GAME, text="Next turn", command=next_turn)
TURN_BTN.grid(row=5, column=1, sticky=tk.E)

# Create board game canvas
BOARD = tk.Canvas(GAME, bg="white", cursor="hand1")
BOARD.grid(row=0, column=0, rowspan=6, sticky=tk.NSEW)
BOARD.bind("<B1-Motion>", drag_piece)

WIDTH = 10*GAME.winfo_screenwidth()/11
HEIGHT = GAME.winfo_screenheight()
for row in range(ROWS):
    ypos = row*HEIGHT/ROWS
    BOARD.create_line(0, ypos, WIDTH, ypos)
for col in range(COLS):
    xpos = col*WIDTH/COLS
    if col not in [4, 5, 6, 7, 8]:
        BOARD.create_line(xpos, HEIGHT/ROWS, xpos, (ROWS-1)*HEIGHT/COLS)
    else:
        BOARD.create_line(xpos, 0, xpos, HEIGHT)

#Pieces
image_king = Image.open("pieces/kung.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/ROWS)))
image_thresh = Image.open("pieces/thresh.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/ROWS)))
image_assassin = Image.open("pieces/assassin.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/ROWS)))
image_tank = Image.open("pieces/tank.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/ROWS)))
PIECE_IMAGES = {
    "wking": ImageTk.PhotoImage(image_king),
    "bking": ImageTk.PhotoImage(image_king.rotate(180)),
    "wthresh": ImageTk.PhotoImage(image_thresh),
    "bthresh": ImageTk.PhotoImage(image_thresh.rotate(180)),
    "wassassin": ImageTk.PhotoImage(image_assassin),
    "bassassin": ImageTk.PhotoImage(image_assassin.rotate(180)),
    "wtank": ImageTk.PhotoImage(image_tank),
    "btank": ImageTk.PhotoImage(image_tank.rotate(180)),
}

# ------------------------ Main Loop -------------------------------------
def wait_loop():
    player_turn = PLAYER*(-1)

    while player_turn != PLAYER:
        time.sleep(0.2)
        server_response = requests.get(URL+"get-state")

        if server_response.status_code != 200:
            raise Exception(f"Server responded with {server_response}")

        game_state = server_response.json()
        print(game_state)
        set_game_state(game_state)
        player_turn = int(game_state["player"])

if __name__=="__main__":
    while True:
        wait_loop()
        GAME.mainloop()
