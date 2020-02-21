# Simple Plugin

## Description

This plugin contains source of the code as well as Dockerfile to build it on Waggle Docker image. It provides a template to publish some measurements and print incoming messages every few seconds.

## Details

The Dockerfile installs necessary libraries in [requirements.txt](plugin/requirements.txt) and build a container that runs [plugin_node](plugin/plugin_bin/plugin_node).

In the Dockerfile, users can specify metadata of the code such as version, name, description, reference url, and etc. They also can put metadata about hardware requirement of the plugin. In the simple plugin case, it requires waggle device, linked to "/dev/waggle_coresense". This metadata can be used to guide on what type of Waggle nodes plugins get deployed.
