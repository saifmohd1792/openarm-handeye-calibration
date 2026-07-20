import cv2
def create_charuco_board(
    squares_x,
    squares_y,
    square_length,
    marker_length,
    dictionary_id=cv2.aruco.DICT_6X6_250,
):
    dictionary = cv2.aruco.getPredefinedDictionary(
        dictionary_id
    )

    board = cv2.aruco.CharucoBoard(
        size=(squares_x, squares_y),
        squareLength=square_length,
        markerLength=marker_length,
        dictionary=dictionary,
    )

    return board, dictionary