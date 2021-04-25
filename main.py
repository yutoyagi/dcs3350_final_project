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


# run SEIR model until 36% of nodes are infected
def SEIR(G, beta):
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['Infected'] = True
    G.nodes[rand_idx]['Infected_t'] = 0

    # run simulation
    t = 0
    while count_infected(G) <= (G.number_of_nodes()*0.36):


        # E- >I, E->S, I->R
        for i in G.nodes:
            if G.nodes[i]['Exposed']: 
                if G.nodes[nbr]['Turn_I_at_t=x'] and G.nodes[nbr]['Turn_I_at_t=x'] <= t:
                    G.nodes[nbr]['Exposed'] = False
                    G.nodes[nbr]['Infected'] = True
                    G.nodes[nbr]['Infected_t'] = t
                    G.nodes[nbr]['Turn_I_at_t=x'] = None
                if G.nodes[nbr]['Turn_S_at_t=x'] and G.nodes[nbr]['Turn_I_at_t=x'] <= t:
                    G.nodes[nbr]['Exposed'] = False
                    G.nodes[nbr]['Susceptible'] = True
                    G.nodes[nbr]['Turn_S_at_t=x'] = None


            elif G.nodes[i]['Infected']: 
                # infect others
                for nbr in G.neighbors(i):
                    if G.nodes[nbr]['Susceptible']:
                        G.nodes[nbr]['Susceptible'] = False
                        G.nodes[nbr]['Exposed'] = True
                        if random.random() <= beta:
                            # this neighbor is infected
                            G.nodes[nbr]['Turn_I_at_t=x'] = t + random.randint(1,10) 
                        else:
                            G.nodes[nbr]['Turn_S_at_t=x'] = t + 10
                # check if they should recover by now
                if G.nodes[i]['Infected_t'] + 14 <= t:
                    G.nodes[i]['Infected'] = False
                    G.nodes[i]['Infected_t'] = None
                    G.nodes[i]['Recovered'] = True
                
        t+=1
        print(t)

        ## stop if it takes tooo long
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

# this function takes Graph G and beta value beta, and returns modified G and beta
def hard_lockdown(G, beta):
    # delete edges 
    # reduce beta because of mask 
    return (new_G, new_beta)

# this function takes Graph G and beta value beta, and returns modified G and beta
def soft_lockdown(G, beta):
    # delete edges 
    # reduce beta because of mask 
    return (new_G, new_beta)




# Wattz Strogartz network 

output = [] # list of list [network_size, beta, avg_degree, time]
n = 100     
k = 5       # household's size
p = 0.3     
beta = 0.1

# lower beta with stronger lockdown

G = nx.watts_strogatz_graph(n, k, p, seed=None)
# TODO: add dissident node
for i in G.nodes: 
    G.nodes[i]['Susceptible'] = True
    G.nodes[i]['Exposed'] = False
    G.nodes[i]['Turn_I_at_t=x'] = None
    G.nodes[i]['Turn_S_at_t=x'] = None
    G.nodes[i]['Infected'] = False
    G.nodes[i]['Infected_t'] = None
    G.nodes[i]['Recovered'] = False

avg_degree = get_avg_degree(G)
time = SEIR(G, beta)
output.append([network_size, beta, avg_degree, time])
        
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