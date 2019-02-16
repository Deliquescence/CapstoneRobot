
# https://medium.com/hardware-interfacing/how-to-install-pytorch-v4-0-on-raspberry-pi-3b-odroids-and-other-arm-based-devices-91d62f2933c7

# NOTE: You will probably want to
# only use the commands from this instead of running it,
# because of the 8 hour build time.

# NOTE:
# Increase swap to at least 2048 or even 10240
# sudo vim /etc/dphys-swapfile

export NO_CUDA=1
export NO_DISTRIBUTED=1
export NO_MKLDNN=1
export NO_NNPACK=1
export NO_QNNPACK=1

sudo apt install libopenblas-dev libblas-dev m4 cmake cython python3-dev python3-yaml python3-setuptools
sudo pip3.6 install Pillow beautifulsoup4 bottleneck dataclasses;python_version<'3.7' fastprogress>=0.1.18 matplotlib numexpr numpy>=1.12 nvidia-ml-py3 packaging pandas pyyaml requests scipy typing
# Watch for missing fastai deps, may have missed some
# also check https://docs.fast.ai/install.html
sudo pip3.6 install --no-deps fastai

cd ~

# Ideally replace below with archive of successfull build
mkdir build_pytorch && cd build_pytorch
git clone --recursive https://github.com/pytorch/pytorch -b v1.0.1
cd pytorch

python3.6 setup.py build

python3.6 setup.py install --skip-build
