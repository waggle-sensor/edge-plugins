FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y \
  ffmpeg \
  nano \
  && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash", "stream.sh"]
