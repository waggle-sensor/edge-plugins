### Video/Audio Streamer Plugin

_NOTE: audio streaming is not supported yet_

The plugin utilizes ffserver and ffmpeg to stream live feed from video/audio devices over http.

_NOTE: ffmpeg does not support ffserver since 2018._

#### Usage

To run,

```
# streaming fed from a down-facing camera
device=/dev/waggle_cam_bottom
version=0.1.0
name=cam_bottom_live
$ docker run -d --rm \
  --device ${device} \
  --name ${name} \
  waggle/plugin-media-streaming:${version} \
  -f v4l2 \
  -input_format mjpeg \
  -video_size 640*480 \
  -i ${device} \
  -c:v libx264
```

To get live feed,

```
$ ffplay http://${name}:8090/live
# or
$ ffmpeg -i http://${name}:8090/live live.mp4
# or
$ python3
>> import cv2
>> cap = cv2.VideoCapture('http://${name}:8090/live')
>> ret, image = cap.read()
```
