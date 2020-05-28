### Applications Logging in Docker

Applications running inside a Docker container print logs to `stdout` and `stderr`. By default, Docker captures those logs from the host, i.e., outside of a container, and puts them in `/var/lib/docker/containers/${CONTAINER_ID}/${CONTAINER_ID}-json.log` (See [more](https://docs.docker.com/config/containers/logging/json-file/)). Note that the path requires root access. However, the log files including their path are removed when the corresponding Docker container exits and is removed (with `--rm` option). 

#### Logging Drivers

Docker supports many logging drivers such as syslog, journald, fluentd, gcplogs, etc. However Docker community engine supports only `local`, `json-file`, and `journald` (See [more](https://docs.docker.com/config/containers/logging/configure/#limitations-of-logging-drivers)).

#### Log Rotation

Logs can be rotated by the options below.

```
# using Docker run
$ docker run -ti --log-opt max-size=10m --log-opt max-file=3 waggle/plugin-base:0.1.0
# or specified in /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3" 
  }
}
```
