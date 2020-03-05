#/bin/bash

wget https://nvidia.box.com/shared/static/ncgzus5o23uck9i5oth2n8n06k340l6k.whl -O torch-1.4.0-cp36-cp36m-linux_aarch64.whl

echo "You must prepare torchvision==0.5.0 for aarch64 since it is not available as of 02/07/2020"
echo "It can be compiled from source by 'python3 setup.py bdist_wheel'"
