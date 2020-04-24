#!/bin/bash

unparsed_parameters=()
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    -input_format)
    input_format="$2"
    shift
    shift
    ;;
    -video_size)
    video_size="$2"
    shift
    shift
    ;;
    *)
    unparsed_parameters+=("$1")
    shift
    ;;
  esac
done
set -- "${unparsed_parameters[@]}"

cp _ffserver.conf /etc/ffserver.conf
sed -i \
  -e "s/\FORMAT/${input_format}/" \
  -e "s/VIDEO_SIZE/${video_size}/" \
  /etc/ffserver.conf

ffserver &
sleep 1
ffmpeg -loglevel panic $@ http://localhost:8090/feed1.ffm
