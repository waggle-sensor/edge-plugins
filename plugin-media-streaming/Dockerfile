FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y \
  ffmpeg \
  nano \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY _ffserver.conf stream.sh /app/

ENTRYPOINT ["/bin/bash", "stream.sh"]
