#!/bin/bash

for i in {2002..2016}
do
	echo $i
	curl http://localhost/nvdcve-2.0-$i.xml | nvd2sqlite3 -d data.db
done
curl http://localhost/nvdcve-2.0-Modified.xml | nvd2sqlite3 -d data.db
curl http://localhost/nvdcve-2.0-Recent.xml | nvd2sqlite3 -d data.db
