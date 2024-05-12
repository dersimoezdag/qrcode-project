import os

import numpy as np
from itertools import permutations
from math import factorial
from pyzbar.pyzbar import decode as decodeQRCode

from baseChecks import isValidQRCode
from matrixHelper import (
    insertMatrixInMatrix,
    replaceInMatrix,
    create_qr_code_image,
    create3DMatrix,
    remove2DItemFrom3DArray,
)

from matrixStore import tilesListCenter, maxKnownMatrix, validPositions, validFor1818

## Settings start
# activate testmode
testmode = False
# 0,1,2
stepMode = 0
# times to iterate befor stop
iterateXTimes = 9999999999
## Settings end


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
        f"\t⏳ {title}: [{done_str}{togo_str}] {percent_done}% done. Current Element: {index}",
        end="\r",
    )

    if round(percent_done) == 100:
        print("\t✅")


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


def validateQRCode(matrix):
    if isValidQRCode(matrix, testmode):
        replacedMatrixToTest = create3DMatrix(matrix)
        decodedQR = decodeQRCode(replacedMatrixToTest)

        if decodedQR and decodedQR[0] and decodedQR[0].data:
            return {"valid": True, "data": decodedQR[0].data}
        else:
            return {"valid": False, "data": None}
    else:
        return {"valid": False, "data": None}


def mainQRLoop(tiles, positions, matrix):
    permutationGenerator = permutations(tiles)
    amountToCalculate = factorial(len(tiles))

    countMainLoop = 0
    while countMainLoop < iterateXTimes:
        countMainLoop += 1
        print_percent_done(countMainLoop, iterateXTimes)

        perm = next(permutationGenerator)
        result_matrix = matrix

        i = 0
        for single_tile in perm:
            position = positions[i]
            result_matrix = insertMatrixInMatrix(result_matrix, single_tile, position)
            i += 1

        # print(result_matrix)
        result = validateQRCode(result_matrix)

        # Überprüfen, ob die Matrix ein gültiger QR-Code ist
        if result["valid"] == True:
            if decodedQR and decodedQR[0] and decodedQR[0].data:
                print("Decoded: ", result["data"])
                print("Test erfolgreich!")
                create_qr_code_image(
                    result_matrix, "res/valid_qr_code_" + str(countMainLoop) + "_.png"
                )
                np.save("res/valid_test_" + str(countMainLoop), result_matrix)
                print("Treffer als png gespeichert!")
        # else:
        # print("Die Matrix ist kein gültiger QR-Code.")


# Main
if __name__ == "__main__":

    try:
        os.makedirs("./res")
    except FileExistsError:
        # directory already exists
        pass

    if testmode == True:
        if isValidQRCode(testMatrix, testmode):
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

    corner1818 = validFor1818[stepMode]
    tiles = tilesListCenter
    tiles = remove2DItemFrom3DArray(tiles, corner1818)

    positions = validPositions
    positions.remove((18, 18))

    # Check lists for valid length
    if len(tiles) != len(positions):
        print("ERROR:")
        print(
            "tilesListCenter: " + str(len(tiles)),
            "validPositions:" + str(len(positions)),
        )
        quit()

    matrix = insertMatrixInMatrix(maxKnownMatrix, corner1818, (18, 18))

    mainQRLoop(tiles, positions, matrix)
