FROM alpine:3.10.2

LABEL version="0.1.0" \
      description="Alpine based plugin image"

RUN apk update\
  && apk --no-cache add \
  python3 \
  git \
  py3-pip \
  nano \
  py3-numpy
