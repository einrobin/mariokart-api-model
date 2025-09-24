import subprocess
import sys


def install_torch():
    """
    Torch is huge (~ 2,5 GB), so we download it on the fly instead of packing it into the binary
    """
    try:
        import torch
    except ImportError:
        print("PyTorch not found, installing it now... this will take a while!")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.5.1+cu121",
                               "--index-url", "https://download.pytorch.org/whl/cu121"])
        import torch

    print(f"Torch version: {torch.__version__}")


def install_torchvision():
    try:
        import torchvision
    except ImportError:
        print("PyTorchvision not found, installing it now... this will take a while!")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torchvision==0.20.1+cu121",
                               "--index-url", "https://download.pytorch.org/whl/cu121"])
        import torchvision

    print(f"Torchvision version: {torchvision.__version__}")
