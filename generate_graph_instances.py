
n = 100000     
k = 20      
p = 0.3     
beta = 0.2
lockdown_start = 30




import os.path
import json
import pickle
import networkx as nx
from payoff_generators import generate_payoffs, print_M


def write_instance(id, node_size):
    filename = 'inputs/game_instances_%s.p' %id
    if os.path.isfile(filename):
        print("Game instances with this id already exists.")
        return None


    G = nx.nx.watts_strogatz_graph(n, k, p, seed=None)

    with open(filename, 'wb') as fp:
        pickle.dump(G, fp, protocol=pickle.HIGHEST_PROTOCOL)
    print("Done!")
    return None

def read_instance(id):
    """ Given a unique id, this function returns a set of game instances that is stored with that id """
    filename = 'inputs/game_instances_%s.p' %id
    print(filename)
    if not os.path.isfile(filename):
        print("No such instance exists!")
        raise IndexError

    with open(filename, 'rb') as fp:
        G = pickle.load(fp)
    return G



write_instance("")