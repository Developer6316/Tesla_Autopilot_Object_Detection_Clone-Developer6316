from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tesla-autopilot-clone",
    version="1.0.0",
    author="Developer6316",
    description="Tesla Autopilot Clone – Object & Lane Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tesla-autopilot-clone",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "customtkinter>=5.2.0",
        "opencv-python>=4.5.0",
        "Pillow>=9.0.0",
        "ultralytics>=8.0.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "tesla-autopilot=autopil2:main",
        ],
    },
)