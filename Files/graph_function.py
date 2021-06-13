# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 00:44:16 2020

@author: liece
"""
from networkx.algorithms.flow import maximum_flow
import networkx as nx



def create_bigraph(source,target,start_city,final_city,p,p_equi,size,subTable):
    """
    Permet de créer un bigraphn comme spécifié par la librairie de networkx,
    Nous avons donc un bigraphe avec les villes d'entrée reliée à la source
    avec leur pi assigné, les villes d'entrée reliée au villes de sortie avec 
    leur cout associé dans la table et les villes de sorties reliée au puit
    avec leur capacité de sortie équilibré'
    """
    G = nx.DiGraph()

    G.add_nodes_from(start_city)
    G.add_nodes_from(final_city)    
    G.add_nodes_from([source,target])
    #We'll use networkx to display our max flow min cost problem
    
    #We define a source and a target
    #The edges s -> city will have the capacity defined in our random p line 119
    edges = []
    for i in range(size):
        edges.append((source,start_city[i],{"capacity":int(p[i])}))
        edges.append((final_city[i],target,{"capacity":int(p_equi[i])}))
    #Creatings edges from sources to targets, with the subtable cost given
    for i in range(size):
        for j in range(size):
            edges.append((start_city[i],final_city[j],{"weight":int(subTable[i][j])}))
    
    G.add_edges_from(edges)
    
    return G
def max_flot_min_cost(G,source,target):
    """
    Appelle la fonction max_flow_min_cost de networkx pour calculer le cout
    de notre solution de flot maximale
    """
    mincostFlow = nx.max_flow_min_cost(G, source, target)#compute maxflow
    return nx.cost_of_flow(G, mincostFlow)