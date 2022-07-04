import rpyc, sys
from threading import Lock, Thread

HOST = 'localhost'
PORT = 5000
N = 4 # número de réplicas

# cria o grafo inicial com nós aleatórios
def create_replicas():
	replicas = []

	for n in range(1, N+1):
		replicas.append((n, PORT+n, [(HOST, PORT+i) for i in range(1, N+1) if i != n]))

	return replicas

class Replica(rpyc.Service):
	def __init__(self, replica_id, neighbors):
		self.replica_id = replica_id # identificador da réplica
		self.neighbors = neighbors # lista de tuplas (id, port)
		self._x = 0 # valor atual de X
		self.original = 1 # réplica que mantém o valor de X
		self.history = [] # guarda o histórico de alterações
		self.lock = Lock() # bloqueia acesso ao valor de X

	# lê o valor da réplica
	def exposed_read_value(self):
		print(f"O valor na réplica {self.replica_id} é {self._x}.")

	# vê o histórico de alterações
	def exposed_get_history(self):
		if len(self.history) == 0:
			print("O histórico está vazio.")

		else:
			print(f"Histórico de atualizações:")
			for h in self.history:
				print(f"Réplica {h[0]}: {h[1]}")

	# atualiza o histórico de alterações da réplica
	def exposed_update_history(self, replica_id, x):
		self.history.append((replica_id, x))

	# atualiza o valor da réplica
	def exposed_update_value(self, x):
		self._x = x

	# atualiza o valor de X na réplica
	def exposed_write_value(self, replica_id, x):

		self.exposed_get_original()

		with self.lock: # bloqueia acesso ao valor de X
			self._x = x # atualiza o valor de X
			self.exposed_update_history(replica_id, self._x) # atualiza o histórico de alterações

	# modifica qual réplica mantém a cópia primária
	def exposed_set_original(self, replica_id):
		self.original = replica_id

	def exposed_get_original(self):
		if self.replica_id == self.original:
			return

		try:
			conn = rpyc.connect(HOST, PORT+self.original)
			conn.root.update_original(self.replica_id)
			conn.close()
		except ConnectionRefusedError:
			pass

	# lógica de atualização da cópia primária
	def exposed_update_original(self, replica_id):

		self.original = replica_id

		# atualiza cópia primária dos vizinhos
		for n in self.neighbors:
			try:
				conn = rpyc.connect(n[0], n[1])
				conn.root.set_original(replica_id)
				conn.root.update_value(self._x)
				if len(self.history) > 0:
					conn.root.update_history(*self.history[-1])
				conn.close()
			except ConnectionRefusedError:
				pass

	# finaliza o programa
	def exposed_exit_program(self):
		if self.replica_id == self.original:
			new_original = None
			# atualiza o valor de X e o histórico nas outras réplicas
			for n in self.neighbors:
				try:
					conn = rpyc.connect(n[0], n[1])

					if new_original is None:
						new_original = n[1]-PORT
					if new_original is not None:
						conn.root.set_original(new_original)
						conn.root.update_value(self._x)
						if len(self.history) > 0:
							conn.root.update_history(*self.history[-1])
					conn.close()

				except ConnectionRefusedError:
					pass

	# executa quando uma conexão é criada
	def on_connect(self, conn):
		pass

	# executa quando uma conexão é fechada
	def on_disconnect(self, conn):
		pass

# inicializa a réplica
def initialize(tid, port, neighbors):
	global t
	t = rpyc.utils.server.ThreadedServer(Replica(tid, neighbors), port=port)
	t.start()

def main():
	replicas = create_replicas()

	id = int(sys.argv[1])

	server = Thread(target=initialize, args=replicas[id-1])
	server.start()

	conn = rpyc.connect(HOST, PORT + id)

	# imprime o menu no terminal
	while True:
		print("\n1. ler o valor atual de X na réplica")
		print("2. ler o histórico de alterações de X")
		print("3. alterar o valor de X")
		print("4. finalizar o programa")
		print("\nDigite a opção desejada: ")

		op = int(input())

		if op == 1:
			conn.root.read_value()
		elif op == 2:
			conn.root.get_history()
		elif op == 3:
			print("Digite o novo valor de X: ")
			x = int(input())
			conn.root.write_value(id, x)
		elif op == 4:
			conn.root.exit_program()
			break
		else:
			print("Opção inválida!")

	t.close()

if __name__ == "__main__":
    main()