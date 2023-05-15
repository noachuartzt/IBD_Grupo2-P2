FROM openjdk:8-jre-slim

# -- Layer: OS + Python 3.9

ARG shared_workspace=/opt/workspace

RUN mkdir -p ${shared_workspace} && \
    apt-get update -y && \
	apt install -y curl gcc &&\ 
	apt install -y build-essential zlib1g-dev libncurses5-dev && \
	apt install -y libsqlite3-dev && \
	apt install -y libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget libjpeg-dev && \
	curl -O https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz  && \
    tar -xf Python-3.9.7.tar.xz && cd Python-3.9.7 && ./configure && make -j 8 &&\
    make install && \
    apt-get update && apt-get install -y procps && apt-get install -y vim && apt-get install -y net-tools && \
    rm -rf /var/lib/apt/lists/*

ENV SHARED_WORKSPACE=${shared_workspace}

ARG spark_version=3.4.0
ARG hadoop_version=3

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

# -- Runtime

WORKDIR ${SPARK_HOME}

VOLUME ${shared_workspace}
CMD ["bash"]
