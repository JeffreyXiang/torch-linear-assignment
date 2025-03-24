from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension, IS_HIP_EXTENSION
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

BUILD_TARGET = os.environ.get("BUILD_TARGET", "auto")

if BUILD_TARGET == "auto":
    if IS_HIP_EXTENSION:
        IS_HIP = True
    else:
        IS_HIP = False
else:
    if BUILD_TARGET == "cuda":
        IS_HIP = False
    elif BUILD_TARGET == "rocm":
        IS_HIP = True

if not IS_HIP:
    cc_flag = []
else:
    archs = os.getenv("GPU_ARCHS", "native").split(";")
    cc_flag = [f"--offload-arch={arch}" for arch in archs]
    
with open("requirements.txt", "r") as fp:
    required_packages = [line.strip() for line in fp.readlines()]

setup(
    name="torch-linear-assignment",
    version="0.0.3",
    author="Ivan Karpukhin",
    author_email="karpuhini@yandex.ru",
    description="Batched linear assignment with PyTorch and CUDA.",
    packages=["torch_linear_assignment"],
    ext_modules=[
        CUDAExtension(
            name="torch_linear_assignment._backend",
            sources=[
                "src/torch_linear_assignment_cuda.cpp",
                "src/torch_linear_assignment_cuda_kernel.cu"
            ],
            extra_compile_args={
                "cxx": ["-O3", "-std=c++17"],
                "nvcc": ["-O3","-std=c++17"] + cc_flag,
            }
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    },
    install_requires=required_packages,
)
