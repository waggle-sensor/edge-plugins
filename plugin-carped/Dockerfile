FROM waggle/plugin-opencv:4.1.1-gpu

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# hot fix for pywaggle to use rabbitmq hostname, instead of localhost
RUN pywaggle_loc=$(pip3 show waggle | grep Location | cut -d ':' -f 2 | tr -d ' ') \
  && sed -i 's|amqp://localhost|amqp://rabbitmq|g' ${pywaggle_loc}/waggle/pipeline.py \
  && sed -i 's|localhost|rabbitmq|g' ${pywaggle_loc}/waggle/plugin/__init__.py

COPY plugin_node ./plugin_bin/
COPY models/ ./plugin_bin/models/
COPY plugin.instance plugin.ver plugin.credentials ./

CMD ["python3", "-u", "/app/plugin_bin/plugin_node"]
