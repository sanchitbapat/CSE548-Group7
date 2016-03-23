#! /usr/bin/env python
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import metis
import xmltodict
import json
import os
import sys
with open('AttackGraph.xml') as fd:
    doc=xmltodict.parse(fd.read())
    G=nx.Graph()
    for i in range(0,548):
        G.add_edge(int(doc['attack_graph']['arcs']['arc'][i]['src']),int(doc['attack_graph']['arcs']['arc'][i]['dst']))
    
	# print G.edges()
	# print G.nodes()
    (edgecuts, parts) = metis.part_graph(G, 3)
 #   print G.edge[1]
    print G.edge[2]
    print G.edges()[1]
#    for i, p in enumerate(parts):
#        print G.edge[i+1]
    colors = ['red','blue','green']
	# for i, p in enumerate(parts):
	# G.node[i+1]['color'] = colors[1]
	# write_dot(G, 'before.dot')
    for i, p in enumerate(parts):
        G.node[i+1]['color'] = colors[p]
    write_dot(G, 'before.dot')
    m={}
    for i in G.edges():
#        count=count+1
        if str(G.node[i[1]]['color']) == str(G.node[i[0]]['color']):
            m[i]=G.node[i[0]]['color']
        else:
            m[i]='black'
    #print m
    
    
    bb = nx.edge_betweenness_centrality(G, normalized=False)
    #print bb
    #print m
    nx.edge_betweenness_centrality(G, normalized=False)
    nx.set_edge_attributes(G, 'color', m)
    #print nx.get_edge_attributes(G,'color')
    
    nodeMap={}
    greenTuple=()
    blueTuple=()
    redTuple=()
    for i in G.nodes():
        if G.node[i]['color'] == str('green'):
            greenTuple=greenTuple+(i,)
        elif G.node[i]['color'] == str('blue'):
            blueTuple=blueTuple+(i,)
        elif G.node[i]['color'] == str('red'):
            redTuple=redTuple+(i,)
        #value=nodeMap[key]+",

    nodeMap['green']=greenTuple
    nodeMap['blue']=blueTuple
    nodeMap['red']=redTuple
    vertexFile = open("vertexData.csv", "w")
    edgeFile = open("edgeData.csv", "w")
    for i in nodeMap.keys():
        for j in nodeMap[i]:
            vertexFile.write(str(j)+","+i+"\n")
    vertexFile.close
    for i in G.edges():
        edgeFile.write(str(i[0])+","+str(i[1])+",color\n")
#    print len(greenTuple)+len(blueTuple)+len(redTuple)
            
    
    #write_dot(G, 'final.dot')
    
#    bb = nx.edge_betweenness_centrality(G, normalized=False)
#    nx.set_edge_attributes(G, 'betweenness', bb)
#    print G[1][2]['betweenness']
#    print G.node[1]
#    print len(G.nodes())
#    print len(G.edges())

#G.node[i+1]['color'] = colors[p]
	# print G.node[i+1]
	# print G2.edges()
	# print G.node[0]
#	write_dot(G, 'clusteredGraph.dot')
