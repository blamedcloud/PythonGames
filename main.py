#!/usr/bin/env python
#main.py
###USAGE### main.py [-o <'simulate_all'/'simulate_end'/'simulate_d2_end'>] [-n <numgames>] [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'>] | [-n <numgames>] [-f <filename>] [-h <num_humans>] [-g <'Fractoe'/'Connect4'/'Checkers'/'Othello'>] [-D <depth_lim_x>] [-d <depth_lim_o>] [-A <ai_type_x>] [-a <ai_type_o>] [-s] [-q] [-x] [-o] ; sms=N ; $#=0-13
import AISuite.PythonLibraries.prgm_lib as prgm_lib
import sys
import AISuite.player as player
import AISuite.recorder as recorder
import random
from fractoe import Fractoe
from fractoe_heuristics import fractoe_heuristic
from checkers import Checkers, checkers_heuristic
from connect4 import Connect4, connect4_heuristic
from othello import Othello, othello_heuristic
from AISuite.alphabeta import shallowest_first

re_mk = prgm_lib.flag_re_mk

arg_dict = {}
arg_dict[re_mk('option')] = 1
arg_dict[re_mk('numgames')] = 1
arg_dict[re_mk('file')] = 1
arg_dict[re_mk('humans')] = 1
arg_dict[re_mk('game')] = 1
arg_dict[re_mk('DepthlimX')] = 1
arg_dict[re_mk('depthlimO')] = 1
arg_dict[re_mk('AitypeX')] = 1
arg_dict[re_mk('aitypeO')] = 1
arg_dict[re_mk('show')] = 0
arg_dict[re_mk('quiet')] = 0
arg_dict[re_mk('xhuman')] = 0
arg_dict[re_mk('ohuman')] = 0

flag_argc = [1,1,1,1,1,1,1,1,1,0,0,0,0]
flags = [re_mk('options'), re_mk('num_games'), re_mk('file'), re_mk('humans'), re_mk('game'), re_mk('DepthlimX'), re_mk('depthlimO'), re_mk('AitypeX'), re_mk('aitypeO'), re_mk('show'), re_mk('quiet'), re_mk('xhuman'), re_mk('ohuman')]

o_args = prgm_lib.arg_flag_ordering(sys.argv, flag_argc, flags)

option = "None"
num_games = 1
filename = "default"
humans = 0
game = "Fractoe"
depth_x = 4
depth_o = 4
ai_x = "random"
ai_o = "random"
show = False
quiet = False
xhuman = False
ohuman = False

if str(o_args[0]) != "None":
	option = str(o_args[0])
	
if str(o_args[1]) != "None":
	num_games = int(o_args[1])

if str(o_args[2]) != "None":
	filename = str(o_args[2])
	
if str(o_args[3]) != "None":
	humans = int(o_args[3])
	
if str(o_args[4]) != "None":
	game = str(o_args[4])
	
if str(o_args[5]) != "None":
	depth_x = int(o_args[5])
	
if str(o_args[6]) != "None":
	depth_o = int(o_args[6])
	
if str(o_args[7]) != "None":
	ai_x = str(o_args[7])
	
if str(o_args[8]) != "None":
	ai_o = str(o_args[8])
	
if str(o_args[9]) != "None":
	show = True
	
if str(o_args[10]) != "None":
	quiet = True
	
if str(o_args[11]) != "None":
	xhuman = True
	
if str(o_args[12]) != "None":
	ohuman = True

G = Fractoe
heuristic = fractoe_heuristic
tiles = ['X', 'O', ' ']
rec_board_height = 9
rec_board_height = 9
prefix = "fr_"
if game == "Fractoe":
	pass
elif game == "Connect4":
	G = Connect4
	heuristic = connect4_heuristic
	from connect4 import STANDARD_C4_HEIGHT as rec_board_height
	from connect4 import STANDARD_C4_WIDTH as rec_board_width
	prefix = "c4_"
elif game == "Checkers":
	G = Checkers
	heuristic = checkers_heuristic
	from checkers import BOARD_SIZE as rec_board_height
	rec_board_width = rec_board_height
	tiles = ['X', 'x', 'O', 'o', ' ']
	prefix = "ch_"
elif game == "Othello":
	G = Othello
	heuristic = othello_heuristic
	from othello import BOARD_SIZE as rec_board_height
	rec_board_width = rec_board_height
	prefix = "ot_"
	
if filename == "default":
	filename = prefix + "game_data.txt"

player1 = player.RandomAI()
player2 = player.RandomAI()
rec = None



if ai_x == "random":
	pass
elif ai_x == "heuristic":
	player1 = player.AI_ABPruning(heuristic, depth_lim = depth_x)
	player1.set_child_selector(shallowest_first)
elif ai_x == "recorder":
	rec = recorder.Recorder(filename, rec_board_height, rec_board_width, tiles)
	player1 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = depth_x)
	player1.set_child_selector(shallowest_first)
if ai_o == "random":
	pass
elif ai_o == "heuristic":
	player2 = player.AI_ABPruning(heuristic, depth_lim = depth_o)
	player2.set_child_selector(shallowest_first)
elif ai_o == "recorder":
	if rec == None:
		rec = recorder.Recorder(filename, rec_board_height, rec_board_width, tiles)
	player2 = player.AI_ABPruning(rec.recorder_heuristic, depth_lim = depth_o)
	player2.set_child_selector(shallowest_first)	

if humans == 1:
	if xhuman:
		player1 = player.Human()
	else:
		if ohuman:
			player2 = player.Human()
		else:
			choice = random.choice(["X","O"])
			if choice == "X":
				player1 = player.Human()
			else:
				player2 = player.Human()
elif humans == 2:
	player1 = player.Human()
	player2 = player.Human()
	
win_counts = [0,0,0]
		
if option == "simulate_all":	
	filename = prefix + "game_data_all.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		g = G(player.RandomAI(),player.RandomAI(),True)
		w = g.play()
		g.record_history_to_file(FILE)
		if x % 100 == 0:
			print x
		win_counts[w] += 1
	FILE.close()
elif option == "simulate_end":
	filename = prefix + "game_data.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		g = G(player.RandomAI(),player.RandomAI(),True)
		w = g.play()
		FILE.write(str(g) + '~' + str(w) + '\n')
		if x % 100 == 0:
			print x
		win_counts[w] += 1
	FILE.close()	
elif option == "simulate_d2_end":
	filename = prefix + "game_data_d2.txt"
	FILE = open(filename, 'a')
	for x in range(num_games):
		ai1 = player.AI_ABPruning(heuristic, depth_lim = 2)
		ai1.set_child_selector(shallowest_first)
		ai2 = player.AI_ABPruning(heuristic, depth_lim = 2)
		ai2.set_child_selector(shallowest_first)
		g = G(ai1,ai2,True)
		w = g.play()
		FILE.write(str(g) + '~' + str(w) + '\n')
		if x % 10 == 0:
			print x
		win_counts[w] += 1
	FILE.close()
else:
	for x in range(num_games):
		if not quiet:
			print "Beginning game %i" % (x)
		g = G(player1,player2, quiet, show)
		w = g.play()
		player1.reset()
		player2.reset()
		win_counts[w] += 1
		
print win_counts
for w in win_counts:
	print str(w) + "/" + str(num_games) + " : " + str(w/float(num_games))
print