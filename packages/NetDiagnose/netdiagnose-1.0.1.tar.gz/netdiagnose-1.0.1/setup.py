from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="NetDiagnose",  
    version="1.0.1", 
    author="Erwin Pimenta",  
    author_email="erwinpimenta1644@gmail.com", 
    description="A network diagnostic assistant",  
    long_description=long_description, 
    long_description_content_type="text/markdown",  
    url="https://github.com/gentlsnek/NetDiagnose",  
    packages=find_packages(where="src"), 
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", 
    install_requires=[
        'customtkinter', 
        'scapy', 
        'psutil',
        'speedtest-cli',
        'ping3',
    ],
    entry_points={ 
        "console_scripts": [
            "NetDiagnose = main:main", 
        ],
    },
    include_package_data=True,
)
