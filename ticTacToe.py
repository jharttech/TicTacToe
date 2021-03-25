#Import needed library
from random import randrange
import subprocess


def main():
    #Clear screen
    subprocess.call('clear')
    #Ask user for board size
    ready = False
    while not ready:
        print(""" Welcome to
 ________  __           ________                  ________
/        |/  |         /        |                /        |
$$$$$$$$/ $$/   _______$$$$$$$$/______    _______$$$$$$$$/______    ______
   $$ |   /  | /       |  $$ | /      \  /       |  $$ | /      \  /      \.
   $$ |   $$ |/$$$$$$$/   $$ | $$$$$$  |/$$$$$$$/   $$ |/$$$$$$  |/$$$$$$  |
   $$ |   $$ |$$ |        $$ | /    $$ |$$ |        $$ |$$ |  $$ |$$    $$ |
   $$ |   $$ |$$ \_____   $$ |/$$$$$$$ |$$ \_____   $$ |$$ \__$$ |$$$$$$$$/
   $$ |   $$ |$$       |  $$ |$$    $$ |$$       |  $$ |$$    $$/ $$       |
   $$/    $$/  $$$$$$$/   $$/  $$$$$$$/  $$$$$$$/   $$/  $$$$$$/   $$$$$$$/
        """)
        size = input("Please pick a board size : (3x3 up to 9x9, must be square)")
        subprocess.call('clear')
        if size[0] == size[2] and size[0] >= '3' and size[0] <= '9':
            ready = True
    #Square the size to get number of boxes needed
    boxes = int(size[0]) ** 2
    #Create the board
    board = makeBoard(boxes, size)
    #Set starting move by computer
    board[1][1] = ' X'
    #Start the game
    gameOver = False
    #Draw the board to screen
    display_board(board, boxes)
    while not gameOver:
        #Get and assign a list of free spots to freeSpots variable
        freeSpots = make_list_of_free_fields(board)
        #Assign users move a O if users move is a free square
        enter_move(board, freeSpots, size)
        sign = ' O'
        #Check for a victory
        gameOver = victory_for(board, sign, size)
        #End the game if victory is found
        if gameOver:
            exit()
        #Update free spot list
        freeSpots = make_list_of_free_fields(board)
        #Assign computer move a X
        draw_move(board, freeSpots, boxes, size)
        sign = ' X'
        #Check for a victory
        gameOver = victory_for(board, sign, size)
        #Clear terminal screen to imitate non moving board
        subprocess.call('clear')
        #Draw the board to screen
        display_board(board, boxes)
        #End game if victory was found
        if gameOver:
            exit()

def display_board(board, boxes):
    # The function accepts one parameter containing the board's current status
    # and accepts another for number of boxes on board
    # and prints it out to the console.

    #Get the number of columns by taking the square-root of boxes and Assign
    #to columnCount variable
    columnCount = int(boxes ** 0.5)
    #Preload varibles for spaceing format of board
    spaceBefore = "   "
    spaceAfter = "   "
    #Draw each row of the board
    for row in range(0,len(board)):
        column = 0
        for y in range(0, columnCount):
            print("+--------", end='')
        print("+")
        for z in range(0, columnCount):
            print("|        ", end='')
        print("|")
        for x in range(0, columnCount):
            print("|" + spaceBefore + str(board[row][column + x]) + spaceAfter, end='')
        print("|")
        for v in range(0, columnCount):
            print("|        ", end='')
        print("|")
    for m in range(0, columnCount):
        print("+--------", end='')
    print("+")

def enter_move(board, freeSpots, size):
    # The function accepts the board current status, asks the user about their move,
    # checks the input and updates the board according to the user's decision.

    #Create an empty currrentMove variable for use later
    currentMove = ''
    #If currentMove is empty then start
    if currentMove == '':
        #Set to false so input prompt is asked until a free spot is selected for the move
        allowed = False
        while not allowed:
            #Ask for users move choice
            currentMove = int(input("Enter your move: "))
            #If user inputs single placeholder int add the leading zero
            if currentMove <= 9:
                currentMove = ('0' + str(currentMove))
            currentMove = str(currentMove)
            #Convert currentMove to a coordinate on board using a dictionary
            coordOfMove = numToCoord(int(currentMove), size)
            #Create a list of free spots and compare to see if user input is a free spot
            for i in range(0,len(freeSpots)):
                if currentMove == freeSpots[i]:
                    #If user input was a free spot then set allowed to true to end while loop
                    allowed = True
                    #Set the coordinate of the board to O to represent users move
                    board[coordOfMove[0] - 1][coordOfMove[1] - 1] = ' O'
                    return board
            #Tell user if they selected a used square for their move
            print("Square already taken!")

def make_list_of_free_fields(board):
    # The function browses the board and builds a list of all the free squares;

    #Create empty list of free squares
    free = []
    for row in range(0,len(board)):
        #Look through the board for free squares
        for column in range(0,len(board[row])):
            #If square is not assigned an X or O it is added to free square list
            if board[row][column] != ' X' and board[row][column] != ' O':
                free.append(board[row][column])
    #Return free square list if free space list is not empty
    if free != []:
        return free
    #If free square list is empty then a cats game exists, say so and kill program
    else:
        print("Cat's Game!!")
        exit()

def victory_for(board, sign, size):
    # The function analyzes the board status in order to check if
    # the player using 'O's or 'X's has won the game

    #Create empty list of taken squares
    markSpots = []
    #Look through the board for takes squares
    for row in range(0,len(board)):
        for column in range(0,len(board[row])):
            #If square is a sign then it is added to taken square list
            if board[row][column] == sign:
                markSpots.append(coordToNum((row + 1, column + 1), size))
    #Loop to keep count of possible win lists
    for i in range(1,(len(board) * 2) + 2):
        count = 0
        #Assign possible win list to compare variable
        compare = possibleWin(i, size)
        for x in range(0, int(size[0])):
            #Increase count if compare list index is in list of taken squares
            if compare[x] in markSpots:
                count += 1
            #If count reaches same size as possible win list then that is a win
            if count == int(size[0]):
                #Look to see which sign is winner
                if sign == ' O':
                    print("You are the WINNER!!")
                else:
                    print("The Computer beat you!!")
                return True

def draw_move(board, freeSpots, boxes, size):
    #The function draws the computer's move and updates the board.

    #Set allowed to false to create while loop until computer selects free square
    allowed = False
    while not allowed:
        #Assign random square as computers move (Will update later with some AI)
        compMove = randrange(1,boxes + 1)
        #Assign leading zero to computer move if needed
        if compMove <= 9:
            compMove = ('0' + str(compMove))
        else:
            compMove = (str(compMove))
        #Make the move and kill the loop if computer selects free square
        if compMove in freeSpots:
            allowed = True
            coordOfMove = numToCoord(int(compMove), size)
            #Set the free square to X
            board[coordOfMove[0] - 1][coordOfMove[1] - 1] = ' X'
    return board

def makeBoard(boxes, size):
    #The function sets the board squares numeric value

    #Set dimension to the square-root of boxes
    dimension = int(boxes ** 0.5)
    #Create an empyt board list of squares
    board = []
    for i in range(0,dimension):
        #Create empty subset list for the coordinates
        subset = []
        for x in range(0,dimension):
            #Add leading zero to numerical value if needed then add coords to subset list
            if coordToNum((i + 1,x + 1), size) <= 9:
                subset.append('0' + str(coordToNum((i + 1,x + 1),size)))
            else:
                subset.append(str(coordToNum((i + 1,x + 1),size)))
        #Put subset lists into board list
        board.append(subset)
    return board

def coordToNum(argument, size):
    #Dynamic creation of coordinates to Numeric value dictionary

    count = 0
    #Create empty dictionary
    coordNum = {}
    #Get size of each side of board
    size = int(size[0])
    for i in range(1,size + 1):
        for x in range(1,size + 1):
            #Keep count of square
            count += 1
            #Create tuple of squares coordinates
            tuple = (i, x)
            #Add information to the dictionary
            coordNum.update({tuple : count})
    #Return requested dictionary entry
    return coordNum.get(argument, "Error getting coordinate number!")

def numToCoord(argument, size):
    #Dynamic creation of numeric value to coordiantes dictionary

    count = 0
    #Create empty dictionary
    numCoord = {}
    #Get size of each side of the board
    size = int(size[0])
    for i in range(1, size + 1):
        for x in range(1, size + 1):
            #Keep count of squares
            count += 1
            #Create tuple of squares coordinates
            tuple = (i, x)
            #Add information to the dictionary
            numCoord.update({count : tuple})
    #Return requested dictionary entry
    return numCoord.get(argument, "Error getting number coordinate!")

def possibleWin(argument, size):
    #Dynamically creates all possible win combination lists
    count = 0
    countX = 0
    #Create empty list for winning squares in line
    winningSquaresList = []
    #Create empty dictionary of possible win lists
    winCombo = {}
    size = int(size[0])
    #Number of possible win combinations will always be number of
    #side squares * 2 + 2, so use + 3 as range is not inclusive of last value
    for i in range(1, (size * 2) + 3):
        count += 1
        #Keep looping until count is equal to size to create the horizontal winning squares
        if count <= size:
            for x in range(1, size + 1):
                countX += 1
                #Add winning squares list to the winning squares list
                winningSquaresList.append(countX)
            #Add info to the dictionary
            winCombo.update({count : winningSquaresList})
            #Reset the winning squares list so its ready for next list of winning squares
            winningSquaresList = []
            #Reset countX to 1 for use in next portion of winning squares
            countX = 1
        #Loop for verticle winning squares
        elif count > size and count <= size * 2:
            for z in range(1, size + 1):
                winningSquaresList.append(countX)
                countX += size
            #Add info to the dictionary
            winCombo.update({count : winningSquaresList})
            #Set countX so its ready for use in next portion of winning squares
            countX = winningSquaresList[0] + 1
            #Reset winning squares list so its ready for next list of winning squares
            winningSquaresList = []
        #Loop for first diagonal winning Squares
        elif count > size * 2 and count <= ((size * 2) + 1):
            countX = 1
            for y in range(1, size + 1):
                winningSquaresList.append(countX)
                countX += size + 1
            #Add info to the dictionary
            winCombo.update({count : winningSquaresList})
            #Reset winning squares list for use in next list of winning squares
            winningSquaresList = []
        #Loop for second diagonal winning squares
        elif count > ((size * 2) + 1):
            countX = size
            for a in range(1, size + 1):
                winningSquaresList.append(countX)
                countX += (size - 1)
            #Add info to dictionary
            winCombo.update({count : winningSquaresList})
    #Return requested dictionary value
    return winCombo.get(argument, "Error getting possible win lists!")

#Start main program function
main()
