import platform
import torch 

def gpu_detection():
    system = platform.system()
    if system == "Darwin":
        return "metal"
    elif system == "Windows" or system == "Linux":
        if torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    else:
        return "cpu"