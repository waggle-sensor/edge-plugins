FROM waggle/plugin-base:0.1.0

COPY /plugin /plugin
RUN pip3 install -r /plugin/requirements.txt
WORKDIR /plugin/plugin_bin

ENV WAGGLE_PLUGIN_ID="37" \
    WAGGLE_PLUGIN_NAME="Simple Plugin" \
    WAGGLE_PLUGIN_REF="https://github.com/waggle-sensor/plugin_manager/tree/master/plugins/simple.plugin"

LABEL "waggle.devices"="/dev/waggle_coresense"

CMD ["./plugin_node"]
