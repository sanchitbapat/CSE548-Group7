#! /usr/bin/env python
import networkx as nx
import xmltodict
with open('/home/sanchit/mulval/AttackGraph.xml') as fd:

	doc=xmltodict.parse(fd.read())
	G=nx.Graph()
	for i in range(0,200):
		G.add_edge(str(doc['attack_graph']['arcs']['arc'][i]['src']),str(doc['attack_graph']['arcs']['arc'][i]['dst']))
#	print G.edges()
	print G.nodes()
