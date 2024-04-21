import numpy as np
import matplotlib.pyplot as plt

def replaceInMatrix(arr, search, replace):
    newArr = np.where(arr == search, replace, arr)
    # newArr = [[_el if _el != search else replace for _el in _ar] for _ar in arr]
    return newArr


def create3DMatrix(matrix_2d):
    matrix_2d_empty = np.zeros((23, 23))
    matrix_2d = insertMatrixInMatrix(matrix_2d_empty, matrix_2d, (1, 1))

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


def insertMatrixInMatrix(big_matrix, small_matrix, position):
    big_matrix[
        position[0] : position[0] + small_matrix.shape[0],
        position[1] : position[1] + small_matrix.shape[1],
    ] = small_matrix
    return big_matrix