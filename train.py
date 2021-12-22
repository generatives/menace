from menace import MenaceAgent
from tictactoe import PerfectAgent, TurnRecord, get_game_state, RandomAgent
from collections import deque
import json
from typing import Dict

def play_game(player_one, player_two, mirror_for_player_two=False):
    turns = []
    position = [0] * 9
    game_state = -1
    while game_state == -1:
        player_one_move = player_one.move(position)
        turns.append(TurnRecord(position.copy(), player_one_move))
        position[player_one_move] = 1
        game_state = get_game_state(position)
        if(game_state == -1):
            player_two_position = position
            if mirror_for_player_two:
                player_two_position = [0] * 9
                for i in range(0, 9):
                    player_two_position[i] = 1 if position[i] == 2 else (2 if position[i] == 1 else 0)
            player_two_move = player_two.move(player_two_position)
            position[player_two_move] = 2
            game_state = get_game_state(position)
    
    return (turns, game_state, position)

def save_menace_weights(filename, weights: Dict[int, list[int]]):
    str = json.dumps(weights)
    with open(f"./{filename}", "w") as f:
        f.write(str)

def generate_models():
    agent = MenaceAgent()
    save_menace_weights("menace_agent_untrained.json", agent.position_weight_table)
    training_agent = PerfectAgent(2)
    validation_agent = PerfectAgent(2)
    episodes = 5000
    start_explore = 1
    end_explore = 0
    episodes_per_diff = 10
    explore_diff_rate = (end_explore - start_explore) / (episodes / episodes_per_diff)
    training_agent.explore_rate = start_explore
    saved = 0
    for i in range(0, episodes):
        (turns, game_state, position) = play_game(agent, training_agent)
        agent.learn_from_game(turns, game_state)

        if i != 0 and i % episodes_per_diff == 0:
            training_agent.explore_rate = training_agent.explore_rate + explore_diff_rate

        if i % 5 == 0:
            results = deque(maxlen=100)
            for j in range(0, 100):
                (turns, game_state, position) = play_game(agent, validation_agent)
                results.append(1 if game_state == 1 or game_state == 0 else 0)

            win_rate = sum(results) / len(results)
            if win_rate >= 0.25 and saved == 0:
                save_menace_weights("menace_agent_25.json", agent.position_weight_table)
                saved = saved + 1
                print(f"Saved 25 with {win_rate} at {i}")
            if win_rate >= 0.50 and saved == 1:
                save_menace_weights("menace_agent_50.json", agent.position_weight_table)
                saved = saved + 1
                print(f"Saved 50 with {win_rate} at {i}")
            if win_rate >= 0.75 and saved == 2:
                save_menace_weights("menace_agent_75.json", agent.position_weight_table)
                saved = saved + 1
                print(f"Saved 75 with {win_rate} at {i}")
            if win_rate >= 0.95 and saved == 3:
                save_menace_weights("menace_agent_95.json", agent.position_weight_table)
                saved = saved + 1
                print(f"Saved 95 with {win_rate} at {i}")

def main():
    agent = MenaceAgent()
    other_agent = PerfectAgent(2, 0.75)
    results = deque(maxlen=20)
    for i in range(0, 500):
        (turns, game_state, position) = play_game(agent, other_agent)
        agent.learn_from_game(turns, game_state)
        results.append(1 if game_state == 1 or game_state == 0 else 0)

        if i % 20 == 0:
            win_rate = sum(results) / len(results)
            print(win_rate)

if __name__ == "__main__":
    generate_models()