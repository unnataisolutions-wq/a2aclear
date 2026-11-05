from setuptools import setup, find_packages
import os

setup(
    name="a2aclear",
    version="1.0.0",
    author="Rohit",
    author_email="contact@unnataisolutions.com",
    description="A2AClear: Sovereign Financial Clearinghouse & Atomic Settlement Protocol for Autonomous AI Agents",
    long_description=open("README.md").read() if os.path.exists("README.md") else "A2AClear Sovereign Protocol",
    long_description_content_type="text/markdown",
    url="https://unnataisolutions.com/a2aclear",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    python_requires=">=3.9",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "a2a=a2aclear.cli:main",
        ],
    },
)
