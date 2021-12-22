from typing import Tuple

def to_position(position_hash):
    remainder = position_hash
    position = []
    for index in range(8, -1, -1):
        if remainder > 0:
            two_val = 2 * pow(3, index)
            if remainder >= two_val:
                remainder = remainder - two_val
                position.append(2)
                continue

            one_val = pow(3, index)
            if remainder >= one_val:
                remainder = remainder - one_val
                position.append(1)
                continue

        position.append(0)
    return position

def to_position_hash(position):
    position_hash = 0
    for index in range(8, -1, -1):
        val = position[8 - index]
        position_hash = position_hash + val * pow(3, index)

    return position_hash

def index_to_coord(index):
    (y, x) = divmod(index, 3)
    return (x, y)

def coord_to_index(coord):
    (x, y) = coord
    return y * 3 + x

def rotate_coord_90_degrees(coord):
    (x, y) = coord
    return (2 - y, x)

# flips around +x, +y axis
def flip_position_diagonally(position):
    return [
        position[8], position[5], position[2],
        position[7], position[4], position[1],
        position[6], position[3], position[0]
    ]

# flips around y axis
def flip_position_horizontally(position):
    return [
        position[2], position[1], position[0],
        position[5], position[4], position[3],
        position[8], position[7], position[6]
    ]

# rotate +90 degrees
def rotate_position_90_degrees(position):
    return [
        position[6], position[3], position[0],
        position[7], position[4], position[1],
        position[8], position[5], position[2]
    ]

def _get_smallest_rotation_hash(position, smallest_hash):
    for i in range(0, 4):
        position = rotate_position_90_degrees(position)
        position_hash = to_position_hash(position)
        if position_hash < smallest_hash:
            smallest_hash = position_hash

    return smallest_hash

rotations=[
    [0,1,2,3,4,5,6,7,8],
    [0,3,6,1,4,7,2,5,8],
    [6,3,0,7,4,1,8,5,2],
    [6,7,8,3,4,5,0,1,2],
    [8,7,6,5,4,3,2,1,0],
    [8,5,2,7,4,1,6,3,0],
    [2,5,8,1,4,7,0,3,6],
    [2,1,0,5,4,3,8,7,6]
]

def apply_rotation(position, rotation):
    return [
        position[rotation[0]], position[rotation[1]], position[rotation[2]],
        position[rotation[3]], position[rotation[4]], position[rotation[5]],
        position[rotation[6]], position[rotation[7]], position[rotation[8]]
    ]

def rotate_index(index, rotation):
    return rotation.index(index)

def apply_inverse_rotation(position, rotation):
    return [
        position[rotation.index(0)], position[rotation.index(1)], position[rotation.index(2)],
        position[rotation.index(3)], position[rotation.index(4)], position[rotation.index(5)],
        position[rotation.index(6)], position[rotation.index(7)], position[rotation.index(8)]
    ]

def inverse_rotate_index(index, rotation):
    return rotation[index]

def get_min_hash_with_rotation(position: list[int]) -> Tuple[int, list[int]]:
    hashes_with_rotations = [(to_position_hash(apply_rotation(position, rotation)), rotation) for rotation in rotations]
    t = min(hashes_with_rotations, key = lambda t: t[0])
    return t

def get_min_hash(position):
    def_pos_hash = to_position_hash(position)
    for rotation in rotations:
        new_position = [
            position[rotation[0]], position[rotation[1]], position[rotation[2]],
            position[rotation[3]], position[rotation[4]], position[rotation[5]],
            position[rotation[6]], position[rotation[7]], position[rotation[8]]
        ]
        new_position_hash = to_position_hash(new_position)
        if new_position_hash < def_pos_hash:
            def_pos_hash = new_position_hash
    return def_pos_hash

def positions_are_equivalent(position_1, position_2):
    return get_min_hash(position_1) == get_min_hash(position_2)

# prints out an 2d board position
def print_position(position):
    print(position[0:3])
    print(position[3:6])
    print(position[6:9])
    print('\n')