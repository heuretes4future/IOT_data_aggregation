FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    python3 \
    python3-pip \
    tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Stockholm /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz && \
    tar -xzvf hadoop-3.3.0.tar.gz && \
    mv hadoop-3.3.0 /usr/local/hadoop && \
    rm hadoop-3.3.0.tar.gz

ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

RUN pip3 install geopy

RUN mkdir -p /app/hadoop_jobs

COPY mapper.py /app/hadoop_jobs/
COPY reducer.py /app/hadoop_jobs/

WORKDIR /app/hadoop_jobs/

CMD ["/bin/bash"]
