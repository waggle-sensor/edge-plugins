FROM waggle/plugin-opencv:4.1.1-cuda 

RUN pip3 --no-cache-dir install torch torchvision tensorboard tqdm

COPY docker_unet/ /train/

#RUN pip3 --no-cache-dir install torchvision

#ENTRYPOINT ["/usr/bin/python3", "/train/main.py"]
