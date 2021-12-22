from typing import Dict
from position_utils import apply_rotation, get_min_hash_with_rotation, inverse_rotate_index, print_position
import random
import math

class TurnRecord:
    position = []
    move = 0

    def __init__(self, position, move):
        self.position = position
        self.move = move

_win_patterns = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

def _get_winner(position):
    for pattern in _win_patterns:
        if position[pattern[0]] != 0 and position[pattern[0]] == position[pattern[1]] and position[pattern[1]] == position[pattern[2]]:
            return position[pattern[0]]
    return -1

def _moves_left(position):
    return 0 in position

def get_game_state(position):
    winner = _get_winner(position)
    if winner != -1:
        return winner
    else:
        if _moves_left(position):
            return -1
        else:
            return 0

def get_valid_moves(position):
    valid_moves = []
    for i in range(0, 9):
        if position[i] == 0:
            valid_moves.append(i)
    return valid_moves

class RandomAgent:
    def move(self, position):
        possible_moves = get_valid_moves(position)
        
        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return -1

class PerfectAgent:
    def __init__(self, player, explore_rate = 0):
        self.move_table: Dict[int, list[int]] = {}
        self.score_table: Dict[int, int] = {}
        self.player: int = player
        self.explore_rate = explore_rate
        self._generate_move_table()

    def _score_position(self, position):
        game_state = get_game_state(position)
        other_player = 3 - self.player
        return 1 if game_state == self.player else 0 if game_state == 0 else -1 if game_state == other_player else None

    def _access_position(self, position, current_player):
        (min_hash, rotation) = get_min_hash_with_rotation(position)
        min_position = apply_rotation(position, rotation)

        # this position has already been accessed, we can skip this branch
        if min_hash in self.score_table:
            return self.score_table[min_hash]

        # this is a leaf position, we can return the score
        score = self._score_position(min_position)
        if score != None:
            self.score_table[min_hash] = score
            return score

        # this is a non-leaf node, we need to make a decision
        maximizing = self.player == current_player
        best_moves = []
        best_score = -math.inf if maximizing else math.inf
        for move in range(0, 9):
            if min_position[move] == 0:
                min_position[move] = current_player
                next_player = 3 - current_player
                move_score = self._access_position(min_position, next_player)
                # find the move with the best score
                if move_score == best_score:
                    best_moves.append(move)
                if (maximizing and move_score > best_score) or (not maximizing and move_score < best_score):
                    best_score = move_score
                    best_moves = [move]
                min_position[move] = 0
        
        self.score_table[min_hash] = best_score
        if self.player == current_player:
            self.move_table[min_hash] = best_moves

        return best_score

    def _generate_move_table(self):
        self._access_position([0] * 9, 1)

    def move(self, current_position: list[int]) -> int:
        (min_hash, rotation) = get_min_hash_with_rotation(current_position)
        if random.uniform(0, 1) > self.explore_rate:
            moves = self.move_table[min_hash]
            index = random.choice(moves)
            move = inverse_rotate_index(index, rotation)
            return move
        else:
            valid_moves = get_valid_moves(current_position)
            return random.choice(valid_moves)
