# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000       # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM

# conecta-se com o par passivo
sock.connect((HOST, PORTA))

while True:
	#mensagem escrita pelo lado ativo
	msg = input()

	# mensagem que encerra a conexão
	if msg.lower() == 'encerrar':
		print('Encerrando conexao...')
		break

	# envia uma mensagem para o par conectado
	sock.send(bytes(msg, 'utf-8'))

	#espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
	rcv = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem

	# imprime a mensagem recebida
	print(str(rcv,  encoding='utf-8'))


# encerra a conexao
sock.close()