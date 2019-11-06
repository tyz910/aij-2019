FROM ubuntu:18.04

ENV LANG=C.UTF-8 \
    ENV_DOCKER=1

# Common packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        build-essential \
        vim \
        wget \
        curl \
        git \
        swig \
        libomp-dev \
        libopenblas-dev \
        zip \
        unzip && \
    rm -rf /var/lib/apt/lists/*

# Python 3.6
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3.6 \
        python3.6-dev \
        python3.6-venv && \
    pip3 install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python

# Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt

RUN curl -sL https://github.com/dangerink/udpipe/archive/load_binary.zip -o /tmp/udpipe.zip && cd /tmp && \
    unzip -qo /tmp/udpipe.zip && cd /tmp/udpipe-load_binary/releases/pypi && ./gen.sh 1.2.0.1.0 && cd ufal.udpipe && \
    python3 setup.py install && cd /tmp && rm -rf /tmp/udpipe*

COPY dev/install.py /var/install.py
RUN python3 /var/install.py

COPY var/model/bert /var/model/bert
COPY var/sberbank /var/sberbank
