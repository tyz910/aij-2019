FROM ubuntu:18.04

ENV LANG=C.UTF-8

# Common packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        build-essential \
        vim \
        wget \
        curl \
        git \
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
    rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip3 install --no-cache-dir --upgrade tensorflow==1.14
RUN pip3 install --no-cache-dir --upgrade torch==1.2
RUN pip3 install --no-cache-dir --upgrade keras-preprocessing==1.1
RUN pip3 install --no-cache-dir --upgrade flask==1.1
RUN pip3 install --no-cache-dir --upgrade nltk==3.4
RUN python3 -m nltk.downloader punkt
RUN pip3 install --no-cache-dir --upgrade pytorch_transformers==1.2
RUN pip3 install --no-cache-dir --upgrade lightgbm==2.2

COPY var/model/bert /var/model/bert

RUN pip3 install --no-cache-dir --upgrade pandas==0.25
RUN pip3 install --no-cache-dir --upgrade deeppavlov sortedcontainers kenlm

COPY dev/install/spelling_correction.py /var/install/spelling_correction.py
RUN python3 /var/install/spelling_correction.py

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        swig && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN curl -sL https://github.com/dangerink/udpipe/archive/load_binary.zip -o /tmp/udpipe.zip &&     cd /tmp &&     unzip -qo /tmp/udpipe.zip  &&     cd /tmp/udpipe-load_binary/releases/pypi &&     ./gen.sh 1.2.0.1.0 &&     cd ufal.udpipe &&     python3 setup.py install &&     cd /tmp &&     rm -rf /tmp/udpipe*
RUN pip3 install --no-cache-dir numpy==1.17.2 scipy sklearn pandas==0.24.2 nltk==3.2.5 gensim==3.8.0 torch catboost pytorch_pretrained_bert==0.6.2 matplotlib==3.0.3 python-Levenshtein sklearn_crfsuite fastai fuzzywuzzy keras tqdm pymorphy2 summa pymystem3 pymorphy2 pymorphy2-dicts-ru jellyfish flask requests tensorflow
RUN python -c "import pymystem3.mystem ; pymystem3.mystem.autoinstall()"
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt');"
ENV ENV_DOCKER=1
COPY var/sberbank /var/sberbank

RUN pip3 install sentencepiece tf-sentencepiece tensorflow-hub
COPY dev/install/universal_sentence_encoder.py /var/install/universal_sentence_encoder.py
RUN python3 /var/install/universal_sentence_encoder.py

RUN pip3 install faiss

RUN pip3 install pybind11==2.2.3
RUN pip3 install git+https://github.com/deepmipt/fastText.git#egg=fastText==0.8.22

COPY dev/install/ner.py /var/install/ner.py
RUN python3 /var/install/ner.py

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libomp-dev \
        libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install russtress
