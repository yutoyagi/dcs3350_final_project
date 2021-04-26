import networkx as nx 
import matplotlib.pyplot as plt 
import random 
import statistics as stat
import random
import csv

# helper functions

"""
def SI(G, beta):
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['I'] = True
    # run simulation
    t = 0
    while count_I(G) <= (G.number_of_nodes()*0.36):
        # for each I node
        I_nodes = [i for i in G.nodes if G.nodes[i]['I'] ]
        for i in I_nodes:
            # for each neigbor
            for nbr in G.neighbors(i):
                if random.random() <= beta:
                    # this neighbor is I
                    G.nodes[nbr]['I'] = True                    
        t+=1 
        print(t)
        if t >= 100000:
            break
        #color_draw(G)
    return t
"""

# run SEIR model until 36% of nodes are I
def SEIR(G, beta, start_time = 0, end_time = 100000):
    """ Return the time it takes to infect 36% of the population """
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['I'] = True
    G.nodes[rand_idx]['I_t'] = 0

    # run simulation
    t = 0
    while count_I_and_R(G) <= (G.number_of_nodes()*0.36):
        # E- >I, E->S, I->R
        for i in G.nodes:
            if G.nodes[i]['I']: 
                # infect others
                for nbr in G.neighbors(i):
                    if G.nodes[nbr]['S']:
                        G.nodes[nbr]['S'] = False
                        G.nodes[nbr]['E'] = True
                        if random.random() <= beta:
                            # this neighbor will be Infected
                            G.nodes[nbr]['Turn_I_at_t=x'] = t + random.randint(1,10) 
                            #print("will be infected on ", G.nodes[nbr]['Turn_I_at_t=x'])
                        else:
                            # this neighbor will not be Infected
                            G.nodes[nbr]['Turn_S_at_t=x'] = t + 10 # assume that quarantine for exposed people are 10 days
                # node should recover after 14 days since infection time
                if G.nodes[i]['I_t'] + 14 == t:
                    G.nodes[i]['I'] = False
                    G.nodes[i]['I_t'] = None
                    G.nodes[i]['R'] = True            

            if G.nodes[i]['E']:
                if G.nodes[i]['Turn_I_at_t=x'] != None:
                    if G.nodes[i]['Turn_I_at_t=x'] == t:
                        G.nodes[i]['E'] = False
                        G.nodes[i]['I'] = True
                        G.nodes[i]['I_t'] = t
                        G.nodes[i]['Turn_I_at_t=x'] = None
                if G.nodes[i]['Turn_S_at_t=x'] != None: 
                    if G.nodes[i]['Turn_S_at_t=x'] == t:
                        G.nodes[i]['E'] = False
                        G.nodes[i]['S'] = True
                        G.nodes[i]['Turn_S_at_t=x'] = None

                
        t+=1
        print("t=", t)

        ## stop if it takes tooo long
        if t >= end_time:
            break
        #color_draw(G)
    return start_time + t



def count_I(G):
    """Return the active infection count"""
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['I']:
            cnt+=1
    return cnt

def count_I_and_R(G):
    """Return the cumuative infection count"""
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['I'] or G.nodes[i]['R']:
            cnt+=1
    print(cnt)
    return cnt

def get_avg_degree(G):
    """ takes a graph G and returns its average"""
    degrees = [G.degree[i] for i in G.nodes]
    return sum(degrees)/len(degrees)

# this function requires plt.show() to be called outside of this function
def color_draw(G):
    color_map = []
    for i in G.nodes:
        if G.nodes[i]['I']:
            color_map.append('red')
        else: 
            color_map.append('blue')     
    nx.draw(G, node_color=color_map, with_labels=True)
    return None 


# TODO: debug
def hard_lockdown(G, beta):
    """ this function takes Graph G and beta value beta, and returns modified G and beta. """
    # delete edges 
    # reduce beta because of mask 
    infected_nodes = []
    compliance_level = range(0.7, 0.999)
    compliant_infected_nodes = [] #theoretically we must only isolate infected nodes, but since we can't identify all infected nodes, in practice we must isolate all nodes
    compliant_infected_nodes = compliance_level * len(infected_nodes)
    dissident_infected_nodes = []
    dissident_infected_nodes = (1 - compliance_level) * len(infected_nodes)
    beta = b
    average_degree_of_node = k
    new_average_degree_of_node = h #determined as household size

    for i in G.nodes:
        if G.nodes[i]['I']: 
            append(i).infected_nodes
    
    for i in infected_nodes:
        if i in compliant_infected_nodes:
            degree_of_node(i) = new_average_degree_of_node
        else:
            degree_of_node(i) = average_degree_of_node
    return None

# TODO: debug
def soft_lockdown(G, beta):
    """ this function takes Graph G and beta value beta, and returns modified G and beta. """
    # delete edges 
    # reduce beta because of mask 
    infected_nodes = []
    compliance_level = range(0.7, 0.999)
    compliant_infected_nodes = [] #theoretically we must only isolate infected nodes, but since we can't identify all infected nodes, in practice we must isolate all nodes
    compliant_infected_nodes = compliance_level * len(infected_nodes)
    dissident_infected_nodes = []
    dissident_infected_nodes = (1 - compliance_level) * len(infected_nodes)
    beta = b
    beta_after_mask_wearing = b * range(0.4, 0.8) #reduction of infectiousness dependent upon type of mask worn and individual's symptomatic condition or viral load
    average_degree_of_node = k
    average_household_size = h
    new_average_degree_of_node = k * range(h, k)

    for i in G.nodes:
        if G.nodes[i]['I']: 
            append(i).infected_nodes
    
    for i in infected_nodes:
        if i in compliant_infected_nodes:
            degree_of_node(i) = new_average_degree_of_node
            beta(i) = beta_after_mask_wearing
        else:
            degree_of_node(i) = average_degree_of_node
    return None




# Wattz Strogartz network 

output = [] # list of list [network_size, beta, avg_degree, time]
n = 50     
k = 5       # household's size
p = 0.3     
beta = 1

# lower beta with stronger lockdown

G = nx.watts_strogatz_graph(n, k, p, seed=None)
# TODO: add dissident node
for i in G.nodes: 
    G.nodes[i]['S'] = True
    G.nodes[i]['E'] = False
    G.nodes[i]['Turn_I_at_t=x'] = None
    G.nodes[i]['Turn_S_at_t=x'] = None
    G.nodes[i]['I'] = False
    G.nodes[i]['I_t'] = None
    G.nodes[i]['R'] = False

avg_degree = get_avg_degree(G)
#color_draw(G)
#plt.show()
time = SEIR(G, beta)
output.append([n, beta, avg_degree, time])
        
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

'''
#Barabasi-Albert

# inputs
network_sizes = [10, 100, 1000]
betas = [0.05, 0.1, 0.4]
ms = [1, 5, 9]

output = [] # list of list [network_size, beta, avg_degree, time]

for network_size in network_sizes:
    for m in ms:
        for beta in betas:
            G = nx.barabasi_albert_graph(network_size, m)
            for i in G.nodes: 
                G.nodes[i]['I'] = False
            avg_degree = get_avg_degree(G)
            time = SI(G, beta)
            output.append([network_size, beta, avg_degree, time])
        
with open("Assignment1/output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)


# Erdos-Renyi 
network_sizes = [10, 100, 1000]
betas = [0.05, 0.1, 0.4]
probs = [0.1, 0.3, 0.5]

output = [] # list of list [network_size, beta, avg_degree, time]

for network_size in network_sizes:
    for prob in probs:
        for beta in betas:
            G = nx.erdos_renyi_graph(network_size, prob)
            for i in G.nodes: 
                G.nodes[i]['I'] = False
            avg_degree = get_avg_degree(G)
            time = SI(G, beta)
            output.append([network_size, beta, avg_degree, time])
            print("here")
        
with open("Assignment1/output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

'''
