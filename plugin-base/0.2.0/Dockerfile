FROM ubuntu:20.04

LABEL version="0.2.0" \
      description="Ubuntu 20.04 based plugin image"

RUN apt-get update\
  && apt-get install -y \
  python3 \
  git \
  python3-pip \
  nano \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir numpy

