# AARON SMITH
# CREATED DEC 2023, UPDATED AUG 2025

import pygame as pg
import constants as cs
import numpy as np
import time as time





class Board:

    def __init__(self) -> None:
        '''
        initializes the board as a 5x5 matrix, or list of list with None's'''
        self.board = [[None for i in range(5)] for i in range(5)]

    def giveboard(self) -> list:
        '''
        returns the board list to be read and usable

        
        parameters: None
        returns: list
        '''
        return self.board
    
    def printBoard(self) -> None:
        '''
        prints a visual representation of the board in the console
        
        parameters: self
        return: None
        '''
        for i in self.board:          #loops through board and prints in terminal
            for j in i:        
                if j:                 #place a 'O' if the spot is empty or print the players' pieces
                    print(j, end = ' ')
                else:
                    print('O',end=' ')
            print()

    def setPiece(self, player, i, j) -> None:
        '''

        set up a piece on the board with specific player


        parameters: the player and location
        return: None
        '''
        try:    
            self.board[i][j] = player
        except:
            pass


def checkfour(lst, i, j) -> bool:
    '''
    Checks for four of the same pieces in a row
    
    parameters: a list of the current player's piece position, and their current move position
    
    return: bool, True for four in a row
    
    '''
    #right 3
    if [i, j+1] in lst and [i, j+2] in lst and [i,j+3] in lst:
        return True
    #left 3
    if [i, j-1] in lst and [i, j-2] in lst and [i,j-3] in lst:
        return True
    #up three
    if [i+1, j] in lst and [i+2,j] in lst and [i+3, j] in lst:
        return True
    #down three
    if [i-1, j] in lst and [i-2, j] in lst and [i-3, j] in lst:
        return True
    #diag up right three
    if [i+1,j+1] in lst and [i+2,j+2] in lst and [i+3,j+3] in lst:
        return True
    #diag down right three
    if [i-1, j+1] in lst and [i-2, j+2] in lst and [i-3, j+3] in lst:
        return True
    #diag up left three
    if [i+1,j-1] in lst and [i+2, j-2] in lst and [i+3,j-3] in lst:
        return True
    #diag down left three
    if [i-1, j-1] in lst and [i-2,j-2] in lst and [i-3,j-3] in lst:
        return True
    return False

def checksquare(lst, i, j):
    #up right 
    if [i-1,j] in lst and [i-1, j+1] in lst and [i,j+1] in lst:
        #print('up right')
        return True
    #down right
    if [i,j+1] in lst and [i+1,j] in lst and [i+1,j+1] in lst:
        #print('down right')
        return True
    #up left
    if [i-1, j] in lst and [i-1,j-1] in lst and [i,j-1] in lst:
        #print('up left')
        return True
    #down left
    if [i, j-1] in lst and [i+1, j-1] in lst and [i+1, j] in lst:
        #print('down left')
        return True
    return False

def checkwin(player, gameboard) -> bool:
    '''
    checks a certain player's pieces to see if they have won

    by getting the player's current pieces and calling the checkfour function
    
    parameters: the current player and the gameboard
    
    return: bool, True for win
    '''
    playerspaces = []                     #creates a list of all the current player's piece positions
    for i in range(len(gameboard.giveboard())): 
        for j in range(len(gameboard.giveboard()[i])):
            if gameboard.giveboard()[i][j] == player:
                playerspaces.append([i, j])





    for i in playerspaces:                 #checks for 8 possible four in a rows for every piece
        i,j = i[0], i[1]
        if checkfour(playerspaces,i,j):
            return True
        if checksquare(playerspaces,i,j):
            return True
    return False
def check_full(gameboard) -> bool:
    '''
    checks if all the pieces have been placed
    
    parameters: the gameboard
    
    return: bool
    '''

    count = 0
    for i in gameboard:
        for j in i:
            if j:
                count += 1

            

       
    if count >= 8:

        return True
    return False


def get_index(position, lst):

    """
    gets the index of a position from the pygame cursor position
    
    note, if the click is not in a cirle, return none
    
    return: index or none
    
    """

    x, y = position           

    for i in lst:                                  #checks every possible circle and returns the index if a click is inside one
        a, b = i
        if (x-a) ** 2 + (y-b) ** 2 <= 1600:

            return int((a - 60) / 120), int((b - 60) / 120)
        



def create_list_of_index(filename) -> list:

    """
    creates a list of the space postions
    
    parameters: name of file with the positions
    
    return: list of the spaces
    
    """

    lst = []
    myfile = open(filename, 'r')                 #opens file with the parameter as its name
    for line in myfile:                          #reads through the lines of the file
        linelist = line.split()
        lst.append((int(linelist[0]), int(linelist[1])))    #adds the file's data into a list
    myfile.close()
    return lst
def draw_x(win, position, color) -> None:


    """
    draws the crosses between spaces

    parameters:pygame window, position, and line color
    
    return: None
    
    """
    x,y = position

    length = int(np.sqrt(2) * 120) / 2        #length of the diagonal and divides by two because drawing starts in at the midpoint

    for i in range(int(length)):

        pg.draw.circle(win, color, (x-i,y-i), 5)      #goes out from center in each diagonal direction and draws a line 
        pg.draw.circle(win, color, (x-i,y+i), 5)
        pg.draw.circle(win, color, (x+i,y-i), 5)
        pg.draw.circle(win, color, (x+i,y+i), 5)
def get_moves(player, i, j, gameboard) -> list:
    
    """
    gets the possible moves for a selected piece

    based on the 8 possible locations surrounding a piece

    parameters: current player, position index, and gameboard

    return: list of possible moves
    
    """
    moves = []
    moves.append((i,j))
    lst = gameboard.giveboard()
    for n in range(-1, 2):
        for m in range(-1, 2): 
            if n == 0 and m == 0:              #already appended the initial point
                continue
            if i + n < 0 or j + m <0:          #ignore negative indecies
                continue
            try:                               #if the index is valid (not out of the range of the list) and the space is empty, appened the index to the possible moves list
                if lst[i+n][j+m] is None :
                    moves.append((i+n,j+m))
            except:
                pass
    return moves
def main():

    gameboard = Board()                            #initialize the board and pygame
    moves = []
    pg.init()

    count = True
    moving = False                                 #initialize changing booleans 
    winner=False
    running = True
    black = True

    board_color = cs.TAN                           #sets defualt board color to tan
    dark_board_color = cs.DARK_TAN

    win = pg.display.set_mode((600,610))           #sets game window to 600x600
    intro = True
    intro_image = pg.image.load('TeekO.png')       #loads the intro screen
    pg.display.set_caption("Teeko")                #sets the game caption 




    while running:   
            
        if not winner:                         #show the current player's color at the bottom of the screen

            
            if black:

                pg.draw.rect(win, cs.BLACK, pg.Rect(0,600,600,10),border_top_left_radius=5,border_top_right_radius=5)

            else:

                pg.draw.rect(win, cs.RED, pg.Rect(0,600,600,10),border_top_left_radius=5,border_top_right_radius=5)
    
        if intro:                               #creates the intro screen
            count = True

            win.fill(cs.WHITE)
            win.blit(intro_image, (0,0))
            colors = [cs.TAN, cs.SAGE_GREEN, cs.LIGHT_BLUE, cs.PINK, cs.LAVENDER, cs.CORAL]       #board color selection
            
            
            for n in range(3):                                                                    #draws board color selections
                set_color = colors[n]
                displacement = n * 80 
                pg.draw.rect(win, cs.BLACK, pg.Rect(340+displacement-3,427, 66,66),border_top_left_radius=10,border_bottom_right_radius=10,border_bottom_left_radius=10,border_top_right_radius=10)        #rounded corners
                pg.draw.rect(win, set_color, pg.Rect(340+displacement,430, 60,60),border_top_left_radius=10,border_bottom_right_radius=10,border_bottom_left_radius=10,border_top_right_radius=10)

            for n in range(3,6):                                                                  #second row of color selection
                set_color = colors[n]
                displacement = (n-3) * 80                                                         #'reset' displacement
                pg.draw.rect(win, cs.BLACK, pg.Rect(340+displacement-3,507, 66,66),border_top_left_radius=10,border_bottom_right_radius=10,border_bottom_left_radius=10,border_top_right_radius=10)
                pg.draw.rect(win, set_color, pg.Rect(340+displacement,510, 60,60),border_top_left_radius=10,border_bottom_right_radius=10,border_bottom_left_radius=10,border_top_right_radius=10)
            pg.display.update()
            for event in pg.event.get():                                #pygame event list, contains the user's actions

                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:                            #end game if they hit esc, start game if they hit enter
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_RETURN:
                        intro = False
                    else:
                        pass

                if event.type == pg.MOUSEBUTTONDOWN:                    #change the board color if they click on a color square
                    color_test = win.get_at(pg.mouse.get_pos())
                    if color_test in colors:
                        board_color = color_test
                        dark_board_color = tuple([i-60 for i in board_color])
                                                         #'reset' displacement
                        
                        intro = False
                        
        else:

            
            if count:                                                    #creates the boards gridlines only once as to not draw over new moves
                
                win.fill(board_color)

                for i in range(60,600,120):                    
                        for j in range(60,541):                
                            pg.draw.circle(win, dark_board_color, (i,j), 5)
                            pg.draw.circle(win, dark_board_color, (j,i), 5)

                for i in range(1,5):
                    for j in range(1,5):
                        position = i * 120, j * 120
                        draw_x(win, position, dark_board_color)                  #draws the board
              
                for i in range(5):                                               #draws the spaces
                    for j in range(5):
                        x, y = 60 + 120 * i, 60 + 120 * j
                        pg.draw.circle(win, board_color, (x,y), 47)
                        pg.draw.circle(win, cs.BLACK, (x,y), 45)
                        pg.draw.circle(win, cs.WHITE, (x,y), 40)
                count = False
            pg.display.update()
         
         
            if not(winner):


                for event in pg.event.get():
                    if event.type == pg.QUIT:                                              #end game if escape key is pressed or quit is clicked
                        running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            running = False
                    if event.type == pg.MOUSEBUTTONDOWN:                                   #if a user clicks on the board, find where they clicked on the board


                        position = pg.mouse.get_pos()
                        if get_index(position, create_list_of_index('standards.txt')):     #if click is inside a circle, not whitespace
                            if not(check_full(gameboard.giveboard())):                     #drop gameplay
                                if black:                                                  #sets the player color and string according to whose turn it is
                                    color2 = cs.GREY
                                    color1 = cs.DARK_GREY
                                    player = 'B'
                                else:
                                    color2 = cs.RED
                                    color1 = cs.DARK_RED
                                    player = 'R'
                                j,i = get_index(position, create_list_of_index('standards.txt'))
                                if gameboard.giveboard()[i][j] is None:         #if the player clicked on an empty space...
                                    #print('test')
                                    gameboard.setPiece(player, i, j)            #set their piece on the gameboard
                                    position = x,y = j * 120 + 60, i * 120 + 60
                                    up_position = x,y-5 
                                    pg.draw.circle(win, color1, position, 40)   #draw their piece on the space
                                    pg.draw.circle(win, color2, up_position, 40)
                                    pg.display.update()
                                    black = not(black)                           #change active player
                                    winner = checkwin(player, gameboard)         #check for four in a row
                                    #if winner:
                                        #print("Winner")
                                    #gameboard.printBoard()
                            else:                                                 #once the 'drop' is over...
                            
                                j, i = get_index(position, create_list_of_index('standards.txt'))
                                position = x,y = j * 120 + 60, i * 120 + 60       
                                up_position = x,y-5 
                                if black:
                                    color2 = cs.GREY
                                    color1 = cs.DARK_GREY
                                    player = 'B'
                                else:
                                    color2 = cs.RED
                                    color1 = cs.DARK_RED
                                    player = 'R'
                                if not(moving):          #if they have not yet picked a piece to move, activate what they clicked on
                                    if gameboard.giveboard()[i][j] == player:
                                        currenti, currentj = i, j
                                        holdi, holdj = i, j
                                        moves = get_moves(player, i, j, gameboard)
                                        for i in moves:           #mark the possible moves for the player's piece
                                            if i == (holdi, holdj):
                                                continue
                                            y1,x1 = i
                                            new_position = x1 * 120 + 60, y1 * 120 + 60
                                            pg.draw.circle(win, (50,50,50), new_position, 10)    #creates a 'gradient' of circles on a possible move space
                                            pg.draw.circle(win, (100,100,100), new_position, 8)
                                            pg.draw.circle(win, (150,150,150), new_position, 6)
                                            pg.draw.circle(win, (200,200,200), new_position, 4)
                                            pg.draw.circle(win, (250,250,250), new_position, 2)
                                        pg.display.update()
                                        moving = True
                                        if len(moves) == 0:
                                            moving = False
                                else:                                #once they clicked on a piece...
                                    if len(moves) != 0:  
                                                                        #if they clicked on a possible move...
                                        if (i,j) in moves:
                                            hold2i, hold2j = i, j
                                            position =x,y= j * 120 + 60, i * 120 + 60
                                            up_position= x, y-5
                                            gameboard.setPiece(None, currenti, currentj)
                                            gameboard.setPiece(player, i, j)     #reset old piece's position
                                            #print(currenti,currentj)
                                            currentposition = currentx,currenty = currentj * 120 + 60, currenti * 120 + 60
                                            currentpositionup = currentx, currenty - 5
                                            pg.draw.circle(win, board_color, currentposition, 47)
                                            pg.draw.circle(win, cs.BLACK, currentposition, 45)
                                            pg.draw.circle(win, cs.WHITE, currentposition, 40)
                                            #print(currentposition)
                                            pg.display.update()
                                            for i in moves:                        #remove the possible moves markers
                                                y1,x1 = i
                                                new_position = x1 * 120 + 60, y1 * 120 + 60
                                                pg.draw.circle(win, cs.WHITE, new_position, 10)
                                            for l in range(len(moves)):            #reset possible moves
                                                moves.pop()
                                            pg.draw.circle(win, color1, position, 40)
                                            pg.draw.circle(win, color2, up_position, 40)
                                            pg.display.update()
                                            #gameboard.printBoard()
                                            if (hold2i,hold2j) != (holdi,holdj):   #only swaps player if the new space is not where the piece already is
                                                black = not(black)
                                            winner = checkwin(player, gameboard)
                                            
                                            moving = False
                pg.display.update()
            else:                                       #once there is a winner...
                time.sleep(0.5)                         #slight delay after someone wins, improves game feel
                running = False
                if black:       #after a win the color changes again, so we must revert back to find the actual winner then use that information to display the winning screen appropriately
                    winner_string = "Red"
                    winner_color = cs.RED
                else:
                    winner_string = "Black"
                    winner_color = cs.BLACK
                pg.draw.rect(win, cs.BLACK, pg.Rect(win.get_size()[0]/2 - 155,win.get_height()/2 - 80,310,160),0, 15)
                pg.draw.rect(win, cs.WHITE, pg.Rect(win.get_size()[0]/2 - 150,win.get_height()/2 - 75,300,150),0, 15)
                target_rect = pg.Rect(win.get_size()[0]/2 - 250/2,win.get_height()/2 - 50,250,100)
                font = pg.font.Font(None, 30)
                text = winner_string + " wins!"
                text_surface = font.render(text, True, winner_color)
                text_rect = text_surface.get_rect(center=target_rect.center)
                win.blit(text_surface,text_rect)
                
                pg.display.update()
                time.sleep(5)
pencolor = main()

pg.quit()







