#! /usr/bin/env python
import networkx as nx
import xmltodict
import os
from networkx.drawing.nx_pydot import write_dot
import metis
    
attackGraph = open("/home/hduser1/AttackGraphS2.xml", "r")

doc=xmltodict.parse(attackGraph.read())
# Construct the Graph using NetworkX
G=nx.Graph()
for i in range(0,len(doc['attack_graph']['arcs']['arc'])):
    G.add_edge(int(doc['attack_graph']['arcs']['arc'][i]['src']),int(doc['attack_graph']['arcs']['arc'][i]['dst']))


#Divide the graph into 3 clusters using PyMetis and color each cluster
(edgecuts, parts) = metis.part_graph(G, 3)
colors = ['red','blue','green']
for i, p in enumerate(parts):
    G.node[i+1]['color'] = colors[p]
    

greenEdges=open('greenEdges.csv','w')
redEdges=open('redEdges.csv','w')
blueEdges=open('blueEdges.csv','w')
otherEdges=open('otherEdges.csv','w')
allEdges=open('allEdges.csv','w')
allNodes=open('allNodes.csv','w')


for i in G.edges():
    if str(G.node[i[0]]['color'])==str(G.node[i[1]]['color']):
        if str(G.node[i[0]]['color'])==str('green'):
            greenEdges.write(str(i[0])+","+str(i[1])+"\n")
        elif str(G.node[i[0]]['color'])==str('blue'):
            blueEdges.write(str(i[0])+","+str(i[1])+"\n")
        elif str(G.node[i[0]]['color'])==str('red'):
            redEdges.write(str(i[0])+","+str(i[1])+"\n")
    else:
        otherEdges.write(str(i[0])+","+str(i[1])+"\n")
    allEdges.write(str(i[0])+","+str(i[1])+"\n")

greenEdges.close() 
blueEdges.close()
redEdges.close()
allEdges.close()
#attackGraph.close()
write_dot(G, 'fullGraph.dot')
#
greenGraph={}
blueGraph={}
redGraph={}
#
##Save the pre/post condition information for each node
#
for i in G.nodes():
    allNodes.write(str(i)+","+str(G.node[i]['color'])+"\n")
    node=str(doc['attack_graph']['vertices']['vertex'][i-1]['fact'])
    if  node.find("exec")!=-1 or node.find("principal")!=-1 or node.find("netAccess")!=-1 or node.find("canAccess")!=-1:
        if G.node[i]['color']==str('green'):
            greenGraph[i]=str('post')
        elif G.node[i]['color']==str('blue'):
            blueGraph[i]=str('post')
        elif G.node[i]['color']==str('red'):
            redGraph[i]=str('post')
    else:
        if G.node[i]['color']==str('green'):
            greenGraph[i]=str('pre')
        elif G.node[i]['color']==str('blue'):
            blueGraph[i]=str('pre')
        elif G.node[i]['color']==str('red'):
            redGraph[i]=str('pre')

#for i in G.edges():
#    print G.edge[i]

redFile=open('redGraph.csv','w')
for i in redGraph:
    redFile.write(str(i)+","+redGraph[i]+"\n")

blueFile=open('blueGraph.csv','w')
for i in blueGraph:
    blueFile.write(str(i)+","+blueGraph[i]+"\n")
    
greenFile=open('greenGraph.csv','w')
for i in greenGraph:
    greenFile.write(str(i)+","+greenGraph[i]+"\n")
    
greenFile.close()
blueFile.close()
redFile.close()
allNodes.close()
attackGraph.close()