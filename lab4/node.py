import rpyc # módulo que oferece suporte à abstração de RPC
from rpyc.utils.server import ThreadedServer # servidor que dispara uma nova thread a cada conexão

# endereco do servidor de echo
HOST = 'localhost'
PORT = 5000

# classe representando o nó do grafo
class Node(rpyc.Service):
	def __init__(self, node_id, neighbors):
		self.node_id = node_id # identificador do nó
		self.neighbors = neighbors # lista de tuplas (id, port)
		self.data = [self.node_id] # lista de valores recebidos
		self.visited = False # determina se o nó já foi visitado

	# executa quando uma conexão é criada
	def on_connect(self, conn):
		pass

	# executa quando uma conexão é fechada
	def on_disconnect(self, conn):
		pass

	# realiza todo o algoritmo de eleição
	# para encontrar o nó com maior valor
	def exposed_probe_echo(self, callback):

		# adiciona o id do vizinho e retorna o maior valor
		# se tiver recebido ack de todos os vizinhos
		def finished_node(pid):
			self.data.append(pid)
			if len(self.data) == len(self.neighbors) + 1:
				callback(max(self.data))

		# se o nó já tiver sido chamado
		# retorna um valor mínimo
		if self.visited:
			callback(0)
			return

		# o nó foi chamado
		self.visited = True

		# percorre todos os vizinhos do nó
		# e se conecta com eles
		for socket in self.neighbors:
			conn = rpyc.connect(*socket)
			conn.root.probe_echo(finished_node)
			conn.close()

# inicializa o nó
def initialize(tid, port, neighbors):
	t = ThreadedServer(Node(tid, neighbors), port=port)
	t.start()