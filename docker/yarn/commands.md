<!-- MAC -->
```bash	
cd base/arm
docker build -t bigdatainf/hadoop-base:3.3.5 .
cd ../../namenode
docker build -t bigdatainf/hadoop-namenode:3.3.5 .
cd ../datanode
docker build -t bigdatainf/hadoop-datanode:3.3.5 .
cd ../resourcemanager
docker build -t bigdatainf/hadoop-resourcemanager:3.3.5 .
cd ../nodemanager
docker build -t bigdatainf/hadoop-nodemanager:3.3.5 .
cd ../historyserver
docker build -t bigdatainf/hadoop-historyserver:3.3.5 .

docker tag bigdatainf/hadoop-namenode:3.3.5 noachuartzt/ibd-g2_hadoop-namenode_mac:3.3.5
docker tag bigdatainf/hadoop-datanode:3.3.5 noachuartzt/ibd-g2_hadoop-datanode_mac:3.3.5
docker tag bigdatainf/hadoop-resourcemanager:3.3.5 noachuartzt/ibd-g2_hadoop-resourcemanager_mac:3.3.5
docker tag bigdatainf/hadoop-nodemanager:3.3.5 noachuartzt/ibd-g2_hadoop-nodemanager_mac:3.3.5
docker tag bigdatainf/hadoop-historyserver:3.3.5 noachuartzt/ibd-g2_hadoop-historyserver_mac:3.3.5

docker push noachuartzt/ibd-g2_hadoop-namenode_mac:3.3.5
docker push noachuartzt/ibd-g2_hadoop-datanode_mac:3.3.5
docker push noachuartzt/ibd-g2_hadoop-resourcemanager_mac:3.3.5
docker push noachuartzt/ibd-g2_hadoop-nodemanager_mac:3.3.5
docker push noachuartzt/ibd-g2_hadoop-historyserver_mac:3.3.5

cd ../ibd-g2_Interface/mac
docker compose up 

```

<!-- WINDOWS -->
```bash
cd base/amd
docker build -t bigdatainf/hadoop-base:3.3.5 .
cd ../../namenode
docker build -t bigdatainf/hadoop-namenode:3.3.5 .
cd ../datanode
docker build -t bigdatainf/hadoop-datanode:3.3.5 .
cd ../resourcemanager
docker build -t bigdatainf/hadoop-resourcemanager:3.3.5 .
cd ../nodemanager
docker build -t bigdatainf/hadoop-nodemanager:3.3.5 .
cd ../historyserver
docker build -t bigdatainf/hadoop-historyserver:3.3.5 .

docker tag bigdatainf/hadoop-namenode:3.3.5 noachuartzt/ibd-g2_hadoop-namenode:3.3.5
docker tag bigdatainf/hadoop-datanode:3.3.5 noachuartzt/ibd-g2_hadoop-datanode:3.3.5
docker tag bigdatainf/hadoop-resourcemanager:3.3.5 noachuartzt/ibd-g2_hadoop-resourcemanager:3.3.5
docker tag bigdatainf/hadoop-nodemanager:3.3.5 noachuartzt/ibd-g2_hadoop-nodemanager:3.3.5
docker tag bigdatainf/hadoop-historyserver:3.3.5 noachuartzt/ibd-g2_hadoop-historyserver:3.3.5

docker push noachuartzt/ibd-g2_hadoop-namenode:3.3.5
docker push noachuartzt/ibd-g2_hadoop-datanode:3.3.5
docker push noachuartzt/ibd-g2_hadoop-resourcemanager:3.3.5
docker push noachuartzt/ibd-g2_hadoop-nodemanager:3.3.5
docker push noachuartzt/ibd-g2_hadoop-historyserver:3.3.5

cd ../ibd-g2_Interface/windows
docker compose up
 
```

s