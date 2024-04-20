import numpy as np
import yaml
import matplotlib.pyplot as plt
from itertools import permutations
from tqdm import tqdm
from math import factorial


def is_valid_qr_code(matrix):
    # Überprüfen, ob die Matrix 21x21 ist
    if matrix.shape != (21, 21):
        print("shape error")
        return False

    # Überprüfen, ob es keine schwarzen Quadrate im zentralen 5x5-Bereich gibt
    if np.sum(matrix[8:13, 8:13]) > 0:
        print("central area error")
        return False

    # Überprüfen, ob es genau 3 schwarze Quadrate in den Ecken gibt
    if matrix[0, 0] != 1 or matrix[0, 20] != 1 or matrix[20, 0] != 1:
        print("orientation square error")
        return False

    # Überprüfe Timingreihen
    expected_values = [0, 1, 0, 1, 0, 1, 0]
    if np.array_equal(matrix[6, 6:13], expected_values):
        print("timing row error")
        return False
    if np.array_equal(matrix[6:16, 6], expected_values):
        print("timing row error")
        return False

    # Überprüfen, ob es keine 4 aufeinanderfolgenden schwarzen Quadrate in einer Zeile oder Spalte gibt
    for i in range(21):
        if np.any(np.convolve(matrix[i], np.ones(4), mode="valid") == 4) or np.any(
            np.convolve(matrix[:, i], np.ones(4), mode="valid") == 4
        ):
            print("too many squares in row error")
            return False

    return True


def create_qr_code_image(matrix, output_path):
    # Erstelle ein Bild aus der Matrix
    image = np.zeros((21, 21, 3), dtype=np.uint8)
    image[matrix == 1] = [0, 0, 0]  # Schwarze Quadrate
    image[matrix == 0] = [255, 255, 255]  # Weiße Quadrate

    # Speichere das Bild
    plt.imsave(output_path, image)
    print(f"Das Bild wurde als {output_path} gespeichert.")


def insert_matrix(big_matrix, small_matrix, position):
    big_matrix[
        position[0] : position[0] + small_matrix.shape[0],
        position[1] : position[1] + small_matrix.shape[1],
    ] = small_matrix
    return big_matrix


# 21x21-Matrix mit allen bekannten Elementen
baseMatrix = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

# fmt: off
tile_ = np.array([
    [1,1,1],
    [1,1,1],
    [1,1,1]
    ])
tile_04 = np.array([
    [1,0,0],
    [1,0,0],
    [1,0,1]
    ])
tile_11 = np.array([
    [0,1,0],
    [1,0,0],
    [0,0,1]
    ])
tile_18 = np.array([
    [0,1,0],
    [1,1,1],
    [1,1,0]
    ])
tile_22 = np.array([
    [1,0,0],
    [1,1,0],
    [1,0,0]
    ])
tile_23 = np.array([
    [0,0,0],
    [1,1,1],
    [0,0,1]
    ])
tile_24 = np.array([
    [0,1,1],
    [1,1,0],
    [0,1,0]
    ])
tile_25 = np.array([
    [1,0,1],
    [0,0,0],
    [1,1,0]
    ])
tile_26 = np.array([
    [0,0,1],
    [0,1,0],
    [1,0,0]
    ])
tile_27 = np.array([
    [1,0,0],
    [1,0,0],
    [0,1,0]
    ])
tile_28 = np.array([
    [0,0,1],
    [0,0,1],
    [1,1,0]
    ])
tile_32 = np.array([
    [0,1,0],
    [1,1,1],
    [0,1,1]
    ])
tile_33 = np.array([
    [1,0,1],
    [1,0,0],
    [0,0,1]
    ])
tile_34 = np.array([
    [0,1,0],
    [1,1,0],
    [0,1,1]
    ])
tile_35 = np.array([
    [1,1,0],
    [0,0,0],
    [1,1,1]
    ])
tile_39 = np.array([
    [1,0,1],
    [0,0,0],
    [0,1,1]
    ])
tile_40 = np.array([
    [1,1,1],
    [0,1,0],
    [1,1,0]
    ])
tile_41 = np.array([
    [1,0,1],
    [0,1,0],
    [1,0,1]
    ])
tile_42 = np.array([
    [0,0,1],
    [0,0,1],
    [1,1,0]
    ])
tile_46 = np.array([
    [1,1,0],
    [0,1,1],
    [1,1,1]
    ])
tile_47 = np.array([
    [1,1,0],
    [0,0,0],
    [1,0,1]
    ])
tile_48 = np.array([
    [1,1,1],
    [0,1,1],
    [1,0,0]
    ])
tile_49 = np.array([
    [0,0,0],
    [1,0,0],
    [0,1,0]
    ])
# fmt: on

tilesList = [
    tile_04,
    tile_11,
    tile_18,
    tile_22,
    tile_23,
    tile_24,
    tile_25,
    tile_26,
    tile_27,
    tile_28,
    tile_32,
    tile_33,
    tile_34,
    tile_35,
    tile_39,
    tile_40,
    tile_41,
    tile_42,
    tile_46,
    tile_47,
    tile_48,
    tile_49,
]


validPositions = [
    (9, 0),
    (9, 3),
    (9, 6),
    (0, 9),
    (3, 9),
    (6, 9),
    (9, 9),
    (12, 9),
    (15, 9),
    (18, 9),
    (9, 12),
    (12, 12),
    (15, 12),
    (18, 12),
    (9, 15),
    (12, 15),
    (15, 15),
    (18, 15),
    (9, 18),
    (12, 18),
    (15, 18),
    (18, 18),
]

# Main
if __name__ == "__main__":
    # Check lists for valid length
    if len(tilesList) != 22 or len(validPositions) != 22:
        print(
            "tilesList: " + len(tilesList),
            "validPositions:" + len(validPositions),
            "should both be: " + 22,
        )

    # start main script
    countPermutations = 0
    with open("./result.yml", "w") as yaml_file:
        yaml.dump(list(permutations(tilesList)), yaml_file, default_flow_style=False)

    # for perm in tqdm(availablePermuations):
    #     countMainLoop = 0
    #     for tile in perm:
    #         countMainLoop += 1

    #         for position in validPositions:
    #             result_matrix = insert_matrix(baseMatrix, tile, position)

    #         print(result_matrix)
    #         # Überprüfen, ob die Matrix ein gültiger QR-Code ist
    #         if is_valid_qr_code(result_matrix):
    #             create_qr_code_image(
    #                 result_matrix, "./valid_qr_code_" + countMainLoop + "_.png"
    #             )
    #         else:
    #             print("Die Matrix ist kein gültiger QR-Code.")
