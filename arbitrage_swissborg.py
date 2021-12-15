#!/usr/bin/env python
# coding: utf-8

import urllib.request as url
import json
import re
import math

# Method to return the rates from the API
def get_raw_rates():
    page = url.urlopen("http://fx.priceonomics.com/v1/rates/?q=1")
    rates = json.loads(page.read())
    return rates


# Method to return a list of lists which contain the currencies as well as the 'logified' conversion rate 
def clean_rates(rates):
    rates_clean = []
    for key in rates:
        a = key.split("_")
        b = [a[0],a[1],-1*math.log(float(rates[key]))]
        rates_clean.append(b)
    return rates_clean


# Define class Edge: a array which contains: the source currency name(u), the destination currency name(v) and the distance between the nodes  
class Edge:
    def __init__(self):
        self.curr_in = 0
        self.curr_out = 0
        self.distance = 0


# Define class Graph: a set of values which will contain all the necessary data 
class Graph:
    def __init__(self):
        self.Nodes = 0
        self.Edges = 0
        self.edge = []


# Method to instanciate a graph given parameters
def build_graph(N, E):
    graph = Graph()
    graph.Nodes = N
    graph.Edges = E
    for i in range(0,E):
        graph.edge.append(Edge())
    return graph

# Method to return the key in integer from the index, a dictionary which contains each currency associated to a unique key
def get_curr_int(val,index):
    for key, value in index.items():
         if val == value:
            return key

# function to return currency name given an integer, i just created this method to have consistency in naming when using the index
def get_curr_str(loop,index):
    new_loop = []
    for i in loop:
        new_loop.append(index[i])
    return new_loop

# Method to loop through the list of predessors of list of closest nodes to identify the negative loop that can be used to exploit arbitrage
def get_path_negative_loop(pred, src_currency):
    path = [src_currency]
    next_node = src_currency
    while pred:
        next_node = pred[next_node]
        if next_node not in path:
            path.append(next_node)
        else:
            path.append(next_node)
            path = path[path.index(next_node):]
            return path

#  Method called relaxation which will assign a new value when the distance of the currency out to the source if a smaller path has been found
#  For each edge, curr_in is the currency being exchanged and curr_out is the currency post exchange, weight is the transformed exchange rate (-log(rates))
#  If the distance between curr_out and the source currency is superior than the one currently established + the weight of the exchange rate then it is updated, in parallel we also store the name of the currency being exchanged
def relax(dist, pred, curr_in, curr_out, weight):
    if ((dist[curr_out] > dist[curr_in] + weight)and (dist[curr_in] != math.inf)):
        dist[curr_out] = dist[curr_in] + weight
        pred[curr_out] = curr_in

# Method which aims to represent the algo of Bellman-Ford
# Initialization: here we setup 2 lists:
#     - 'dist' is the list which contains the distance between the node[src_currency] and all the other nodes (we setup all distance to infinity since we don't know them apart from the src_currency which is set to 0)
#     - 'pred' is the list which contains the name of currency is being exchanged (which 'starts' the negative loop)
def bellmanford_negative_loop(graph, src_currency):
    N = graph.Nodes
    E = graph.Edges
    dist = [math.inf]*N
    pred = [None]*N
    dist[src_currency] = 0

# First loop which will parse the different edges and 'relax' each of them given a source node as input to calculate the shortest path to this source from each node
    for i in range(0,N):
        for j in range(E):
            curr_i = graph.edge[j].curr_in
            curr_o = graph.edge[j].curr_out
            weight = graph.edge[j].distance
            relax(dist, pred, curr_i, curr_o, weight)

# This part will check and actually return the shortest path possible
    for i in range(E):
        curr_i = graph.edge[i].curr_in
        curr_o = graph.edge[i].curr_out
        weight = graph.edge[i].distance
        if (dist[curr_i] != math.inf and dist[curr_i] + weight < dist[curr_o]):
            return True, get_path_negative_loop(pred,src_currency)
    return False, None


def Main():
    raw_rates = get_raw_rates()
    cleaned_rates = clean_rates(raw_rates)
    nodes = []
    for key in cleaned_rates:
        if key[0] not in nodes:
            nodes.append(key[0])
    keys = [i for i in range(len(nodes))]
# Creation of a dictionnary which contains the currency name(nodes) as well as its identifier used in the graph(key)
    index = dict(zip(keys,nodes))
    amount_of_nodes = len(nodes)
    amount_of_edges = len(cleaned_rates)
    graph = build_graph(amount_of_nodes,amount_of_edges)

# fill the graph with each edge
    for i in range(graph.Edges):
        graph.edge[i].curr_in = get_curr_int(cleaned_rates[i][0],index)
        graph.edge[i].curr_out = get_curr_int(cleaned_rates[i][1],index)
        graph.edge[i].distance = cleaned_rates[i][2]

# Starting from each node, run the Bellman-Ford algorithm to detect different cycles which could lead to arbitrage path
    negative_loops = []
    for i in range(graph.Nodes):
        currency = index[i]
        status, negative_loop = bellmanford_negative_loop(graph,i)
        if status == True:
            if negative_loop not in negative_loops and not None:
                negative_loops.append(negative_loop)
        else:
            print("No opportunity seen when starting with ",currency,)

# Display the identified loops with the currency name
    cleaned_loop = []
    for i in range(len(negative_loops)):
        a=get_curr_str(negative_loops[i],index)
        cleaned_loop.append(a)
    print(cleaned_loop)

# Parse the identified loops to show the benefit that can be made
    for single_loop in cleaned_loop:
        benefits = []
        print('\nNew opportunity detected:')
        for curr, next in zip(single_loop, single_loop[1:]):
            for i in range(amount_of_edges):
                if (cleaned_rates[i][0] == curr and cleaned_rates[i][1] == next):
                    rate = math.exp(-cleaned_rates[i][2])
                    benefits.append(rate)
                    print ('From ',curr,' to ',next,' with rate: ',rate)
        print ('Benefit:',math.prod(benefits))

# Execute the main
Main()
