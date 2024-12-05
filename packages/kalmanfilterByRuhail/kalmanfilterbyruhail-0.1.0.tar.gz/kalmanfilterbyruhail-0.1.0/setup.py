from setuptools import setup, find_packages

setup(
    name="kalmanfilterByRuhail",
    version="0.1.0",
    description="A Python library for implementing Kalman and Extended Kalman Filters",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruhail-ali-khan/kalmanfilterByRuhail",  
    author="Ruhail Ali Khan",
    author_email="ruhailalik@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
