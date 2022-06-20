import multiprocessing, random, rpyc
from node import initialize

HOST = 'localhost'
PORT = 5000

def create_nodes():
	tids = random.sample(range(1, 1000), 10)
	nodes = []

	nodes.append((tids[0], PORT+tids[0], [(HOST, PORT+tids[1]), (HOST, PORT+tids[2]), (HOST, PORT+tids[4]), (HOST, PORT+tids[7])]))
	nodes.append((tids[1], PORT+tids[1], [(HOST, PORT+tids[0]), (HOST, PORT+tids[3]), (HOST, PORT+tids[4])]))
	nodes.append((tids[2], PORT+tids[2], [(HOST, PORT+tids[0]), (HOST, PORT+tids[5]), (HOST, PORT+tids[6])]))
	nodes.append((tids[3], PORT+tids[3], [(HOST, PORT+tids[1]), (HOST, PORT+tids[4]), (HOST, PORT+tids[5])]))
	nodes.append((tids[4], PORT+tids[4], [(HOST, PORT+tids[0]), (HOST, PORT+tids[1]), (HOST, PORT+tids[3]), (HOST, PORT+tids[5])]))
	nodes.append((tids[5], PORT+tids[5], [(HOST, PORT+tids[2]), (HOST, PORT+tids[3]), (HOST, PORT+tids[4]), (HOST, PORT+tids[6])]))
	nodes.append((tids[6], PORT+tids[6], [(HOST, PORT+tids[2]), (HOST, PORT+tids[5]), (HOST, PORT+tids[7])]))
	nodes.append((tids[7], PORT+tids[7], [(HOST, PORT+tids[0]), (HOST, PORT+tids[6]), (HOST, PORT+tids[8]), (HOST, PORT+tids[9])]))
	nodes.append((tids[8], PORT+tids[8], [(HOST, PORT+tids[5]), (HOST, PORT+tids[9])]))
	nodes.append((tids[9], PORT+tids[9], [(HOST, PORT+tids[7]), (HOST, PORT+tids[8])]))

	ids = []

	for node in nodes:
		ids.append(node[0])

	print("ids:", ids)
	print("maior id:", max(ids))

	return nodes

def main():
	try:
		nodes = create_nodes()
		processes = []

		for i in range(len(nodes)):
			processes.append(multiprocessing.Process(target=initialize, args=nodes[i]))
			processes[i].start()

		def print_response(response):
			print(f"O líder é o nó {response}")

		node = nodes[random.randint(0, len(nodes)-1)]
		conn = rpyc.connect(HOST, node[1])
		conn.root.probe_echo(print_response)

		for i in range(len(nodes)):
			processes[i].join()

	except KeyboardInterrupt:
		for i in range(len(nodes)):
			processes[i].terminate()

if __name__ == "__main__":
	main()