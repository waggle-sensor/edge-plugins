FROM waggle/plugin-torch:1.4.0

RUN pip3 --no-cache-dir install tqdm fcn pyyaml

COPY pytorch_fcn/ /train/

#ENTRYPOINT ["/bin/bash", "run.sh"]
