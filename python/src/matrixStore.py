import numpy as np

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
tile_17 = np.array([
    [1,0,1],
    [0,0,0],
    [1,1,1]
    ])
tile_18 = np.array([
    [0,1,0],
    [1,1,1],
    [1,1,0]
    ])
tile_19 = np.array([
    [1,0,1],
    [1,0,0],
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

tilesListCenter = [
    tile_04,
    tile_11,
    tile_17,
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

validFor1818 = [tile_25, tile_27, tile_49]

validForTimingRow = {
    "left": [tile_17, tile_25],
    "middle": [tile_18, tile_11, tile_32, tile_34],
    "right": [tile_19, tile_25, tile_39, tile_33],
}

validForTimingColMiddle = {
    "top": validForTimingRow["left"],
    "middle": [],
    "bottom": [],
}
