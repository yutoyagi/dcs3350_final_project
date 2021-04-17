import networkx as nx 
import matplotlib.pyplot as plt 
import random 
import statistics as stat
import random
import csv

# helper functions
def SI(G, beta):
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['Infected'] = True
    # run simulation
    t = 0
    while count_infected(G) <= (G.number_of_nodes()*0.36):
        # for each infected node
        infected_nodes = [i for i in G.nodes if G.nodes[i]['Infected'] ]
        for i in infected_nodes:
            # for each neigbor
            for nbr in G.neighbors(i):
                if random.random() <= beta:
                    # this neighbor is infected
                    G.nodes[nbr]['Infected'] = True                    
        t+=1 
        print(t)
        if t >= 100000:
            break
        #color_draw(G)
    return t

def count_infected(G):
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['Infected']:
            cnt+=1
    return cnt

def get_avg_degree(G):
    degrees = [G.degree[i] for i in G.nodes]
    print(degrees)
    return sum(degrees)/len(degrees)

# this function requires plt.show() to be called outside of this function
def color_draw(G):
    color_map = []
    for i in G.nodes:
        if G.nodes[i]['Infected']:
            color_map.append('red')
        else: 
            color_map.append('blue')     
    nx.draw(G, node_color=color_map, with_labels=True)
    return None 


# Wattz Strogartz network 



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
                G.nodes[i]['Infected'] = False
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
                G.nodes[i]['Infected'] = False
            avg_degree = get_avg_degree(G)
            time = SI(G, beta)
            output.append([network_size, beta, avg_degree, time])
            print("here")
        
with open("Assignment1/output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)

'''