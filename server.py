from flask import Flask, request
import joblib


app = Flask(__name__)

@app.route("/get-state", methods=["GET"])
def get_game_state():
    game_state = joblib.load("game_state")
    return game_state

@app.route("/change-state", methods=["POST"])
def change_game_state():
    game_change = dict(request.form)

    game_state = joblib.load("game_state")
    game_state[game_change["key"]] = game_change["change"]

    joblib.dump(game_state, "game_state")

    return ""

@app.route("/end-game", methods=["GET"])
def end_game():
    game_state = joblib.load("game_state")
    game_state["player"] = 1
    game_state["pub_notes"] = ""
    game_state["dice"] = ""
    game_state["piece_position"] = "none"
    game_state["new_piece"] = "none"
    joblib.dump(game_state, "game_state")

    return ""


if __name__=="__main__":
    game_state = {}
    game_state["player"] = 1
    game_state["pub_notes"] = ""
    game_state["rules"] = ""
    game_state["dice"] = ""
    game_state["piece_position"] = "none"
    game_state["new_piece"] = "none"
    joblib.dump(game_state, "game_state")
