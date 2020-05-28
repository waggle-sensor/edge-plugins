#!/bin/bash

help() {
  echo " Start ffserver and ffmpeg for feedding input to the server"
  echo " USAGE: stream.sh [OPTIONS] [FFMPEG PARAMS]"
  echo "    [OPTIONS]"
  echo "    -h            print usage"
  echo "    -verbose      print logs"
  echo "    -input_format input format of the source"
  echo "                  examples; mjpeg, mp4, mp3"
  echo "    -video_size   video size of the input"
}

unparsed_parameters=()
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    -h)
    help
    exit 0
    ;;
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
    -verbose)
    verbose="true"
    shift
    ;;
    *)
    unparsed_parameters+=("$1")
    shift
    ;;
  esac
done
#set -- "${unparsed_parameters[@]}"

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

print() {
  loglevel=$1
  message=$2
  echo "$(date) $loglevel $message"
}

clean_up() {
  if [ -e ${server_pid} ] ; then
    if ps -p $(cat ${server_pid}) > /dev/null 2>&1 ; then
      if [ ! -z $verbose ]; then
        print "INFO" "Attemping to kill ffserver..."
      fi
      kill -9 $(cat ${server_pid})
    fi
  fi
  if [ -e ${input_pid} ] ; then
    if ps -p $(cat ${input_pid}) > /dev/null 2>&1 ; then
      if [ ! -z $verbose ]; then
        print "INFO" "Attemping to kill the input feeder..."
      fi
      kill -9 $(cat ${input_pid})
    fi
  fi
}

spin_up() {
  if [ ! -z $verbose ]; then
    print "INFO" "Spinning up ffserver and input feeder..."
  fi
  ffserver &
  echo $! > ${server_pid}
  sleep 1
  ffmpeg -loglevel panic ${unparsed_parameters[@]} http://localhost:8090/feed1.ffm &
  echo $! > ${input_pid}
  sleep 5
}

sigint() {
  print "INFO" "Process interruppted! Halting..."
  clean_up
  exit 0
}

trap sigint SIGINT SIGTERM

print "INFO" "Starting..."

clean_up
spin_up
sleep 10

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
    if [ ! -z $verbose ]; then
      print "ERROR" "ffserver not responding!"
    fi
    clean_up
    spin_up
    continue
  fi

  # do input feeder check
  # NOTE: This only works
  #       when processed in background.
  ffmpeg \
    -loglevel panic \
    -i http://localhost:8090/live \
    -frames 1 \
    -vcodec copy \
    -acodec copy \
    -f null /dev/null &
  if [ $? -eq 0 ]; then
    :
  else
    if [ ! -z $verbose ]; then
      print "ERROR" "input feeder not responding!"
    fi
    clean_up
    spin_up
  fi
  # WARNING: The method below is NOT appropriate
  #          to check status of the input feeder
  # or simply check it from stat.html
  # receive_data=$(curl \
  #   --silent \
  #   http://localhost:8090/stat.html | \
  #   grep RECEIVE_DATA
  # )
  # if [[ "${receive_data}x" == "x" ]]; then
  #   clean_up
  #   spin_up
  # else
  #   :
  # fi
  sleep 60
done
