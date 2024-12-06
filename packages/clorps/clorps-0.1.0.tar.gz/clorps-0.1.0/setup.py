from setuptools import setup, find_packages

setup(
    name="clorps",
    version="0.1.0",
    description="CLORPS: A module for CLIP, LPIPS, and ORB based image similarity.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vaibhav Gupta",
    author_email="vaibhavgupta.ggwp@gmail.com",
    url="https://github.com/vaidatascientist",
    packages=find_packages(),
    install_requires=[
        "torch",
        "open_clip_torch",
        "lpips",
        "numpy",
        "scikit-learn",
        "Pillow",
        "opencv-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
