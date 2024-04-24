import numpy as np

def isValidQRCode(matrix,testmode):
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