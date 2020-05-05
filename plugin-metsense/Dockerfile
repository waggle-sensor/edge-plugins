FROM python:3-alpine

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY coresense_4 ./
CMD ["python3", "-u", "/app/plugin.py", "--input-sensor"]
