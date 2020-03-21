import BT
import maze
import score
from time import sleep

class Interface:
	def __init__(self):
		print ('')
		print ('Arduino Bluetooth Connect Program.')
		print ('')
		self.ser = BT.bluetooth()
		port = input('PC bluetooth port name: ')
		while not self.ser.do_connect(port):
			if port == 'quit':
				self.ser.disconnect()
				quit()
			port = input('PC bluetooth port name: ')

	def sendstartsignal(self, check = True):
		read = self.ser.SerialReadString()
		if check:
			while 'z' not in read:
				read = self.ser.SerialReadString()
		input('Press enter to start.')
		self.ser.SerialWrite('s')
		print ('python write: s')
		self.ser.ser.reset_input_buffer()
		sleep(0.01)
		self.ser.ser.reset_output_buffer()

	def wait_for_node(self):
		#self.ser.ser.reset_input_buffer()
		return self.ser.SerialReadByte()

	def send_action(self, direc):
		#self.ser.ser.reset_output_buffer()
		if direc == maze.Action.ADVANCE:
			self.ser.SerialWrite('u')
		elif direc == maze.Action.U_TURN:
			self.ser.SerialWrite('d')
		elif direc == maze.Action.TURN_RIGHT:
			self.ser.SerialWrite('r')
		elif direc == maze.Action.TURN_LEFT:
			self.ser.SerialWrite('l')
		elif direc == maze.Action.HALT:
			self.ser.SerialWrite('h')
		else:
			print ('Error: An invalid input for action.')
		self.ser.ser.reset_output_buffer()

	def end_process(self):
		self.ser.SerialWrite('a')
		self.ser.disconnect()