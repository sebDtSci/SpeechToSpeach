import platform
import torch 

# BUG: not working on macos for now
# def gpu_detection():
#     system = platform.system()
#     if system == "Darwin":
#         return "metal"
#     elif system == "Windows" or system == "Linux":
#         if torch.cuda.is_available():
#             return "cuda"
#         else:
#             return "cpu"
#     else:
#         return "cpu"
    
def gpu_detection():
    system = platform.system()
    if system == "Windows" or system == "Linux":
        if torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    else:
        return "cpu"