FROM waggle/plugin-base:0.1.0

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY coresense_4 ./

ENTRYPOINT ["python3", "/app/plugin.py"]
CMD ["--input-sensor"]
