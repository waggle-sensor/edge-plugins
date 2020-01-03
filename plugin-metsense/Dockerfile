FROM waggle/plugin-base:0.1.0

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# hot fix for pywaggle to use rabbitmq hostname, instead of localhost
RUN pywaggle_loc=$(pip3 show waggle | grep Location | cut -d ':' -f 2 | tr -d ' ') \
  && sed -i 's|amqp://localhost|amqp://rabbitmq|g' ${pywaggle_loc}/waggle/pipeline.py

WORKDIR /app
COPY coresense_4 ./
CMD ["python3", "-u", "/app/plugin.py", "--input-sensor"]
