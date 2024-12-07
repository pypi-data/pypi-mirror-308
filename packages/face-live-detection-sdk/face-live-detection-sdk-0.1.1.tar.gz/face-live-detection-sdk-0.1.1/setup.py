# setup.py

from setuptools import setup, find_packages

setup(
    name="face-live-detection-sdk",  # Name of your SDK
    version="0.1.1",  # Version number
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # List of dependencies for your SDK
        "tensorflow",
        "opencv-python-headless",
        "flask",
        "flask-cors",
        "imutils",
        "numpy",
    ],
    author="rapiddata",
    author_email="datascience.rapiddata@gmail.com",
    description="A Python SDK for liveness detection using a pre-trained model.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gayathri-kannanv/liveness-detection-sdk",  # URL to your SDK's repo (if applicable)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
