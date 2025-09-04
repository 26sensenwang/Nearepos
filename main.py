import tkinter as tk
import random
import math
from abc import ABC, abstractmethod
import numpy as np
from PIL import Image, ImageTk
import time


class GUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title('Pentago')
        self.piece_size = 60
        
    
    def start_game(self):
        self.draw_board()
        self.root.mainloop()
    
    def draw_board(self):
        self.boardsize = 600
        self.bordersize = 25
        self.arrow_size = 25
        self.mainboard = tk.Canvas(self.root, width = self.boardsize+self.bordersize*2, height = self.boardsize+self.bordersize*2, bg = 'gray')
        self.mainboard.pack()

        img = Image.open("Pentago_quadrant.png").resize((300, 300)) 
        self.quadrant_img = ImageTk.PhotoImage(img)
        img2 = Image.open("white_pentago_piece.png").resize((100,100))
        self.white_piece_img = ImageTk.PhotoImage(img2)
        img3 = Image.open("CW_arrow.webp").resize((self.arrow_size,self.arrow_size))
        self.CW_arrow_img = ImageTk.PhotoImage(img3)
        img4 = Image.open("CCW_arrow.jpg").resize((self.arrow_size,self.arrow_size))
        self.CCW_arrow_img = ImageTk.PhotoImage(img4)
        

        self.mainboard.bind("<Button-1>", self.handle_click)
        '''
        self.mainboard.create_image(self.boardsize*0.25+self.bordersize, self.boardsize*0.25+self.bordersize, image=self.quadrant_img)
        self.mainboard.create_image(self.boardsize*0.75+self.bordersize, self.boardsize*0.25+self.bordersize, image=self.quadrant_img)
        self.mainboard.create_image(self.boardsize*0.25+self.bordersize, self.boardsize*0.75+self.bordersize, image=self.quadrant_img)
        self.mainboard.create_image(self.boardsize*0.75+self.bordersize, self.boardsize*0.75+self.bordersize, image=self.quadrant_img)
        '''
        for i in range(4):
            row = i//2
            col = i%2
            self.mainboard.create_image(self.boardsize*(0.25+0.5*col)+self.bordersize, self.boardsize*(0.25+0.5*row)+self.bordersize, image=self.quadrant_img)
            self.mainboard.create_image(self.bordersize-self.arrow_size*0.5+col*(self.arrow_size+self.boardsize), self.bordersize+self.arrow_size*0.5+row*(self.boardsize-2*self.arrow_size), image=self.CCW_arrow_img)
            self.mainboard.create_image(self.bordersize-self.arrow_size*0.5+col*(self.arrow_size+self.boardsize), self.bordersize+self.arrow_size*1.5+row*(self.boardsize-2*self.arrow_size), image=self.CW_arrow_img)

        
        self.centerdistance = 80
        

    def draw_piece(self, row, col, colour):
        quadrant = [row//3, col//3]
        x = self.bordersize+self.boardsize*0.25+self.boardsize*0.5*quadrant[1] + self.centerdistance*(col-quadrant[1]*3-1)
        y = self.bordersize+self.boardsize*0.25+4+self.boardsize*0.5*quadrant[0] + self.centerdistance*(row-quadrant[0]*3-1)
        if colour == 1:
            self.mainboard.create_image(x, y, image = self.white_piece_img, tags='piece')
        else:
            self.mainboard.create_image(x, y, image = self.CW_arrow_img, tags='piece')
    
    
        
    def draw_grid(self):
        self.mainboard.delete("piece")
        for row in range(6):
            for col in range(6):
                if self.game.board.grid[row][col] != 0:
                    self.draw_piece(row, col, self.game.board.grid[row][col])

                    
                    
        
        

    def rotate(self, quadrant_direction):
        #display animation
        self.draw_grid()

    

    def pixel_to_position(self, x, y):
        position_size = self.boardsize/6
        if self.bordersize <= x < self.boardsize+self.bordersize and self.bordersize <= y < self.boardsize+self.bordersize:
            return [(y-self.bordersize) // position_size, (x-self.bordersize) // position_size, 'P']
        for i in range(4):
            row = i // 2
            col = i % 2
            if self.bordersize-self.arrow_size*1+col*(self.arrow_size+self.boardsize)<= x <= self.bordersize+col*(self.arrow_size+self.boardsize) and self.bordersize+row*(self.boardsize-2*self.arrow_size)<=y < self.bordersize+self.arrow_size+row*(self.boardsize-2*self.arrow_size):
                return [i, 0, 'R']
            elif self.bordersize-self.arrow_size*1+col*(self.arrow_size+self.boardsize)<= x <= self.bordersize+col*(self.arrow_size+self.boardsize) and self.bordersize+self.arrow_size+row*(self.boardsize-2*self.arrow_size) <= y <= self.bordersize+self.arrow_size*2+row*(self.boardsize-2*self.arrow_size):
                return [i, 1, 'R']   
        return [None, None, None]
    


    def handle_click(self, click):
        click_pos = self.pixel_to_position(click.x, click.y)
        if ((self.game.turn == self.game.player1.colour or self.game.turn == self.game.player1.colour*2) and self.game.player1.type == 'human') or ((self.game.turn == self.game.player2.colour or self.game.turn == self.game.player2.colour*2) and self.game.player2.type == 'human'):
            if click_pos[2] == 'P' and abs(self.game.turn) == 1:
                row, col = int(click_pos[0]), int(click_pos[1])
                if self.game.board.grid[row][col] == 0:
                    self.game.board.place(row, col, self.game.turn)
                    self.draw_grid()
                    self.game.turn = 2*self.game.turn
            if self.game.board.check_win(5)!= False:
                print('game ended')
            elif click_pos[2] == 'R' and abs(self.game.turn) == 2:
                self.game.board.rotate(click_pos[0]+4*click_pos[1])
                self.rotate(click_pos[0]+4*click_pos[1])
                self.draw_grid()
                self.game.turn = self.game.turn/-2
                self.game.apply_move(self.game.turn)
            if self.game.board.check_win(5)!= False:
                print('game ended')
    
        
        

class Game:
    def __init__ (self):
        self.turn = 1
        self.board = Board()
        self.player1 = HumanPlayer(1)
        self.player2 = ComputerPlayer(-1)
        self.gui = GUI(self)
        self.gui.start_game()
        '''
        for i in range(10):
            self.apply_move(self.player1.make_move(self.board), 1)
            self.board.display_board()
            self.apply_move(self.player2.make_move(self.board), -1)
            self.board.display_board()
        '''
    
    
    
    def apply_move(self, colour):
        if self.player1.colour == colour and self.player1.type == 'computer':
            move = self.player1.make_move(self.board)
            self.board.place(move[0], move[1], colour)
            self.gui.draw_grid()
            time.sleep(0.3)
            self.board.rotate(move[2])
            self.gui.rotate(move[2])
            self.gui.draw_grid()
            self.turn = -self.turn
            if self.board.check_win(5)!= False:
                print('game ended')

        elif self.player2.colour == colour and self.player2.type == 'computer':
            move = self.player2.make_move(self.board)
            self.board.place(move[0], move[1], colour)
            self.gui.draw_grid()
            self.board.rotate(move[2])
            self.gui.rotate(move[2])
            self.gui.draw_grid()
            self.turn = -self.turn
            if self.board.check_win(5)!= False:
                print('game ended')
            


class Player(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def make_move(self):
        pass
        

class HumanPlayer(Player):
    def __init__(self, colour):
        self.colour = colour
        self.type = 'human'

    def make_move(self, board):
        pass


class ComputerPlayer(Player):
    def __init__(self, colour):
        self.colour = colour
        self.type = 'computer'
    
    def make_move(self, board):
        lmove = self.minimax(board, 1, self.colour, -1000000000000000, 1000000000000000)
        print(lmove[0])
        return lmove[1]


    def minimax(self, board, depth, colour, alpha, beta): 
        if depth == 0:
            return [board.evaluate()]
        
        bestscore = -1000000000*colour

        for move in board.get_moves():
            newboard = board.copy_board()
            newboard.place(move[0], move[1], colour)
            '''
            win = newboard.check_win(5)
            if win != False: 
                return [win*10000, move]
            '''
            newboard.rotate(move[2])
            win = newboard.check_win(5)
            if win != False:
                if win == colour:
                    return [win*10000, move]
                elif win == 0:
                    bestscore = 0
                    bestmove = move
                else:
                    continue
            result = self.minimax(newboard, depth-1, -colour, alpha, beta)[0]
            if bestscore*colour < result*colour:
                bestscore = result #*colour
                bestmove = move
                samemoves = 1
            elif bestscore == result:
                samemoves += 1
                
                if random.randint(1,samemoves) == 1:
                    bestmove = move
            if colour == 1:
                alpha = max(alpha, bestscore)
            else:
                beta = min(beta, bestscore)
            if beta <= alpha:
                break
            
        return [bestscore, bestmove]

    
        

class Board:
    def __init__(self):
        #self.grid = [[0 for i in range(6)] for i in range(6)]
        self.grid = (
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0])
        
        
    def display_board(self):
        for i in self.grid:
            print(i)
            
    
    def copy_board(self):
        newboard = Board()
        newboard.grid = [row[:] for row in self.grid]
        return newboard

    def place(self, row, col, colour):
        self.grid[row][col] = colour

    def rotate(self, quadrant_direction):
        quadrant = quadrant_direction % 4
        direction = quadrant_direction // 4
        center = [1 + quadrant // 2 * 3, 1 + quadrant % 2 * 3]
        newgrid = [row[:] for row in self.grid]
        if direction == 0:
            for i in range(3):
                for j in range(3):
                    newgrid[center[0]-1+j][center[1]-1+i] = self.grid[center[0]-1+i][center[1]+1-j]
        else:
            for i in range(3):
                for j in range(3):
                    newgrid[center[0]-1+j][center[1]-1+i] = self.grid[center[0]+1-i][center[1]-1+j]
        self.grid = [row[:] for row in newgrid]

        

    def get_moves(self):
        moves = []
        for i in range(6):
            for j in range(6):
                if self.grid[i][j] == 0:
                    for k in range(8):
                        moves.append([i, j, k])
        return moves


    def check_win(self, connected):
        win = 0
        ended = False
        for i in range(6):
            if abs(sum(self.grid[i][:5])) == connected or abs(sum(self.grid[i][1:])) == connected:
                win = self.grid[i][1] 
                ended = True
            elif abs(sum([row[i] for row in self.grid[:5]])) == connected or abs(sum([row[i] for row in self.grid[1:]])) == connected:
                win = self.grid[1][i]
                ended = True
                
        if abs(sum([self.grid[i][i] for i in range(5)])) == connected or abs(sum([self.grid[i][i] for i in range(1,6)])) == connected:
            win += self.grid[1][1]
            ended = True
        elif abs(sum([self.grid[i][-i-1] for i in range(5)])) == connected or abs(sum([self.grid[i][-i-1] for i in range(1,6)])) == connected:
            win += self.grid[1][4]
            ended = True
        elif abs(sum([self.grid[i][i+1] for i in range(5)])) == connected:
            win += self.grid[0][1]
            ended = True
        elif abs(sum([self.grid[i+1][i] for i in range(5)])) == connected:
            win += self.grid[1][0]
            ended = True
        elif abs(sum([self.grid[i][-i-2] for i in range(5)])) == connected:
            win += self.grid[0][4]
            ended = True
        elif abs(sum([self.grid[i+1][-i-1] for i in range(5)])) == connected:
            win += self.grid[1][5]
            ended = True
        if ended:
            return win
        else:
            return False
 
    def find_potentials(self, array):
        output = [0,0,0,0,0,0,0,0]
        for length in range(1,5):
            if sum(array) == length and -1 not in array:
                output[(length-1)*2] = 1
            if sum(array) == -length and 1 not in array:
                output[(length-1)*2+1] = 1
        return output
    
    
    def calculate_score(self, board):
        
        weights = [10,-10,30,-30,80,-80, 200, -200]

        score = 0
        for i in range(6):
            score += np.dot(weights, self.find_potentials(board[i][:5]))
            score += np.dot(weights, self.find_potentials(board[i][1:]))
            score += np.dot(weights, self.find_potentials([row[i] for row in board[:5]]))
            score += np.dot(weights, self.find_potentials([row[i] for row in board[1:]]))

        score += np.dot(weights, self.find_potentials([self.grid[i][i] for i in range(5)]))
        score += np.dot(weights, self.find_potentials([self.grid[i][i] for i in range(1, 6)]))
        score += np.dot(weights, self.find_potentials([self.grid[i][-i-1] for i in range(5)]))
        score += np.dot(weights, self.find_potentials([self.grid[i][-i-1] for i in range(1, 6)]))
        score += np.dot(weights, self.find_potentials([self.grid[i][i+1] for i in range(5)]))
        score += np.dot(weights, self.find_potentials([self.grid[i+1][i] for i in range(5)]))
        score += np.dot(weights, self.find_potentials([self.grid[i][-i-2] for i in range(5)]))
        score += np.dot(weights, self.find_potentials([self.grid[i+1][-i-1] for i in range(5)]))
        
        return score
        
    def evaluate(self):
        is_won = self.check_win(5)
        if is_won != False:
            return is_won*1000000
        score = 0
        score += 2*self.calculate_score(self.grid)
        for direction in range(8):
            newboard = self.copy_board()
            newboard.rotate(direction)
            score += self.calculate_score(newboard.grid)
            
        return score
        
        
class Menu:
    pass
if __name__ == '__main__':
    Game()
