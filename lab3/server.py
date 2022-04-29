# Servidor

import select, socket, string, sys, threading
from os.path import exists

HOST = ''    # '' possibilita acessar qualquer endereço alcancavel da maquina local
PORT = 5000  # porta onde chegarao as mensagens para essa aplicacao
inputs = [sys.stdin] # entradas para escuta do select

def access(filename):
	# confere se o arquivo existe
	if exists(filename + '.txt'):
		f = open(filename + '.txt', 'r')
		text = f.read().rstrip()

		return True, text
	else:
		return False, "Esse arquivo não existe!"

def process(filename):
	# ativa a camada de acesso para pegar o arquivo
	file_exists, text = access(filename)

	# se o arquivo existe, realiza o processamento dos dados
	if file_exists:
		processed_text = text.translate(str.maketrans('', '', string.punctuation)) # retira pontuação do texto
		processed_text = processed_text.lower().replace('\n', ' ') # troca quebra de linha por espaço
		words = processed_text.split(' ') # cria um array com as palavras do texto
		word_count = {} # dicionário para contar a frequência das palavras

		for word in words:
			word_count[word] = word_count.get(word, 0) + 1 # salva a frequência da palavra em sua respectiva chave

		sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True) # ordena o dicionário por frequência
		most_frequent = '\nPalavras mais frequentes:\n\n'
		i = 0

		# cria uma lista com as 5 palavras mais frequentes
		for word in sorted_words:
			if i == 5: break
			if word[0] == '': continue
			most_frequent += word[0] + ': ' + str(word[1]) + '\n'
			i += 1

		return True, most_frequent

	# se o arquivo não existe, retorna a mensagem de erro
	else:
		return False, text

def initializeServer():
	# cria um socket para comunicação
	s = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # código para reusar a porta
	s.bind((HOST, PORT)) # vincula a interface e porta para comunicacao
	s.listen(5) # define o limite máximo de conexões pendentes e coloca-se em modo de espera por conexão
	s.setblocking(False) # configura o socket para não ser bloqueante
	return s

def acceptConnection(s):
	cs, addr = s.accept() # retorna um novo socket e o endereço do par conectado
	return cs, addr

def handleRequests(cs, addr):
		while True:
			msg = cs.recv(1024) # argumento indica a quantidade máxima de dados
			if not msg:
				# mensagem de encerramento da conexão
				print('Encerrando conexão com', addr)
				cs.close()
				return
			# ativa a camada de processamento
			file_exists, text = process(msg.decode())
			# envia a lista de palavras mais frequentes ou uma mensagem de erro
			cs.sendall(text.encode())


def main():
	sock = initializeServer()
	inputs.append(sock)
	print('Servidor inicializado!')
	clients = [] # threads ativas

	while True:
		r, w, e = select.select(inputs, [], []) # separa os tipos de entrada

		# faz um loop por todas as entradas
		for ready in r:
			# socket criado pelo servidor
			if ready == sock:
				cs, addr = acceptConnection(sock)
				print('Conectado com:', addr)
				client = threading.Thread(target=handleRequests, args=(cs, addr)) # cria a thread
				client.start()
				clients.append(client)

			# input do terminal
			elif ready == sys.stdin:
				cmd = input()

				if cmd == 'fim':
					# passa pelas threads para poder encerrar
					for c in clients:
						c.join()

					sock.close()
					print('Encerrando servidor...')
					# encerra a aplicação
					sys.exit()

if __name__ == '__main__':
	main()
