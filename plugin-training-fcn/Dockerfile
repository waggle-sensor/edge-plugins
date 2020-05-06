FROM waggle/plugin-torch:1.4.0

RUN pip3 --no-cache-dir install tqdm fcn

COPY pytorch_fcn/ /train/

ENTRYPOINT ["/usr/bin/python3", "/train/main.py"]
