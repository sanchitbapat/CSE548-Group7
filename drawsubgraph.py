# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 00:48:13 2016

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
#        G1.add_edge(int(doc['attack_graph']['arcs']['arc'][i]['src']),int(doc['attack_graph']['arcs']['arc'][i]['dst']))
Gr=nx.Graph()
redfile = open("/home/hduser1/red/part-00000", "r")
for i in redfile.readlines():
    Gr.add_edge(int(i.split(",")[0].strip()),int(i.split(",")[1].strip()))

for i in Gr.nodes():
    Gr.node[i]['color']=str('red')

write_dot(Gr, 'redGraph.dot')
redfile.close()

Gn=nx.Graph()
greenfile = open("/home/hduser1/green/part-00000", "r")
for i in greenfile.readlines():
    Gn.add_edge(int(i.split(",")[0].strip()),int(i.split(",")[1].strip()))

for i in Gn.nodes():
    Gn.node[i]['color']=str('green')

write_dot(Gn, 'greenGraph.dot')
greenfile.close()

Gb=nx.Graph()
bluefile = open("/home/hduser1/blue/part-00000", "r")
for i in bluefile.readlines():
    Gb.add_edge(int(i.split(",")[0].strip()),int(i.split(",")[1].strip()))

for i in Gb.nodes():
    Gb.node[i]['color']=str('blue')

write_dot(Gb, 'blueGraph.dot')
bluefile.close()