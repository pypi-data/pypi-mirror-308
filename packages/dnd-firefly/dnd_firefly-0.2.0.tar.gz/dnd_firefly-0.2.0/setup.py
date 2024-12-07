from setuptools import setup, find_packages

setup(
    name="dnd-firefly",
    version="0.2.0",
    packages=find_packages(),
    # install_requires=[
    #     "selenium",
    # ],
    author="Emmanuel Joliet",
    author_email="ejoliet@caltech.edu",
    description="Programatically drag-and-drop in IRSA Viewer tool via Upload feature",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ejoliet/firefly-vscode-extension.git",
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Minimum Python version
    entry_points={
        "console_scripts": [
            "dnd_firefly=firefly_demo.dnd_firefly:main",
        ],
    },
)
