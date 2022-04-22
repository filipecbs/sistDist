# Servidor

import socket, string, sys
from os.path import exists

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

HOST = ''    # '' possibilita acessar qualquer endereço alcancavel da maquina local
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

				msg = ns.recv(1024) # argumento indica a quantidade máxima de dados

				# ativa a camada de processamento
				file_exists, text = process(msg.decode())
				ns.sendall(text.encode())
				# mensagem de encerramento da conexão
				print('Encerrando conexão com: ', addr)

		# reconhece ctrl + c para encerrar o servidor
		except KeyboardInterrupt:
			print('Encerrando servidor...')
			break

# encerra a aplicação
sys.exit()