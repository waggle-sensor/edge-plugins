FROM waggle/plugin-tensorflow:2.0.0-armv7l
COPY . .
WORKDIR /src
RUN pip3 install -r /src/requirements.txt
ARG TOKEN="-10"
ENV WAGGLE_PLUGIN_ID="50" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_REF="https://github.com/iperezx/edge-plugins/tree/master/plugin-smokedetect" \
    TOKEN=${TOKEN}
CMD [ "python3","/src/main.py" ]
