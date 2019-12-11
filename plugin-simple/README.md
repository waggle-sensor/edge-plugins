### Simple Plugin

This simple plugin contains source of the code as well as Docker recipe to build it on Waggle Docker image. All the simple plugin does is that it publishes a value to Waggle data pipeline every 5 seconds. The docker recipe (i.e., Dockerfile) first installs necessary libraries in [requirements.txt](plugin/requirements.txt) and build a container that runs [plugin_node](plugin/plugin_bin/plugin_node).

In the Docker recipe, users can specify metadata of the code such as version, name, description, reference url, and etc. They also can put metadat about hardware requirement of the plugin. In the simple plugin case, it requires waggle device, linked to "/dev/waggle_coresense". This metadata can be used to guide on what type of Waggle nodes plugins get deployed.