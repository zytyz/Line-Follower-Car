from time import sleep
import serial

class bluetooth:
	def __init__(self):
		self.ser = serial.Serial()
		#if(self.ser.is_open):
			#print("open")

	def do_connect(self,port):
		self.ser.close()
		print('Connecting...')
		try:
			self.ser = serial.Serial(port, 9600, timeout=1)
			print('connect success')
			print('')
		except serial.serialutil.SerialException:
			print('fail to connect')
			print('')
			return False
		return True

	def disconnect(self):
		self.ser.close()

	def SerialWrite(self,output):
		send = bytes(output.encode('utf-8'))
		#bytes(i.encode("utf-8"))
		self.ser.write(send)

	def SerialReadString(self):
		sleep(0.01)
		waiting = self.ser.in_waiting
		#rv = [chr(c) for c in self.ser.read(waiting)]
		#print(rv)
		#rv = self.ser.readline().decode("utf-8")
		if(waiting != 0):
			return self.ser.readline().decode('utf-8')
			'''print("".join(rv))
			self.ser.flushInput()
			return "".join(rv)'''
		else:
			return ''

	def SerialReadByte(self):
		UID = ''
		while UID == '':
			sleep(0.05)
			waiting = self.ser.in_waiting
			rv = self.ser.read(20)
			#rv = self.ser.readline()

			if (rv):
				print ('rv', rv)
				UID = hex(int.from_bytes(bytearray([int(i) for i in bytes.decode(rv).split('\r\n')[:4]]), byteorder = 'big', signed = False))
				print(UID)
				print('')
				#self.ser.reset_input_buffer()
				return UID