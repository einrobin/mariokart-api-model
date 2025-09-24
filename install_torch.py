import subprocess
import sys
import importlib


def ensure_torch_module(module: str, version: str):
    try:
        torch = importlib.import_module(module)
        return torch
    except ImportError:
        print(f"Torch module '{module}' not found, installing it now... this will take a while!")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            f"{module}=={version}", "--index-url", "https://download.pytorch.org/whl/cu121"
        ])


def install_torch():
    """
    Torch is huge (~ 2,5 GB), so we download it on the fly instead of packing it into the binary
    """
    torch = ensure_torch_module("torch", "2.5.1+cu121")
    print(f"Torch version: {torch.__version__}")


def install_torchvision():
    torchvision = ensure_torch_module("torchvision", "0.20.1+cu121")
    print(f"Torchvision version: {torchvision.__version__}")
