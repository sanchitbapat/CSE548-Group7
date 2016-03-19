#! /usr/bin/env python
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import metis
import xmltodict
with open('/home/sanchit/mulval/AttackGraph.xml') as fd:

	doc=xmltodict.parse(fd.read())
	G=nx.Graph()
	for i in range(0,200):
		G.add_edge(int(doc['attack_graph']['arcs']['arc'][i]['src']),int(doc['attack_graph']['arcs']['arc'][i]['dst']))
#	print G.edges()
#	print G.nodes()
	(edgecuts, parts) = metis.part_graph(G, 3)
	colors = ['red','blue','green']
#	for i, p in enumerate(parts):
#	     G.node[i+1]['color'] = colors[1]
#	write_dot(G, 'before.dot')
	for i, p in enumerate(parts):
	     G.node[i+1]['color'] = colors[p]
#		print G.node[i+1]
#	print G2.edges()
#	print G.node[0]
	write_dot(G, 'clusteredGraph.dot')
