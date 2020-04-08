FROM waggle/plugin-torch:1.4.0

RUN pip3 --no-cache-dir install tqdm pyyaml fcn (maybe not fcn, need to check 4/8/2020)

COPY pytorch_fcn/ /train/

#ENTRYPOINT ["/bin/bash", "run.sh"]
