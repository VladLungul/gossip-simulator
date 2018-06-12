import random
import argparse

parser = argparse.ArgumentParser(description='Epidemic protocol simulator.')
parser.add_argument('-n', type=int, help='Nodes quantity')
parser.add_argument('-i', type=int, help='Tests amount')

args = parser.parse_args()

NODE_REDIRECT_MESSSAGE_COUNT = 4
NODE_QUANTITY = args.n
TESTS_QUANTITY = args.i
DATA = 'data'


class Node:
    def __init__(self, redirect_number):
        self.redirect_number = redirect_number
        self.seen_data = set()
        self.done = False

    def set_nodes(self, nodes):
        nodes = nodes.copy()
        nodes.remove(self)
        self.known_nodes = nodes

    def _get_random_nodes(self, nodes_updated):
        redirect_number = self.redirect_number
        if len(nodes_updated) <= redirect_number:
           redirect_number = len(nodes_updated)            
        return random.sample(nodes_updated, redirect_number)

    def send(self, data):
        nodes_updated = set(self.known_nodes) - data.visited_nodes
        nodes_to_send_data = self._get_random_nodes(nodes_updated)
        for node in nodes_to_send_data:
            node.receive(data)

    def receive(self, data):
        if data not in self.seen_data:
            self.seen_data.add(data)
            self.send(data)
            self.done = True

class Data:
    def __init__(self, DATA):
        self.data = DATA
        self.visited_nodes = set()
        


succes_count = 0

for i in range(TESTS_QUANTITY):
    nodes = [Node(NODE_REDIRECT_MESSSAGE_COUNT) for i in range(NODE_QUANTITY)]
    [node.set_nodes(nodes) for node in nodes]
    first_node = nodes[0]
    data = Data(DATA)
    first_node.send(data)
    succes_count += all([node.done for node in nodes])
print('In {:.2f}% cases all nodes received the packet'.format(succes_count/1000 * 100))
