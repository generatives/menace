from flask import Flask, Response, request, redirect, url_for
import json
from menace import MenaceAgent
from tictactoe import PerfectAgent, RandomAgent, get_game_state

app = Flask(__name__)

def load_menace_agent(filename): 
    with open(f"./{filename}") as f:
        str = f.read()
        string_weights = json.loads(str)
        weights = {int(key):value for (key,value) in string_weights.items()}
        return MenaceAgent(weights)

agents = [
    PerfectAgent(1),
    RandomAgent(),
    load_menace_agent("menace_agent_untrained.json"),
    load_menace_agent("menace_agent_25.json"),
    load_menace_agent("menace_agent_50.json"),
    load_menace_agent("menace_agent_75.json"),
    load_menace_agent("menace_agent_95.json")
]

@app.route("/")
def hello_world():
    return redirect(url_for("static", filename="index.html"))

@app.route("/move", methods=["POST"])
def move():
    requestData = request.get_json()
    position = requestData["position"]
    move = requestData["move"]
    opponent = requestData["opponent"]
    turns = []

    game_state = get_game_state(position)
    if game_state == -1 and move != None:
        if position[move] == 0:
            position[move] = 2
            turns.append({ "position": position.copy(), "game_state": game_state })

    game_state = get_game_state(position)
    if game_state == -1:
        opponent_move = agents[opponent].move(position)
        position[opponent_move] = 1
        game_state = get_game_state(position)
        turns.append({ "position": position.copy(), "game_state": game_state })

    response = {
        "turns": turns
    }
    return Response(json.dumps(response), mimetype='application/json')
