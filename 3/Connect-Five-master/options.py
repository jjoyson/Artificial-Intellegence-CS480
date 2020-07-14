
boardSize = 9

def getCols():
    global boardSize
    return boardSize

def getRows():
    global boardSize
    return boardSize-1

def getTotalCells():
    global boardSize
    return boardSize*(boardSize-1)
