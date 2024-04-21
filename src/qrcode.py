import os, errno
import time
import sys
import numpy as np
import yaml
import matplotlib.pyplot as plt
from itertools import permutations
from math import factorial
from pyzbar.pyzbar import decode as decodeQRCode
import cv2

testmode = False


def print_percent_done(index, total, bar_len=50, title="Please wait"):
    """
    index is expected to be 0 based index.
    0 <= index < total
    """
    percent_done = (index + 1) / total * 100
    percent_done = round(percent_done, 3)

    done = round(percent_done / (100 / bar_len))
    togo = bar_len - done

    done_str = "█" * int(done)
    togo_str = "░" * int(togo)

    print(
        f"\t⏳{title}: [{done_str}{togo_str}] {percent_done}% done. Current Element: {index}",
        end="\r",
    )

    if round(percent_done) == 100:
        print("\t✅")


def is_valid_qr_code(matrix):
    # Unnötig für aktuellen Fall

    # # Überprüfen, ob die Matrix 21x21 ist
    # if matrix.shape != (21, 21):
    #     if testmode: print("shape error")
    #     return False

    # # Überprüfen, ob es keine schwarzen Quadrate im zentralen 5x5-Bereich gibt
    # if np.sum(matrix[8:13, 8:13]) > 0:
    #     if testmode: print("central area error")
    #     return False

    # # Überprüfen, ob es genau 3 schwarze Quadrate in den Ecken gibt
    # if matrix[0, 0] != 1 or matrix[0, 20] != 1 or matrix[20, 0] != 1:
    #     if testmode:  print("orientation square error")
    #     return False

    # Überprüfe Timingreihen
    expectedValues = [0, 1, 0, 1, 0, 1, 0]
    if np.array_equal(matrix[6, 6:13], expectedValues):
        if testmode:
            print("timing row error")
        return False
    if np.array_equal(matrix[6:16, 6], expectedValues):
        if testmode:
            print("timing row error")
        return False

    # Überprüfe Matrixcode (Prüfen, ob die untere rechte 2x2-Submatrix der 21x21-Matrix mit dem Encoding-Code übereinstimmt)
    # Vorliegend: Byte bei Matrix-Patter 2
    # fmt: off
    expectedEncodingCode = np.array([
        [0, 0], 
        [1, 0]
        ])
    # fmt: on
    if not np.array_equal(matrix[-2:, -2:], expectedEncodingCode):
        if testmode:
            print("encoding code error")
            print(matrix[-2:, -2:])
            print(expectedEncodingCode)
        return False

    # # Überprüfen, ob es keine 4 aufeinanderfolgenden schwarzen Quadrate in einer Zeile oder Spalte gibt
    # maxSquaresInRow = 5
    # for i in range(21):
    #     if np.any(
    #         np.convolve(matrix[i], np.ones(maxSquaresInRow), mode="valid")
    #         == maxSquaresInRow
    #     ) or np.any(
    #         np.convolve(matrix[:, i], np.ones(maxSquaresInRow), mode="valid")
    #         == maxSquaresInRow
    #     ):
    #         if testmode:
    #             print("too many squares in row error")
    #         return False

    return True


def replaceInMatrix(arr, search, replace):
    newArr = np.where(arr == search, replace, arr)
    # newArr = [[_el if _el != search else replace for _el in _ar] for _ar in arr]
    return newArr


def create3DMatrix(matrix_2d):
    matrix_2d_empty = np.zeros((23, 23))
    matrix_2d = insert_matrix(matrix_2d_empty, matrix_2d, (1, 1))

    matrix_3d = np.zeros((23, 23, 3), dtype=np.uint8)
    matrix_3d[matrix_2d == 1] = [0, 0, 0]  # Schwarze Quadrate
    matrix_3d[matrix_2d == 0] = [255, 255, 255]  # Weiße Quadrate
    return matrix_3d


def create_qr_code_image(matrix, output_path):
    # Erstelle ein Bild aus der Matrix
    image = create3DMatrix(matrix)

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

maxKnownMatrix = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

testMatrix = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
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

    try:
        os.makedirs("./res")
    except FileExistsError:
        # directory already exists
        pass

    if testmode == True:
        if is_valid_qr_code(testMatrix):
            replacedMatrixToTest = create3DMatrix(testMatrix)
            decodedQR = decodeQRCode(replacedMatrixToTest)
            create_qr_code_image(testMatrix, "res/testmode_qr-code.png")
            np.save("res/testmode_qr-matrix", testMatrix)
            if decodedQR and decodedQR[0] and decodedQR[0].data:
                print("Decoded: ", decodedQR[0].data)
                print("Test erfolgreich!")
        else:
            print("Test fehlerhaft.")
        quit()

    permutationGenerator = permutations(tilesList)
    amountToCalculate = factorial(22)

    iterateXTimes = 9999999999

    countMainLoop = 0
    while countMainLoop < iterateXTimes:
        countMainLoop += 1
        print_percent_done(countMainLoop, iterateXTimes)

        perm = next(permutationGenerator)
        result_matrix = maxKnownMatrix

        i = 0
        for tile in perm:
            result_matrix = insert_matrix(result_matrix, tile, validPositions[i])
            i += 1

        # print(result_matrix)

        # Überprüfen, ob die Matrix ein gültiger QR-Code ist
        if is_valid_qr_code(result_matrix):
            replacedMatrixToTest = create3DMatrix(result_matrix)
            decodedQR = decodeQRCode(replacedMatrixToTest)

            if decodedQR and decodedQR[0] and decodedQR[0].data:
                print("Decoded: ", decodedQR[0].data)
                print("Test erfolgreich!")
                create_qr_code_image(
                    result_matrix, "res/valid_qr_code_" + str(countMainLoop) + "_.png"
                )
                np.save("res/valid_test_" + str(countMainLoop), result_matrix)
                print("Treffer als png gespeichert!")
        # else:
        # print("Die Matrix ist kein gültiger QR-Code.")
