FROM waggle/plugin-opencv:4.1.1-gpu

WORKDIR /plugin

# copy heavy weight "static" models as first layer
COPY models/ ./models/

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY plugin_node plugin.instance plugin.ver plugin.credentials ./

ENV WAGGLE_PLUGIN_ID="50" \
  WAGGLE_PLUGIN_NAME="Car / Person Counter"

CMD ["python3", "./plugin_node"]
