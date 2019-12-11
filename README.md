### Edge Plugins

Waggle edge plugins (i.e., user application) are containerized using Waggle Docker images, managed by Waggle edge repository, and deployed to Waggle nodes via Waggle scheduler/dispatcher. Waggle Docker images support not only computation environment for edge plugins, but also provide many commonly used machine learning tools and other libraries to help users package their dependencies. Users may use provided Waggle Docker images as a base to build their own edge plugin. Users are also welcomed to suggest adding packages and libraries that they wish to have to the Waggle Docker images.

#### Hello World Edge Plugin

```
$ cat <<EOF > plugin.sh
echo "hello world"
echo "bye"
EOF
$ cat <<EOF > Dockerfile
FROM waggle/plugin-base-light:0.1.0
COPY plugin.sh /app/
WORKDIR /app
CMD ["/bin/sh", "plugin.sh"]
EOF
```

Then run Docker "build" command to build (or "buildx" if you have),

__NOTE__: Assuming you have access to your local docker engine; if not, add the user to docker group

```
# when using docker build command
$ docker build -t tmp/helloworld .

# when using docker buildx command
$ docker buildx build -t tmp/helloworld --platform linux/amd64,linux/arm/v7 --load .

# running the container
$ docker run -ti --rm tmp/helloworld
hello world
bye
```

#### How to Build Your Edge Plugin

Please refer to [building simple edge plugin](plugin-simple/README.md)
