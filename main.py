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
def SEIR(G, beta, case_dict, start_time = 0, end_time = 100000):
    """ Return the time it takes to infect 36% of the population """
    # TODO: return something when infection is zero!!
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['I_a'] = True
    G.nodes[rand_idx]['I_t'] = 0

    # run simulation
    t = 0
    while True:
    #while count_I_and_R(G) <= (G.number_of_nodes()*0.36):
        print("cumulative case=", count_I_and_R(G))
        # E- >I, E->S, I->R
        for i in G.nodes:
            # if I_s, then it will be in isolation and won't infect others   20%
            # if I_a, then it's asymptomatic and thus infect others  80%
            if G.nodes[i]['I_a'] or G.nodes[i]['I_s']: 
                # only asymptomatic or newly infected symptomatic will infect others b/c isolation
                if G.nodes[i]['I_a'] or (G.nodes[i]['I_s'] and (t - G.nodes[i]['I_t'])<5 ): 
                    for nbr in G.neighbors(i):
                        if G.nodes[nbr]['S']:
                            G.nodes[nbr]['S'] = False
                            G.nodes[nbr]['E'] = True
                            if random.random() <= beta:
                                # this neighbor will be Infected
                                G.nodes[nbr]['Turn_I_at_t=x'] = t + random.randint(5,10) 
                                # print("will be infected on ", G.nodes[nbr]['Turn_I_at_t=x'])
                            else:
                                # this neighbor will not be Infected
                                G.nodes[nbr]['Turn_S_at_t=x'] = t + 10 # assume that quarantine for exposed people are 10 days
                # node should recover after 14 days since infection time
                if G.nodes[i]['I_t'] + 14 == t:
                    G.nodes[i]['I_a'] = False
                    G.nodes[i]['I_s'] = False
                    G.nodes[i]['I_t'] = None
                    G.nodes[i]['R'] = True            

            # Exposed don't infect others until it turns infected
            if G.nodes[i]['E']:
                if G.nodes[i]['Turn_I_at_t=x'] != None:
                    if G.nodes[i]['Turn_I_at_t=x'] == t:
                        G.nodes[i]['E'] = False
                        # TODO coinflip
                        if random.random() <= 0.8:
                            G.nodes[i]['I_a'] = True
                        else:
                            G.nodes[i]['I_s'] = True
                        G.nodes[i]['I_t'] = t
                        G.nodes[i]['Turn_I_at_t=x'] = None
                if G.nodes[i]['Turn_S_at_t=x'] != None: 
                    if G.nodes[i]['Turn_S_at_t=x'] == t:
                        G.nodes[i]['E'] = False
                        G.nodes[i]['S'] = True
                        G.nodes[i]['Turn_S_at_t=x'] = None

        case_dict[t + start_time] = count_I_and_R(G)
        t+=1
        print("t=", t + start_time)

        ## stop if it takes tooo long
        if t >= end_time+start_time:
            break
        #color_draw(G)

        ## stop if no more infection
        if count_I(G)+count_E(G) == 0:
            print("No covid")
            break
        #color_draw(G)

    return G, (start_time + t), case_dict
    # TODO: should return G, t
    


def count_I(G):
    """Return the active infection count"""
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['I_a'] or G.nodes[i]['I_s'] :
            cnt+=1
    return cnt

def count_E(G):
    """Return the active infection count"""
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['E']:
            cnt+=1
    return cnt

def count_I_and_R(G):
    """Return the cumuative infection count"""
    cnt = 0
    for i in G.nodes:
        if G.nodes[i]['I_a'] or G.nodes[i]['I_s'] or G.nodes[i]['R']:
            cnt+=1
    return cnt

def get_avg_degree(G):
    """ takes a graph G and returns its average"""
    degrees = [G.degree[i] for i in G.nodes]
    return sum(degrees)/len(degrees)

# this function requires plt.show() to be called outside of this function
def color_draw(G):
    color_map = []
    for i in G.nodes:
        if G.nodes[i]['I_a'] or G.nodes[i]['I_s']:
            color_map.append('red')
        else: 
            color_map.append('blue')     
    nx.draw(G, node_color=color_map, with_labels=True)
    return None 


# TODO: debug
def lockdown(G, beta, max_degree, beta_multiplier, compliance_level): 
    """ this function takes Graph G and beta value beta, and returns modified G and beta. """
    neighbors_to_remove = set()
    
    for i in G.nodes:
        # if compliant 
        if random.random() <= compliance_level:
            # reduce the edges to 5
            neighbors = set(G.neighbors(i))
            if len(neighbors) <= max_degree:
                neighbors_to_keep = neighbors
            else:
                neighbors_to_keep = set(random.sample(neighbors, max_degree))
            neighbors_to_remove = neighbors - neighbors_to_keep
            for neighbors_to_remove in neighbors_to_remove:
                G.remove_edge(i, neighbors_to_remove)

    # reduce the beta value
    new_beta = beta * beta_multiplier
    
    return (G, new_beta)

def hard_lockdown(G, beta):
    return lockdown(G, beta, 4, 0.5, 0.9)

def soft_lockdown(G, beta):
    return lockdown(G, beta, 20, 0.5, 0.6)



# Wattz Strogartz network 

def run_simulation(G, lockdown_starts, beta=0.2):
    n = G.number_of_nodes()

    # initiliaze the G labels
    for i in G.nodes: 
        G.nodes[i]['S'] = True
        G.nodes[i]['E'] = False
        G.nodes[i]['Turn_I_at_t=x'] = None
        G.nodes[i]['Turn_S_at_t=x'] = None
        G.nodes[i]['I_s'] = False
        G.nodes[i]['I_a'] = False
        G.nodes[i]['I_t'] = None
        G.nodes[i]['R'] = False

    for lockdown_start in lockdown_starts:

        # let it run before lockdown
        case_dict=dict()
        G2, lockdown_start_date, case_dict = SEIR(G, beta, case_dict, start_time=0, end_time=lockdown_start)


        for lockdown_type in ["Hard", "Soft", "NA"]:
            if lockdown_type == "Hard":
                (new_G, new_beta) = hard_lockdown(G2, beta)
            elif lockdown_type == "Soft":
                (new_G, new_beta) = soft_lockdown(G2, beta)
            else:
                (new_G, new_beta) = (G2, beta)


            #avg_degree = get_avg_degree(new_G)
            new_G, time, case_dict = SEIR(new_G, new_beta, case_dict, start_time=lockdown_start_date)

            filename = 'outputs/n={0}_type={1}_start={2}.p'.format(n, lockdown_type, time)
            with open("output.csv", "w", newline="") as f:
                writer = csv.writer(f)
                for data in case_dict:
                    writer.writerow(data)

    return None


n=1000
k=30
p=0.5

lockdown_starts=[30, 60, 90]
G = nx.nx.watts_strogatz_graph(n, k, p, seed=None)
run_simulation(G, lockdown_starts, beta=0.2)


"""
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
"""


