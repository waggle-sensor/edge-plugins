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

# support video/audio/image streams
if [[ "${input_format}x" == "mp3x" ]]; then
  cat << EOF >> /etc/ffserver.conf
<Stream live>
Feed feed1.ffm
Format ${input_format}
AudioBitRate 192
AudioChannels 1
AudioSampleRate 44100
NoVideo
</Stream>
EOF
else
  cat << EOF >> /etc/ffserver.conf

<Stream live>
Feed feed1.ffm
Format ${input_format}
NoAudio
VideoBitRate 2000
VideoBufferSize 8000
VideoFrameRate 10
VideoSize ${video_size}
VideoGopSize 12
</Stream>
EOF
fi

mkdir -p /var/run/waggle
server_pid=/var/run/waggle/ffserver.pid
input_pid=/var/run/waggle/ffmpeg.pid

clean_up() {
  if [ -e ${server_pid} ] ; then
    if ps -p $(cat ${server_pid}) > /dev/null 2>&1 ; then
      kill -9 $(cat ${server_pid})
    fi
  fi
  if [ -e ${input_pid} ] ; then
    if ps -p $(cat ${input_pid}) > /dev/null 2>&1 ; then
      kill -9 $(cat ${input_pid})
    fi
  fi
}

spin_up() {
  ffserver &
  echo $! > ${server_pid}
  sleep 1
  ffmpeg -loglevel panic $@ http://localhost:8090/feed1.ffm &
  echo $! > ${input_pid}
  sleep 5
}

sigint() {
  echo "interrupted!"
  clean_up
  exit 0
}

trap sigint SIGINT

clean_up
spin_up

while :;
do
  # do server check
  return_code=$(curl \
    --write-out %{http_code} \
    --silent \
    --output /dev/null \
    http://localhost:8090/stat.html
  )
  # if return code is 2XX
  if [[ ${return_code} =~ ^[2]{1} ]]; then
    :
  else
    clean_up
    spin_up $@
    continue
  fi

  # do input feeder check
  # TODO: This does not run, i.e. uses 0 % CPU.
  #       Do not know why.
  # timeout 30 ffmpeg \
  #   -loglevel panic \
  #   -i http://localhost:8090/live \
  #   -frames 1 \
  #   -vcodec copy \
  #   -acodec copy \
  #   -f null /dev/null 2>&1
  # if [ $? -eq 0 ]; then
  #   :
  # else
  #   clean_up
  #   spin_up $@
  # fi
  # or simply check it from stat.html
  receive_data=$(curl \
    --silent \
    http://localhost:8090/stat.html | \
    grep RECEIVE_DATA
  )
  if [[ "${receive_data}x" == "x" ]]; then
    clean_up
    spin_up $@
  else
    :
  fi
  sleep 60
done
