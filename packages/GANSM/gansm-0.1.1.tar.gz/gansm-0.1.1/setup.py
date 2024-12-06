from setuptools import setup, find_packages

setup(
    name = "GANSM",
    version = '0.1.1',
    packages = find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "torchvision>=0.10.0",
        "tensorboard>=2.5.0",
    ],
)