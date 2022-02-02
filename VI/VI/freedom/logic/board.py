from multiprocessing.dummy import current_process
import random
import math
import copy
import pdb
from freedom.logic.field import Field


class Board:
    size = 10
    WHITE_COLOR = 'white'
    BLACK_COLOR = 'black'
    scores_black = {
            "five_or_more" : -100,
            "four" : 3000,
            "three" : 300,
            "two" : 5
        }
    scores_white = {
            "five_or_more" : 100,
            "four" : -3500,
            "three" : -300,
            "two" : -5
        }
    def __init__(self,player):
        self.whiteOnMove = True
        self.matrix = []
        self.populate_matrix()
        self.choose_player(player)
        self.last_move_played = None
        self.moves_played = 0
        self.lastMove = False
        self.computer_not_play_last_move = False
        #self.start_depth = 5
    def __str__(self):
        return f'Current player:{self.return_player_color()},last_move_played:{self.last_move_played},moves_played:{self.moves_played}'
    def populate_matrix(self):
        for i in range(0,self.size):
            self.matrix.append([])
            for j in range(0,self.size):
                self.matrix[i].append(Field(i*10 + j))
    def is_field_free(self,i,j):
        return self.matrix[i][j].empty
    def choose_player(self,player):
        if player == 'igrac':
            self.is_computer = False
        else:
            self.is_computer = True
            if player == 'laki':
                self.computer_level = 1
                self.start_depth = 4
            elif player == 'srednji':
                self.computer_level = 2
                self.start_depth = 5
            else:
                self.computer_level = 3
                self.start_depth = 6
    def set_field_used(self,i,j):
        self.matrix[i][j].empty = False
        if self.whiteOnMove:
            self.matrix[i][j].isWhiteColor = True
        self.whiteOnMove = not self.whiteOnMove
        self.moves_played+=1
        if self.moves_played == (self.size * self.size) - 1:
            self.lastMove = True
            return True
        return False
    def game_has_finished(self):
        return (self.size * self.size) == self.moves_played
    def create_already_used_matrix(self):
       arr = [[False for i in range(self.size)] for j in range(self.size)]
       return arr

    # proverava da li je indeks unutar definisanih granica
    def is_valid_index(self,i,j):
        return (i >= 0 and i < self.size) and (j >= 0 and j < self.size)
    def can_computer_play(self,i,j):
        return self.is_valid_index(i,j) and self.matrix[i][j].is_empty()
    def return_player_color(self):
        if self.whiteOnMove:
            return self.WHITE_COLOR
        return self.BLACK_COLOR

    def calculate_points(self,color):
        points = 0
        used_fields = []

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j].is_empty():
                    continue
                if self.matrix[i][j].checkForCollor(color):
                    if i-3 >=0 and j-3>=0 and self.matrix[i-3][j-3].checkForCollor(color) \
                        and self.matrix[i-2][j-2].checkForCollor(color) and self.matrix[i-1][j-1].checkForCollor(color) \
                            and not ([self.matrix[i-3][j-3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if i - 4 >= 0  and j - 4 >= 0 and self.matrix[i-4][j-4].checkForCollor(color):
                            valid_current = False
                        if i + 1 < self.size and j + 1 < self.size and self.matrix[i+1][j+1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i-3][j-3].code,self.matrix[i][j].code]))
                            points +=1
                    if i-3 >=0 and self.matrix[i-3][j].checkForCollor(color) \
                        and self.matrix[i-2][j].checkForCollor(color) and self.matrix[i-1][j].checkForCollor(color) \
                            and not ([self.matrix[i-3][j].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if i - 4 >= 0 and self.matrix[i-4][j].checkForCollor(color):
                            valid_current = False
                        if i + 1 < self.size and self.matrix[i+1][j].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i-3][j].code,self.matrix[i][j].code]))
                            points +=1
                    if i-3 >=0 and j+3<self.size and self.matrix[i-3][j+3].checkForCollor(color) \
                        and self.matrix[i-2][j+2].checkForCollor(color) and self.matrix[i-1][j+1].checkForCollor(color) \
                            and not ([self.matrix[i-3][j+3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if i - 4 >= 0  and j + 4 < self.size and self.matrix[i-4][j+4].checkForCollor(color):
                            valid_current = False
                        if i + 1 < self.size and j - 1 >= 0 and self.matrix[i+1][j-1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i-3][j+3].code,self.matrix[i][j].code]))
                            points +=1
                    if  j-3>=0 and self.matrix[i][j-3].checkForCollor(color) \
                        and self.matrix[i][j-2].checkForCollor(color) and self.matrix[i][j-1].checkForCollor(color) \
                            and not ([self.matrix[i][j-3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if   j - 4 >= 0 and self.matrix[i][j-4].checkForCollor(color):
                            valid_current = False
                        if  j + 1 < self.size and self.matrix[i][j+1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i][j-3].code,self.matrix[i][j].code]))
                            points +=1
                    if  j+3<self.size and self.matrix[i][j+3].checkForCollor(color) \
                        and self.matrix[i][j+2].checkForCollor(color) and self.matrix[i][j+1].checkForCollor(color) \
                            and not ([self.matrix[i][j+3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if  j + 4 < self.size and self.matrix[i][j+4].checkForCollor(color):
                            valid_current = False
                        if  j - 1 >= 0 and self.matrix[i][j-1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i][j+3].code,self.matrix[i][j].code]))
                            points +=1
                    if i+3 <self.size and j-3>=0 and self.matrix[i+3][j-3].checkForCollor(color) \
                        and self.matrix[i+2][j-2].checkForCollor(color) and self.matrix[i+1][j-1].checkForCollor(color) \
                            and not ([self.matrix[i+3][j-3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if i + 4 < self.size and j - 4 >= 0 and self.matrix[i+4][j-4].checkForCollor(color):
                            valid_current = False
                        if i - 1 >= 0 and j + 1 < self.size and self.matrix[i-1][j+1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i+3][j-3].code,self.matrix[i][j].code]))
                            points +=1
                    if i+3 <self.size  and self.matrix[i+3][j].checkForCollor(color) \
                        and self.matrix[i+2][j].checkForCollor(color) and self.matrix[i+1][j].checkForCollor(color) \
                            and not ([self.matrix[i+3][j].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        
                        if i + 4 < self.size and self.matrix[i+4][j].checkForCollor(color):
                            valid_current = False
                        if i - 1 >= 0 and self.matrix[i-1][j].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i+3][j].code,self.matrix[i][j].code]))
                            points +=1
                    if i+3 <self.size and j+3 <self.size and self.matrix[i+3][j+3].checkForCollor(color) \
                        and self.matrix[i+2][j+2].checkForCollor(color) and self.matrix[i+1][j+1].checkForCollor(color) \
                            and not ([self.matrix[i+3][j+3].code,self.matrix[i][j].code] in used_fields):
                        valid_current = True
                        if i + 4 < self.size  and j + 4 < self.size and self.matrix[i+4][j+4].checkForCollor(color):
                            valid_current = False
                        if i - 1 >= 0 and j - 1 >= 0 and self.matrix[i-1][j-1].checkForCollor(color):
                            valid_current = False
                        if valid_current:
                            used_fields.append(sorted([self.matrix[i+3][j+3].code,self.matrix[i][j].code]))
                            points +=1
        return [points,used_fields]

    def calculate_winner(self):
        white_points,white_arr = self.calculate_points('white')
        black_points,black_arr = self.calculate_points('black')
        return [white_points,white_arr,black_points,black_arr]

    def is_valid_move(self,new_i,new_j):
        #print("Last move played",self.last_move_played)
        if self.last_move_played is None:
            self.last_move_played = [new_i,new_j]
            return True
        i , j =self.last_move_played
        valid_moves_to_play = []
        if i - 1 >= 0 and j - 1 >= 0:
            valid_moves_to_play.append([i-1,j-1])
        if i - 1 >= 0:
            valid_moves_to_play.append([i-1,j])
        if i - 1 >= 0 and j + 1 < self.size:
            valid_moves_to_play.append([i-1,j+1])
        if  j - 1 >= 0:
            valid_moves_to_play.append([i,j-1])
        if  j + 1 < self.size:
            valid_moves_to_play.append([i,j+1])
        if i + 1 < self.size and j - 1 >= 0:
            valid_moves_to_play.append([i+1,j-1])
        if i + 1 < self.size:
            valid_moves_to_play.append([i+1,j])
        if i + 1 < self.size and j + 1 < self.size:
            valid_moves_to_play.append([i+1,j+1])
        valid_moves_to_play = list(filter(lambda el: self.is_field_free(el[0],el[1]),valid_moves_to_play))
        if len(valid_moves_to_play) == 0 or [new_i,new_j] in valid_moves_to_play:
            self.last_move_played = [new_i,new_j] # postavljamo ko je odigrao novi potez
            return True
        return False

    # funkcija za pribavljanje svih slobodnih polja oko trenutnog polja
    def get_free_fields(self,i,j):
        arr = []
        i -= 1
        j -= 1
        for n in range(3):
            curr_i = i+n
            for m in range(3):
                curr_j = j + m
                if self.can_computer_play(curr_i,curr_j):
                    arr.append([curr_i,curr_j])
        return arr
    def get_all_free_fields_on_board(self):
        arr = []
        for i in range(0,self.size):
            for j in range(0,self.size):
                if self.matrix[i][j].is_empty():
                    arr.append([i,j])
        return arr

    # valid moves from which computer can choose
    def moves_for_computer(self,i,j):
        valid_computer_moves = self.get_free_fields(i,j)
        if not valid_computer_moves:
            valid_computer_moves = self.get_all_free_fields_on_board()
        return valid_computer_moves

    #funkcija koja odigrava potez kompjutera na random nacin
    def play_move_random(self,i,j):
        valid_computer_moves = self.get_free_fields(i,j)

        # ako ne postoji potez koji trenutno crni moze da odigra
        if not valid_computer_moves:
            valid_computer_moves = self.get_all_free_fields_on_board()
        random_i, random_j = random.choice(valid_computer_moves) 
 
        self.set_field_used(random_i,random_j)
        self.last_move_played = [random_i,random_j]
        
        return [random_i,random_j]
    
    # computer to play serious moves
    def play_move_minimax(self,i,j):
        valid_computer_moves = self.get_free_fields(i,j)

        # ako ne postoji potez koji trenutno crni moze da odigra
        if not valid_computer_moves:
            valid_computer_moves = self.get_all_free_fields_on_board()
        
        min_max_result = self._minimax(self,False,self.start_depth)
        print(min_max_result)
        if self.lastMove:
            current_score = self.evalute_board_state()
            if  current_score > min_max_result[0]:
                return []
        #print(f'Minmax result:{min_max_result}')
        move_i,move_j = min_max_result[1]
        self.set_field_used(move_i,move_j)
        self.last_move_played = [move_i,move_j]

        return [move_i,move_j]
    
    def check_color_and_field_not_empty(self,i,j,color):
        return self.is_valid_index(i,j) and (not self.matrix[i][j].is_empty()) and (self.matrix[i][j].getColor() == color)

    # finding k or more fields in a row(2,3,4,5,6,7,8,9,10)
    def find_k_or_more_in_row(self,color,used_fields_set,num_of_fields):
        total_num_of_k_fields = 0
        konstanta = num_of_fields - 1 # ako trazimo za 5 polja u nizu konstanta ce biti 4
        for i in range(self.size):
            for j in range(self.size):
                code = i * 10 + j
                if self.matrix[i][j].is_empty() or self.matrix[i][j].getColor()!=color or code in used_fields_set:
                    continue
                # 1 slucaj
                if self.is_valid_index(i-konstanta,j-konstanta):
                    arr = []
                    n = i - konstanta
                    m = j - konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        n+=1
                        m+=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i - konstanta
                    m = j - konstanta
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 2 slucaj
                if self.is_valid_index(i-konstanta,j):
                    arr = []
                    n = i - konstanta
                    m = j
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        n+=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i - konstanta
                    m = j
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 3 slucaj   
                if self.is_valid_index(i-konstanta,j+konstanta):
                    arr = []
                    n = i - konstanta
                    m = j + konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        n+=1
                        m-=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i - konstanta
                    m = j + konstanta
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 4 slucaj
                if self.is_valid_index(i,j-konstanta):
                    arr = []
                    n = i
                    m = j - konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        m+=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i
                    m = j - konstanta
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 5 slucaj
                if self.is_valid_index(i,j+konstanta):
                    arr = []
                    n = i
                    m = j + konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        m-=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i
                    m = j + konstanta
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 6 slucaj
                if self.is_valid_index(i+konstanta,j-konstanta):
                    arr = []
                    n = i + konstanta
                    m = j - konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        n-=1
                        m+=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i + konstanta
                    m = j - konstanta
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 7 slucaj
                if self.is_valid_index(i+konstanta,j):
                    arr = []
                    n = i + konstanta
                    m = j
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        n-=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i + konstanta
                    m = j
                    arr.append(n*10 + m)
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
                # 8 slucaj
                if self.is_valid_index(i+konstanta,j+konstanta):
                    arr = []
                    n = i + konstanta
                    m = j + konstanta
                    count = 0
                    while self.check_color_and_field_not_empty(n,m,color) and count != konstanta:
                        m+=1
                        count+=1
                        arr.append(n*10 + m)
                    n = i + konstanta
                    m = j + konstanta
                    arr.append(n*10 + m)                   
                    if count == konstanta:
                        total_num_of_k_fields += 1
                        used_fields_set.update(arr)
        return total_num_of_k_fields
    
    # get arr [0,0,1,1,0,0,1,1,1,0] where each index represents number of conntected fields
    def get_k_in_a_row_fields(self,color):
        used_fields_set = set()
        k_in_row_fields = []
        for k in range(10,1,-1):
            k_in_row_fields.append(self.find_k_or_more_in_row(color,used_fields_set,k))
        return k_in_row_fields

    def calculate_score_from_arr_black(self,arr) -> int:
        greater_than_five_sum = sum(arr[0:6]) 
        four_in_row = arr[6]
        three_in_row = arr[7]
        two_in_row = arr[8]
        total_score = self.scores_black["five_or_more"] * greater_than_five_sum + four_in_row * self.scores_black["four"] + \
            three_in_row * self.scores_black["three"] + two_in_row * self.scores_black["two"]
        return total_score
    def calculate_score_from_arr_white(self,arr) -> int:
        greater_than_five_sum = sum(arr[0:6]) 
        four_in_row = arr[6]
        three_in_row = arr[7]
        two_in_row = arr[8]
        total_score = self.scores_white["five_or_more"] * greater_than_five_sum + four_in_row * self.scores_white["four"] + \
            three_in_row * self.scores_white["three"] + two_in_row * self.scores_white["two"]
        return total_score
        
    def _minimax(self, board, player: bool, depth:int,alpha: float=-math.inf, beta: float=math.inf):
        # osnovni slucaj 
        # pdb.set_trace()
        if depth == 0 or board.game_has_finished():
            current_board_score = board.evalute_board_state()
            print(f'Current board score #{current_board_score}')
            return [current_board_score,None]
        
        i,j = board.last_move_played
        valid_computer_moves = board.moves_for_computer(i,j)
        #print(valid_computer_moves)
        if not board.whiteOnMove:
            maxScore, bestMove = -math.inf,None
            for move in valid_computer_moves:
                new_board = copy.deepcopy(board)
                new_board.set_field_used(move[0],move[1])
                new_board.last_move_played = [move[0],move[1]]
                score = new_board._minimax(new_board,not player,depth-1,alpha,beta)
                alpha = max(alpha,score[0])
                if score[0] >= maxScore:
                    maxScore = score[0]
                    bestMove = move
                if beta <= alpha:
                    print("Breaking MAX score")
                    break
                
            #print(f'Max score:{maxScore},bestMove:{bestMove}')
            return [maxScore,bestMove]
        else:
            minScore, bestMove = math.inf, None
            for move in valid_computer_moves:
                new_board = copy.deepcopy(board)
                new_board.set_field_used(move[0],move[1])
                new_board.last_move_played = [move[0],move[1]]
                score = new_board._minimax(new_board, player,depth-1,alpha,beta)
                beta = min(beta,score[0])
                if score[0] <= minScore:
                    minScore = score[0]
                    bestMove = move
                if beta <= alpha:
                    #print("Breaking MIN score")
                    break
                
            #print(f'Min score:{minScore},bestMove:{bestMove}')
            return [minScore,bestMove]

    # funkcija koja vraca broj poena koji predstavlja trenutno stanje na tabli
    def evalute_board_state(self):
        k_in_row_fields_white = self.get_k_in_a_row_fields(self.WHITE_COLOR)
        k_in_row_fields_black = self.get_k_in_a_row_fields(self.BLACK_COLOR)
        total_score = self.calculate_score_from_arr_white(k_in_row_fields_white) + self.calculate_score_from_arr_black(k_in_row_fields_black)
        return total_score
    
    #functions only for testing board
    def fill_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.set_field_used(i,j)
        
