import random
from position_utils import get_min_hash_with_rotation, inverse_rotate_index, rotate_index, to_position
from tictactoe import TurnRecord
from positions import list_playable_min_hashes

class MenaceAgent:
    position_weight_table: dict[int, list[int]]

    def __init__(self, position_weight_table: dict[int, list[int]] = None):
        if position_weight_table == None:
            self.position_weight_table = self._generate_position_weight_table()
        else:
            self.position_weight_table = position_weight_table

    def _generate_position_weight_table(self):
        position_weight_table = {}
        for min_hash in list_playable_min_hashes(1):
            position_weights = [0] * 9
            position = to_position(min_hash)
            move_num = sum([1 if s == 1 else 0 for s in position])
            init_count = 5 - move_num
            for index in range(0, 9):
                if position[index] == 0:
                    position_weights[index] = init_count
            position_weight_table[min_hash] = position_weights
        return position_weight_table

    def move(self, current_position: list[int]):
        (min_hash, rotation) = get_min_hash_with_rotation(current_position)
        position_weights = self.position_weight_table[min_hash]
        if position_weights.count(0) != 9:
            [index] = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], weights=position_weights)
            move = inverse_rotate_index(index, rotation)
            if current_position[move] != 0:
                print("broke")
            return move
        else:
            return -1

    def learn_from_game(self, turns: list[TurnRecord], who_won: int):
        diff = 3 if who_won == 1 else (-1 if who_won == 2 else 1)
        for turn in turns:
            (min_hash, rotation) = get_min_hash_with_rotation(turn.position)
            min_hash_move = rotate_index(turn.move, rotation)
            position_weights = self.position_weight_table[min_hash]
            position_weights[min_hash_move] = max(position_weights[min_hash_move] + diff, 1)