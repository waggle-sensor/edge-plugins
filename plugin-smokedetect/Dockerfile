FROM waggle/plugin-tensorflow:2.0.0-armv7l
COPY . .
WORKDIR /src
RUN pip3 install -r /src/requirements.txt
ENV WAGGLE_PLUGIN_ID="37" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_REF=""
ENTRYPOINT [ "python3" ]
CMD [ "/src/main.py" ]
