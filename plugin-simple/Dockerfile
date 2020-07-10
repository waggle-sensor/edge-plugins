FROM waggle/plugin-base:0.1.0

COPY /plugin/requirements.txt /plugin/requirements.txt
RUN pip3 install -r /plugin/requirements.txt

COPY /plugin /plugin
WORKDIR /plugin/plugin_bin
CMD ["./plugin_node"]
