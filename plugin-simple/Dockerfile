FROM waggle/plugin-base:0.1.0

COPY /plugin /plugin
RUN pip3 install -r /plugin/requirements.txt
WORKDIR /plugin/plugin_bin

CMD ["./plugin_node"]
