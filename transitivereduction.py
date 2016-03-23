# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 19:29:30 2016

@author: hduser1
"""

import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import metis
import xmltodict
import json
import os
import sys


#mainGraph=open("/home/hduser1/AttackGraph.xml")
#doc=xmltodict.parse(mainGraph.read())
#G1=nx.Graph()
#for i in range(0,len(doc['attack_graph']['arcs']['arc'])):
 #       G1.add_edge(int(doc['attack_graph']['arcs']['arc'][i]['src']),int(doc['attack_graph']['arcs']['arc'][i]['dst']))

G=nx.Graph()
redfile = open("/home/hduser1/red/part-00000", "r")
for i in redfile.readlines():
    G.add_edge(int(i.split(",")[0].strip()),int(i.split(",")[1].strip()))
    
    
#G=nx.directed(G)
#G.add_edges_from()
#print len(G1.edges())
#G=G.to_directed()
#G = Graph()
#N = G1.nodes()
#for  x in N:
 #  for y in N:
  #    for z in N:
   #      #print("(%d,%d,%d)" % (x,y,z))
    #     if (x,y) != (y,z) and (x,y) != (x,z):
     #        if (x,y) in G1.edges() and (y,z) in G1.edges():
      #           print "abc "+str(x)+","+str(z)
       #          if (x,z) in G1.edges():
        #             print (x,z)
         #            G1.remove_edge(x,z)
                
#print nx.minimum_cut(G)
G1=nx.minimum_spanning_tree(G)
write_dot(G1, 'reduc.dot')

print "Removed edges:"
#print G.removed_edges
print "Remaining edges:"
print len(G1.edges())
