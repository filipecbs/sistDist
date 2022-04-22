# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORT = 5000       # porta que o par passivo esta escutando

# cria socket
with socket.socket() as s: # default: socket.AF_INET, socket.SOCK_STREAM
	s.connect((HOST, PORT)) # conecta-se com o par passivo
	print('Conectado!')

	while True:
		#mensagem escrita pelo lado ativo
		msg = input()

		# mensagem que encerra a conexão
		if msg.lower() == 'encerrar':
			print('Encerrando conexao...')
			break

		# envia uma mensagem para o par conectado
		s.sendall(msg.encode())

		#espera a resposta do par conectado
		rcv = s.recv(1024)

		# imprime a mensagem recebida
		print(rcv.decode())