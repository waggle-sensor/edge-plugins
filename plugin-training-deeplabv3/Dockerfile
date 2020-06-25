FROM waggle/plugin-opencv:4.1.1-cuda 

RUN pip3 --no-cache-dir install torch torchvision tensorboard tqdm wandb

COPY pytorch_deeplabv3/ /train/

ENTRYPOINT ["/usr/bin/python3", "/train/main.py"]
