import os
import numpy as np
from itertools import permutations
from math import factorial
from pyzbar.pyzbar import decode as decodeQRCode

from baseChecks import isValidQRCode
from matrixHelper import insertMatrixInMatrix, replaceInMatrix, create_qr_code_image, create3DMatrix

from matrixStore import tilesList, maxKnownMatrix,validPositions,validFor1818

testmode = False
# 0,1,2
stepMode = 0


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

def mainQRLoop(list,positions,matrix):
    permutationGenerator = permutations(list)
    amountToCalculate = factorial(len(list))

    iterateXTimes = 9999999999

    countMainLoop = 0
    while countMainLoop < iterateXTimes:
        countMainLoop += 1
        print_percent_done(countMainLoop, iterateXTimes)

        perm = next(permutationGenerator)
        result_matrix = matrix

        i = 0
        for tile in perm:
            result_matrix = insertMatrixInMatrix(result_matrix, tile, positions[i])
            i += 1

        # print(result_matrix)

        # Überprüfen, ob die Matrix ein gültiger QR-Code ist
        if isValidQRCode(result_matrix, testmode):
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
    tiles = tilesList
    tiles.remove(corner1818)

    positions = validPositions
    positions.remove((18,18))

    matrix = insertMatrixInMatrix(maxKnownMatrix,corner1818,(18,18))

    # Check lists for valid length
    if len(tilesList) != 22 or len(positions) != 22:
        print(
            "tilesList: " + len(tiles),
            "validPositions:" + len(positions),
            "should both be: " + 22,
        )

    mainQRLoop(tiles,positions,matrix)

    
