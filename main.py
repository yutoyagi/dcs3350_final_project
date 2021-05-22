import networkx as nx 
import matplotlib.pyplot as plt 
import random 
import statistics as stat
import random
import csv
import copy


# run SEIR model until 36% of nodes are I
def SEIR(G, beta, case_dict, start_time = 0, end_time = 1000):
    """ Return the time it takes to infect 36% of the population """
    # TODO: return something when infection is zero!!
    # randomly infect one node
    rand_idx = random.randrange(0, G.number_of_nodes())
    G.nodes[rand_idx]['I_a'] = True
    G.nodes[rand_idx]['I_t'] = 0

    # run simulation
    t = start_time
    while True:
    #while count_I_and_R(G) <= (G.number_of_nodes()*0.36):
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
                if G.nodes[i]['I_t'] + 14 <= t:
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

        case_dict[t] = count_I_and_R(G)
        t+=1
        print("t=", t, "cumulative case=", count_I_and_R(G), "I=",count_I(G), "E=", count_E(G))

        ## stop if it takes tooo long
        if t >= end_time:
            break
        #color_draw(G)

        ## stop if no more infection
        if count_I(G)+count_E(G) == 0:
            print("No covid")
            break
        #color_draw(G)

    return G, t, case_dict
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
        if G.nodes[i]['E'] and G.nodes[i]['Turn_I_at_t=x']:
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
def lockdown(G, beta, max_degree, new_beta, compliance_level): 
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
    
    return (G, new_beta)

def hard_lockdown(G, beta):
    return lockdown(G, beta, 4, 0.05, 0.9)

def soft_lockdown(G, beta):
    return lockdown(G, beta, 15, 0.1, 0.9)

def init_G(G):
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
    return G

# Wattz Strogartz network 
"""
def run_simulation(G, lockdown_starts, beta=0.2):
    n = G.number_of_nodes()

    for lockdown_start in lockdown_starts:
        for lockdown_type in ["NA", "Soft", "Hard"]:
            inputG = init_G(G)
            # let it run before lockdown
            case_dict=dict()
            G2, lockdown_start_date, case_dict = SEIR(inputG, beta, case_dict, start_time=0, end_time=lockdown_start)
            print(lockdown_start_date)
            assert(lockdown_start_date == lockdown_start)

            if lockdown_type == "Hard":
                (new_G, new_beta) = hard_lockdown(G2, beta)
            elif lockdown_type == "Soft":
                (new_G, new_beta) = soft_lockdown(G2, beta)
            else:
                (new_G, new_beta) = (G2, beta)

            new_G, time, case_dict = SEIR(new_G, new_beta, case_dict, start_time=lockdown_start_date)

            filename = 'outputs/n={0}_type={1}_start={2}.csv'.format(n, lockdown_type, lockdown_start_date)
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                for key, value in case_dict.items():
                    writer.writerow([key, value])
    return None
"""
def run_simulation(G, lockdown_starts,lockdown_types, beta=0.2):
    n = G.number_of_nodes()
    G = init_G(G)
    avg_dig = get_avg_degree(G)

    for lockdown_start in lockdown_starts:
        G_copy = copy.deepcopy(G)
        # let it run before lockdown
        case_dict=dict()
        G2, lockdown_start_date, case_dict = SEIR(G_copy, beta, case_dict, start_time=0, end_time=lockdown_start)
        print(lockdown_start_date)
        assert(lockdown_start_date == lockdown_start)

        for lockdown_type in lockdown_types:
            new_case_dict = copy.deepcopy(case_dict) 
            G3 = copy.deepcopy(G2)
            if lockdown_type == "Hard":
                (new_G, new_beta) = hard_lockdown(G3, beta)
            elif lockdown_type == "Soft":
                (new_G, new_beta) = soft_lockdown(G3, beta)
            else:
                (new_G, new_beta) = (G3, beta)

            new_G, time, case_dict = SEIR(new_G, new_beta, case_dict, start_time=lockdown_start_date)

            filename = 'outputs/n={0}_type={1}_start={2}_avg_dig={3}.csv'.format(n, lockdown_type, lockdown_start_date, avg_dig)
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                for key, value in case_dict.items():
                    writer.writerow([key, value])


    return None


n=10000
k=20 # number of connection per node
p=0.5
# Only ome of lockdown_starts and lockdown_types should take multiple values.
lockdown_starts=[30]
lockdown_types= ["NA", "Soft", "Hard"]
#lockdown_types = ["Soft"]

G = nx.watts_strogatz_graph(n, k, p, seed=None)
#G = nx.barabasi_albert_graph(n, k)
#G = nx.erdos_renyi_graph(n, prob)
run_simulation(G, lockdown_starts, lockdown_types, beta=0.45)




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


