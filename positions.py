from tictactoe import get_game_state
from position_utils import get_min_hash

def _add_position(position, perspective_player, player, player_one_positions, player_two_positions):
    if get_game_state(position) == -1:
        min_hash = get_min_hash(position)
        if min_hash in player_one_positions or min_hash in player_two_positions:
            return
        if player == perspective_player:
            player_one_positions.append(min_hash)

        for move in range(0, 9):
            if position[move] == 0:
                position[move] = player
                # 3 - player = 1 - (player - 1) + 1
                _add_position(position, perspective_player, 3 - player, player_one_positions, player_two_positions)
                position[move] = 0

def list_playable_min_hashes(perspective_player: int) -> list[int]:
    position = [0] * 9
    player_one_positions = []
    _add_position(position, perspective_player, 1, player_one_positions, {})
    return player_one_positions