FROM waggle/plugin-base:0.1.0

RUN apt-get update \
  && apt-get install -y \
  ffmpeg \
  curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY _ffserver.conf stream.sh /app/

ENTRYPOINT ["/bin/bash", "/app/stream.sh"]
