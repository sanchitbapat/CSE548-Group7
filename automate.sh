#!/bin/bash

#ssh slave5 "ls; cd /usr/lib/testFolder/; ls; echo 12345678 | sudo -S rm -rf test1; ls"

echo "Begin Graph partitioning"

SECONDS=0
python conditioninfo.py
timeToPartition=$SECONDS

echo "Graph partitioning complete"

cd /usr/local/hadoop/bin/

echo "Deleting files on HDFS"

./hadoop dfs -rmr /user/hadoop/*.csv

echo "Uploading new files to HDFS"

./hadoop fs -put ~/allNodes.csv /user/hadoop/allNodes.csv
./hadoop fs -put ~/allEdges.csv /user/hadoop/allEdges.csv
./hadoop fs -put ~/otherEdges.csv /user/hadoop/otherEdges.csv
./hadoop fs -put ~/greenEdges.csv /user/hadoop/greenEdges.csv
./hadoop fs -put ~/blueEdges.csv /user/hadoop/blueEdges.csv
./hadoop fs -put ~/redEdges.csv /user/hadoop/redEdges.csv
./hadoop fs -put ~/greenGraph.csv /user/hadoop/greenGraph.csv
./hadoop fs -put ~/blueGraph.csv /user/hadoop/blueGraph.csv
./hadoop fs -put ~/redGraph.csv /user/hadoop/redGraph.csv

echo "Upload Complete"
echo "Refreshing Ganglia"

cd /var/lib/ganglia/rrds/
echo 12345678 | sudo -S rm -rf myCluster/ __SummaryInfo__/

ssh slave1 "cd /var/lib/ganglia/rrds/; echo 12345 | sudo -S rm -rf myCluster/ __SummaryInfo__/"

ssh slave2 "cd /var/lib/ganglia/rrds/; echo 12345 | sudo -S rm -rf myCluster/ __SummaryInfo__/"

sleep 5

echo -e "\nStarting merge process on RDDs\n"
cd ~/spark/bin/

SECONDS=0
./pyspark ~/processing.py
timeToMerge=$SECONDS

echo -e "\nMerge Complete\n"

echo "Time to partition is $timeToPartition seconds"
echo "Time to merge is $timeToMerge seconds"
