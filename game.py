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
PLAYER = -1
PIECES = []
URL = "https://divingmad.pythonanywhere.com/"

# ---------------------- Bound functions ---------------------
def throw_dice():
    number = random.randint(1, 6)

    DICE.configure(state="normal")
    DICE.delete("1.0", "end")
    DICE.insert("1.0", "Dice shows: " + str(number))
    DICE.configure(state="disabled")

def next_turn():
    game_state = {}
    game_state["player"] = PLAYER*(-1)
    game_state["rules"] = RULES.get("1.0", "end-1c")
    game_state["pub_notes"] = PUB_NOTES.get("1.0", "end-1c")
    game_state["dice"] = DICE.get("1.0", "end-1c")

    game_state["piece_positions"] = ""
    for piece, piece_name in PIECES:
        x, y = BOARD.coords(piece)
        game_state["piece_positions"] += f"{x} {y} {piece_name}\n"

    requests.post(URL+"change-state", data=game_state)
    BOARD.quit()

def add_piece(piece_text=None, position=None):
    if piece_text is None:
        piece_text = PIECE_ENTRY.get()
    if position is None:
        piece = BOARD.create_image(0, 0, image=PIECE_IMAGES[piece_text])
    else:
        piece = BOARD.create_image(*position, image=PIECE_IMAGES[piece_text])

    PIECES.append((piece, piece_text))

def drag_piece(event):
    closest = None
    min_dist = 70
    eventx, eventy = event.x, event.y

    for piece, _ in PIECES:
        piecex, piecey = BOARD.coords(piece)
        dist = ((piecex - eventx)**2 + (piecey - eventy)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = piece
    if closest is not None:
        BOARD.coords(closest, (eventx, eventy))

def exit_game(event):
    next_turn()

    t = requests.get(URL+"end-game")

    GAME.destroy()
    sys.exit()

def quit_game(event):
    GAME.destroy()
    sys.exit()

def set_game_state(game_state):
    global PIECES
    RULES.delete("1.0", "end")
    RULES.insert("1.0", game_state["rules"])

    PUB_NOTES.delete("1.0", "end")
    PUB_NOTES.insert("1.0", game_state["pub_notes"])

    DICE.configure(state="normal")
    DICE.delete("1.0", "end")
    DICE.insert("1.0", game_state["dice"])
    DICE.configure(state="disabled")

    for piece, _ in PIECES:
        BOARD.delete(piece)
    PIECES = []

    piece_positions = game_state["piece_positions"]
    if piece_positions != "none":
        for piece_text in piece_positions.split("\n"):
            piece_list = piece_text.split(" ")
            if len(piece_list) != 3:
                continue
            x, y, piece_name = piece_list[0], piece_list[1], piece_list[2]
            add_piece(piece_text=piece_name, position=(int(float(x)), int(float(y))))


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

# Create official noteboard
PUB_NOTES = tk.Text(GAME, bg="white", width=1, height=1, cursor="arrow")
PUB_NOTES.grid(row=1, column=1, sticky=tk.NSEW)

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
image_king = Image.open("pieces/king.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/(ROWS*2))))
image_thresh = Image.open("pieces/thresh.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/(ROWS*2))))
image_assassin = Image.open("pieces/assassin.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/(ROWS*2))))
image_tank = Image.open("pieces/tank.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/(ROWS*2))))
image_ranged = Image.open("pieces/ranged.jpg").resize((int(WIDTH/(COLS*2)), int(HEIGHT/(ROWS*2))))
PIECE_IMAGES = {
    "wking": ImageTk.PhotoImage(image_king),
    "bking": ImageTk.PhotoImage(image_king.rotate(180)),
    "wthresh": ImageTk.PhotoImage(image_thresh),
    "bthresh": ImageTk.PhotoImage(image_thresh.rotate(180)),
    "wassassin": ImageTk.PhotoImage(image_assassin),
    "bassassin": ImageTk.PhotoImage(image_assassin.rotate(180)),
    "wtank": ImageTk.PhotoImage(image_tank),
    "btank": ImageTk.PhotoImage(image_tank.rotate(180)),
    "wranged": ImageTk.PhotoImage(image_ranged),
    "branged": ImageTk.PhotoImage(image_ranged.rotate(180)),
}

# ------------------------ Main Loop -------------------------------------
def wait_loop():
    player_turn = PLAYER*(-1)

    while player_turn != PLAYER:
        time.sleep(1)
        server_response = requests.get(URL+"get-state")

        if server_response.status_code != 200:
            raise Exception(f"Server responded with {server_response}")

        game_state = server_response.json()
        player_turn = int(game_state["player"])
        print(player_turn)
    set_game_state(game_state)

if __name__=="__main__":
    requests.get(URL+"start-game")
    while True:
        wait_loop()
        GAME.mainloop()
