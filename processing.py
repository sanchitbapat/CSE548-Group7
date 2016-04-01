# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:49:41 2016

@author: hduser1
"""

import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import re
import sys
from operator import add
#from pyspark import hdfs

from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName("graph processing").setMaster("spark://192.168.0.13:7077")
sc = SparkContext(conf=conf)

#Graphs with pre post
#g1=sc.textFile("/home/hduser1/g1.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
#g2=sc.textFile("/home/hduser1/g2.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#
#Edges
#e1=sc.textFile("/home/hduser1/e1.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#e2=sc.textFile("/home/hduser1/e2.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#e3=sc.textFile("/home/hduser1/e3.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#all the nodes with color
#allNodes=sc.textFile("/home/hduser1/allNodes.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#for hadoop
allNodes=sc.textFile("hdfs://master:54310/user/hadoop/allNodes.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#Edges
#allEdges=sc.textFile("/home/hduser1/allEdges.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
#greenEdges=sc.textFile("/home/hduser1/greenEdges.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#blueEdges=sc.textFile("/home/hduser1/blueEdges.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#redEdges=sc.textFile("/home/hduser1/redEdges.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
#otherEdges=sc.textFile("/home/hduser1/otherEdges.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#for hadoop
allEdges=sc.textFile("hdfs://master:54310/user/hadoop/allEdges.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
greenEdges=sc.textFile("hdfs://master:54310/user/hadoop/greenEdges.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
blueEdges=sc.textFile("hdfs://master:54310/user/hadoop/blueEdges.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
redEdges=sc.textFile("hdfs://master:54310/user/hadoop/redEdges.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1]))
otherEdges=sc.textFile("hdfs://master:54310/user/hadoop/otherEdges.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#Graph with pre post
#greenGraph=sc.textFile("/home/hduser1/greenGraph.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
#blueGraph=sc.textFile("/home/hduser1/blueGraph.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
#redGraph=sc.textFile("/home/hduser1/redGraph.txt").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

#for hadoop
greenGraph=sc.textFile("hdfs://master:54310/user/hadoop/greenGraph.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
blueGraph=sc.textFile("hdfs://master:54310/user/hadoop/blueGraph.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()
redGraph=sc.textFile("hdfs://master:54310/user/hadoop/redGraph.csv").map(lambda line: line.split(",")).map(lambda line: (line[0],line[1])).collect()

nodelist=()
for nodeG,conditionG in greenGraph:
    if conditionG==str('post'):
        for node1,node2 in otherEdges:
            if str(node1)==str(nodeG):
                nodelist=nodelist+((node1,node2),)
                

for nodeG,conditionG in redGraph:
    if conditionG==str('post'):
        for node1,node2 in otherEdges:
            if str(node1)==str(nodeG):
                nodelist=nodelist+((node1,node2),)
                
                
for nodeG,conditionG in blueGraph:
    if conditionG==str('post'):
        for node1,node2 in otherEdges:
            if str(node1)==str(nodeG):
                nodelist=nodelist+((node1,node2),)


lostEdges={}
lostMap=()
for node1,node2 in otherEdges:
    flag=True
    for i in nodelist:
        if str(node1)==str(i[0]) and str(node2)==str(i[1]):
            flag=False
    if flag:
        lostEdges[str(node1)+","+str(node2)]=str(node1)+","+str(node2)
        lostMap=lostMap+((node1,node2),)

#print len(otherEdges)
#print len(nodelist)
#print len(lostEdges.keys())
#print len(lostMap)
#lostInfo=open('/home/hduser1/lostinfo.txt','w')
##lostInfo2=open('/home/hduser1/lostinfo2.txt','w')
#for i in lostEdges.keys():
#    lostInfo.write(str(i[0])+","+str(i[1])+"\n")
#lostInfo.close()

#for 

G=nx.Graph()
for node1,node2 in allEdges:
    G.add_edge(int(node1),int(node2))

for node,color in allNodes:
    G.node[int(node)]['color'] = str(color)

print "Edges "+str(len(G.edges()))+" Nodes "+str(len(G.nodes()))

for i in lostMap:
    G.remove_edge(int(i[0]),int(i[1]))

print "Edges "+str(len(G.edges()))+" Nodes "+str(len(G.nodes()))

write_dot(G, '/home/hduser1/finalGraph.dot')


finalRdd=sc.parallelize(G.edges()).repartition(1).saveAsTextFile("hdfs://master:54310/user/hadoop/finalGraph.csv")
#e1.filter(lambda e:(e[0])=>e3)
#e4=e3.filter(lambda e:e[1]==(e1.filter(lambda l:l[0]))).map(lambda e: (e[0],e[1])).collect()

sc.stop()