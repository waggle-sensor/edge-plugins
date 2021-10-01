_**WARNING: this repository contains plugins that are no longer managed. Each of the plugins moved to a separated repository for better management. Please search repositories starting with `plugin-` under waggle-sensor to find the plugins being maintained**_

### Edge Plugins

Waggle edge plugins (i.e., user application) are containerized using Waggle Docker images, managed by Waggle edge repository, and deployed to Waggle nodes via Waggle scheduler/dispatcher. Waggle Docker images support not only computation environment for edge plugins, but also provide many commonly used machine learning tools and other libraries to help users package their dependencies. Users may use provided Waggle Docker images as a base to build their own edge plugin. Users are also welcomed to suggest adding packages and libraries that they wish to have in the Waggle Docker images.

#### Hello World Edge Plugin

Run Docker "build" command (or "buildx" if you have set it up) to build helloworld Docker image.

__NOTE__: Assuming you have access to your local docker engine; if not, add the user to docker group

```
# when using docker build command at root of this repository
$ docker build -t tmp/helloworld plugin-helloworld

# when using docker buildx command at root of this repository
$ docker buildx build -t tmp/helloworld --platform linux/amd64,linux/arm64,linux/arm/v7 --load plugin-helloworld

# run the container
$ docker run -ti --rm tmp/helloworld
hello world
bye
```

#### How to Build Your Edge Plugin

Please refer to [building simple edge plugin](plugin-simple/README.md)

#### Which Waggle image I choose for my application

Users are provided a set of Waggle Docker images to build user applications. The Waggle Docker images support a variety of software libraries and machine learning (ML) tools. Many of ML Waggle Docker images come with a specific version of CUDA library installed inside the image. To know further about our Waggle Docker images, please find [Waggle base images](docs/waggle_base_images.md).
