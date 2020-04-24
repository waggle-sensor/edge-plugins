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

echo "--------------"
echo $input_format
echo $video_size
echo $unparsed_parameters
echo "------------"
echo $@

cp _ffserver.conf a.conf
sed -i "s/\FORMAT/${input_format}/" a.conf
sed -i "s/VIDEO_SIZE/${video_size}/" a.conf

