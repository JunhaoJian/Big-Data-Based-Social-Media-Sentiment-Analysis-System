import torch

print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA是否可用: {torch.cuda.is_available()}")

# 只在CUDA可用时打印GPU名称
if torch.cuda.is_available():
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
else:
    print("使用CPU运行（不影响代码功能，仅训练速度稍慢）")