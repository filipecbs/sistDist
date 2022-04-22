# Exemplo basico socket (lado passivo)

import socket, sys

HOST = ''    # '' possibilita acessar qualquer addr alcancavel da maquina local
PORT = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicação
with socket.socket() as s: # default: socket.AF_INET, socket.SOCK_STREAM
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # código para reusar a porta
	s.bind((HOST, PORT)) # vincula a interface e porta para comunicacao
	s.listen() # define o limite máximo de conexões pendentes e coloca-se em modo de espera por conexão

	while True:
		try:
			# aceita uma conexão dentro do loop para que o servidor continue ligado no socket s
			ns, addr = s.accept()  # retorna um novo socket e o endereço do par conectado

			with ns:
				print('Conectado com', addr)

				while True:
					# depois de conectar-se, espera uma mensagem
					msg = ns.recv(1024) # argumento indica a qtde maxima de dados

					# mensagem de encerramento da conexão
					if not msg:
						print('Encerrando conexao com: ', addr)
						break

					else:
						# envia mensagem de resposta
						ns.send(msg)

		# reconhece ctrl + c para encerrar o servidor
		except KeyboardInterrupt:
			print('Encerrando servidor...')
			break

# encerra a aplicação
sys.exit()