#port = /dev/tty.15-SPPDev

import node
import maze
import score
import student

import time
import sys
#import pandas
#import copy

def main():
	global mz
	global Interface
	try:
		game = sys.argv[1]
	except:
		game = str(input('game 1 or 2:'))
	#mz = maze.Maze('data/test_dis_20180502.csv')
	mz = maze.Maze('data/maze_405_0508.csv')
	#next_nd = mz.getStartPoint()
	#point = score.Scoreboard('data/UID_405_20180502.csv')
	Interface = student.Interface()	 #include do_connect


	if game == '1':	#connecting another bluetooth

		game_1()

	elif game == '2':

		game_2()


def game_1(car_dir = node.Direction.South, cur_nd = 1, move = True):
	point = score.Scoreboard('data/UID_405_20180502.csv')
	action_list, order, total_path = mz.strategy_1(car_dir, cur_nd)
	#action_list = [3, 5, 2, 1, 3, 6]
	#order, total_path = mz.BFS()
	i = 0
	j = 0
	rfid_list = []

	Interface.sendstartsignal(move)	#SerialWrite('s')
	while True:
		try:
			if Interface.ser.ser.in_waiting != 0:
				readstring = Interface.ser.SerialReadString()
				#print out trash
				print ("arduino(readstring): ", readstring)
				#cur_nd = next_nd
				#next_nd = total_path[i+1]
				act = action_list[i]
				if 'q' in readstring:	#at node
					print ('python node')
					if act == 5:	#at deadend
						Interface.send_action(act)
						time.sleep(1)
						i += 1
						Interface.send_action(action_list[i])
						
						time.sleep(1)
						read = Interface.ser.SerialReadString()
					else:	
						Interface.send_action(act)
					print ('current node:', total_path[j])
					print (act)
					i += 1
					j += 1

				elif 'y' in readstring:
					print ("arduino print(read): ", read)
					#read = Interface.ser.SerialReadString()
					time.sleep(0.5)
					rfid_hex = Interface.wait_for_node()
					###
					rfid_list.append(rfid_hex)
					print ('rfid_hex', rfid_hex)
					print (rfid_list)
					###
					#rfid_hex = Interface.wait_for_node()
					point.add_UID(rfid_hex)
				
					mz.deadend = mz.deadend[1:]

					if act == 6:	#should stop
						Interface.end_process()
						break


		except KeyboardInterrupt:
			instruction = str(input('Continue(c) or End(e):'))
			if instruction == 'c':
				print (mz.deadend)
				direc = int(input('Please input current direction:(1->N, 2->S, 3->W, 4->E)'))
				cur_nd = int(input('Please input current node:'))
				game_1(direc, cur_nd, False)
			elif instruction == 'e':
				print (rfid_list)
				print ('---complete---')
				print ('')
				print ('The total score: ', point.getCurrentScore())

				Interface.end_process()
				break
	
	print (rfid_list)
	print ('---complete---')
	print ('')
	print ('The total score: ', point.getCurrentScore())

def game_2(car_dir = node.Direction.South, cur_nd = 1, move = True):
	nds = input('assigned point:')
	nd_list = [int(i) for i in nds.split(' ')]
	action_list, total_path = mz.strategy_2(nd_list, car_dir, cur_nd)
	i = 0
	j = 0
	#rfid_list = []

	Interface.sendstartsignal(move)	#SerialWrite('s')
	while True:
		try:
			if Interface.ser.ser.in_waiting != 0:
				readstring = Interface.ser.SerialReadString()
				print ('python print: ', readstring)
				act = action_list[i]

				if 'q' in readstring:
					print ('send action')
					act = action_list[i]
					if act == 5:
						Interface.send_action(act)
						time.sleep(1)
						i += 1
						Interface.send_action(action_list[i])
						
						read = Interface.ser.SerialReadString()
						while 'y' not in read:
							read = Interface.ser.SerialReadString()
						rfid_hex = Interface.wait_for_node()
						rfid_list.append(rfid_hex)
						print ('get rfid')
						print (rfid_list)
						
					else:
						Interface.send_action(act)
					print ('current node: ', total_path[j])
					print (act)
					i += 1
					j += 1

				if act == 6:
					Interface.end_process()
					break

		except KeyboardInterrupt:
			instruction = str(input('Continue(c) or End(e):'))
			if instruction == 'c':
				direc = int(input('Please input current direction:(1->N, 2->S, 3->W, 4->E)'))
				cur_nd = int(input('Please input current node:'))
				game_2(direc, cur_nd)
			elif instruction == 'e':
				Interface.end_process()
				break


	print ('---complete---')
	print ('')
	print ('/'.join(str(i) for i in rfid_list))

if __name__ == '__main__':
	main()