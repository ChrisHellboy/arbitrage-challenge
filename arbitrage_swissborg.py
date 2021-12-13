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


# Method to convert the currency to int, it will be used to help with the parsing of the lists
def convert_to_int(currency):
    if currency == 'USD': 
        return 0
    elif currency == 'EUR':
        return 1
    elif currency == 'JPY':
        return 2
    elif currency == 'BTC':
        return 3


# Method to convert the int back to string when all the negative loops are discovered
def convert_to_str(currency):
    if currency == 0: 
        return 'USD'
    elif currency == 1:
        return 'EUR'
    elif currency == 2:
        return 'JPY'
    elif currency == 3:
        return 'BTC'


# Method to loop through the list of predessors to identify the negative loop that can be used to exploit arbitrage
def retrace_negative_loop(p, start):
    arbitrageLoop = [start]
    next_node = start
    while True:
        next_node = p[next_node]
        if next_node not in arbitrageLoop:
            arbitrageLoop.append(next_node)
        else:
            arbitrageLoop.append(next_node)
            arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
            return arbitrageLoop



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

# First loop 
    for i in range(1,N):
        for j in range(E):
            curr_i = graph.edge[j].curr_in
            curr_o = graph.edge[j].curr_out
            weight = graph.edge[j].distance
            relax(dist, pred, curr_i, curr_o, weight)
            
# This part will check       
    for i in range(E):
        curr_i = graph.edge[i].curr_in
        curr_o = graph.edge[i].curr_out
        weight = graph.edge[i].distance
        if (dist[curr_i] != math.inf and dist[curr_i] + weight < dist[curr_o]):
            return True, retrace_negative_loop(pred,src_currency)
    return False, None


def Main():
    raw_rates = get_raw_rates()
    cleaned_rates = clean_rates(raw_rates)
    amount_of_nodes = 4
    amount_of_edges = 16
    graph = build_graph(4,16)
    
# fill the graph with each edge
    for i in range(graph.Edges):
        graph.edge[i].curr_in = convert_to_int(cleaned_rates[i][0])
        graph.edge[i].curr_out = convert_to_int(cleaned_rates[i][1])
        graph.edge[i].distance = cleaned_rates[i][2]
        
# Starting from each node, run the Bellman-Ford algorithm to detect different cycles which could lead to arbitrage
    negative_loops = []
    for i in range(graph.Nodes):
        currency = convert_to_str(i)
        status, negative_loop = bellmanford_negative_loop(graph,i)
        if status == True:
            if negative_loop not in negative_loops and not None:
                negative_loops.append(negative_loop)
        else:
            print("No opportunity seen when starting with ",currency,)
# Display the identified loops with the currency name
    cleaned = []
    for i in range(len(negative_loops)):
        a=list(map(convert_to_str,negative_loops[i]))
        cleaned.append(a)
    print(cleaned)  

Main()
