import socket

class Client(object):
	"""docstring for Client"""
	def __init__(self, port_send, port_rcv, ip_server):
		super(Client, self).__init__()
		self.port_send = port_send
		self.port_rcv = port_rcv
		self.ip_server = ip_server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def connect(self):
		message = "conecta"
		print("Send Message: ",message)
		self.sock.sendto(message.encode('utf-8'), (self.ip_server, self.port_send))

		answer = self.rcv_message()
		if answer == "conectado":
			print "Conectado"

	def rcv_message(self):

		while True:
			data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
			# print ("Message received:", data.decode('utf_8'))
			return data

	def send_move(self, moves):

		for m in moves:
			message = m
			print("Send Message: ", message)
			self.sock.sendto(message.encode('utf-8'), (self.ip_server, self.port_send))

			answer = self.rcv_message()
			if answer == "ok":
				print "Movimento OK"

		message = "fim"
		print("Send Message: ", message)
		self.sock.sendto(message.encode('utf-8'), (self.ip_server, self.port_send))
