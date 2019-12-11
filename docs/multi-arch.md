### Multi Architecture Build

As Waggle accommodates many computation enhanced devices as edge device on Waggle nodes, Waggle Docker images and edge plugins should support different hardware architecture to be running without problems. Waggle currently (as of 2019) supports armv7 architecture and tries to accommodate both arm64 and amd64 (i.e., x86_64) architectures. Development version of Waggle Docker images support all of them. This means you can run edge plugins, without modifications, on your laptop, cloud clusters, edge devices in development kit, and actuall Waggle nodes. This document describes how to enable multi-architecture build using Docker.

__NOTE__: Any suggestion on this process is welcomed!

#### Docker buildx (recommended)

From Docker 19.03 CE buildx is built along with Docker. To use it, [experimental flag](https://docs.docker.com/engine/reference/commandline/cli/#experimental-features) should be set. For details, visit [buildx github](https://github.com/docker/buildx).

Docker buildx developers suggest mainly [3 strategies](https://github.com/docker/buildx#building-multi-platform-images) to build multi-arch Docker images.

1) Use QEMU: host machine builds multi-arch Docker images using QEMU. The QEMU binaries may need to be installed in kernel inside Docker image.
2) Use multiple native nodes: set up multiple nodes to accept connection from host machine and the host machine uses the nodes to build Docker image.
3) Use architecture independent programming language (e.g., Go language)

This document follows 2) as it gives simpler and better. Here is a simple set up for the machines.

```
                             [ router ]
                                 |
       --------------------------------------------------------- 
       |               |                   |                   |
   [ host ]    [ amd64 machine ]   [ arm64 machine ]   [ armv7 machine ]
```

On each machine except the host their Docker daemon needs to accept connection from the host. To configure,

```
# add hosts element in /etc/docker/daemon.json
...
"hosts": [
        "unix:///var/run/docker.sock",
        "tcp://0.0.0.0:2376"
    ]
...
$ systemctl restart docker.service
```

__NOTE__: You may see an error below. Then remove -H flag of ExecStart in /lib/systemd/system/docker.service and retry.
```
unable to configure the Docker daemon with file /etc/docker/daemon.json: the following directives are specified both as a flag and in the configuration file : hosts: (from flag: [fd://], from file: [unix:///var/run/docker.sock tcp://0.0.0.0:2376])
```
On the host machine set a builder with nodes,
```
$ docker context create node-armv7 --docker "host=tcp://${armv7_host}:2376"
$ docker context create node-arm64 --docker "host=tcp://${arm64_host}:2376"
$ docker context create node-amd64 --docker "host=tcp://${amd64_host}:2376"
$ docker buildx create --name mybuilder --driver docker-container node-armv7 node-arm64 node-amd64
$ docker buildx inspect mybuilder --bootstrap
$ docker buildx use mybuilder
```

This setup now lets you build multi-arch Docker image,
```
# push the images to hub registry
$ docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t ${TAG} --push ${dockerfile_path}
# push the images to host machine 
$ docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t ${TAG} --load ${dockerfile_path}
```

Now, you can run the Docker image on any of the 3 architecture platforms with the same Docker run command
```
$ docker run -ti --rm ${TAG}
```

#### Docker build and manifest (if necessary)

Docker buildx requires a single Dockerfile to populate it on multi architecture platforms. Dockerfile however may be different between target platforms. For example, [plugin-opencv](../plugin-opencv) needs multiple Dockerfiles that are differently configured. plugin-opencv on armv7 with Mali GPU needs Mali GPU driver and OpenCV compilation may need NEON flag set. On the other hand, it needs CUDA package as well as CUDA flag set when building on Tegra Jetson arm64 platforms or amd64 platform with Nvidia graphics cards installed. However, Docker image of plugin-opencv still needs its tag name unified such that other plugins that are based on this can always refer to the same tag name no matter what architecture they are in.

In such case, multiple Dockerfile can be built on their target platform with different tag name and their tag can be merged using [Docker manifest](https://docs.docker.com/engine/reference/commandline/manifest/).
```
# running the following on each target machine
$ docker build -t ${TAG}-armv7 -f Dockerfile.armv7 ${dockerfile_path}
$ docker push ${TAG}-armv7
$ docker build -t ${TAG}-arm64 -f Dockerfile.arm64 ${dockerfile_path}
$ docker push ${TAG}-arm64
$ docker build -t ${TAG}-amd64 -f Dockerfile.amd64 ${dockerfile_path}
$ docker push ${TAG}-amd64
```

And then on any machine run,
```
$ docker manifest create ${TAG} ${TAG}-armv7 ${TAG}-arm64 ${TAG}-amd64
$ docker manifest inspect ${TAG}
$ docker manifest push --purge ${TAG}  # --purge removes the manifest from local machine
```
