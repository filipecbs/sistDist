# Cliente

import socket

HOST = 'localhost' # máquina onde esta o servidor
PORT = 5000       # porta que o servidor está escutando

# cria socket
with socket.socket() as s: # default: socket.AF_INET, socket.SOCK_STREAM
	s.connect((HOST, PORT)) # conecta-se com o servidor
	print('Conectado! Digite o nome do arquivo: ')

	# nome do arquivo que o cliente deseja acessar
	filename = input()

	# envia o nome do arquivo para o servidor
	s.sendall(filename.encode())

	# espera a resposta do servidor
	rcv = s.recv(1024)

	# imprime a mensagem recebida
	print(rcv.decode())

	# mensagem que encerra a conexão
	print('Encerrando conexão...')