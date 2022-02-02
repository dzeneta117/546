import json
from django import template
from django.http.response import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, request
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from freedom.logic.board import Board



board = Board(None)

def index(request):
    context = {}
    return render(request,'freedom/index.html',context)

# this method is called when new game has started
@csrf_exempt
def game(request):
    global board
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        board = Board(body['chosenPlayer'])
        return JsonResponse({'message':'New game started'})
    return

@csrf_exempt
def finish(request):
    if request.method == 'POST':
        winner_arr = board.calculate_winner()
        white_points,white_arr,black_points,black_arr = winner_arr
        print(white_arr)
        print(black_arr)
        return JsonResponse({'message':'Game has finished',
        'whitePoints':white_points,
        'whiteArr':white_arr,
        'blackPoints':black_points,
        'blackArr':black_arr
        })

#this method is called when the player plays new move       
@csrf_exempt
def play(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        #citanje podataka
        i = body['i']
        j = body['j']

        if not board.is_field_free(i,j):
            return JsonResponse({'errorCode':1})

        if not board.is_valid_move(i,j):
            return JsonResponse({'errorCode':2})

        board.set_field_used(i,j) # oznacavanje polja kao zauzeto
        
        computer_moves = [] #potezi koje igra kompjuter
        if board.is_computer:
            computer_moves = board.play_move_minimax(i,j)
            if not computer_moves:
                board.computer_not_play_last_move = True


        data = {
            'errorCode':0,
            'whiteOnMove':board.whiteOnMove if board.is_computer else not board.whiteOnMove,
            'gameFinished':False,
            "computerMoves" : computer_moves
        }
        
        if board.lastMove:
            data['gameFinished'] = board.game_has_finished()
        if board.computer_not_play_last_move:
            data['gameFinished'] = True


        data['lastMove'] = board.lastMove
        return JsonResponse(data)
    return 