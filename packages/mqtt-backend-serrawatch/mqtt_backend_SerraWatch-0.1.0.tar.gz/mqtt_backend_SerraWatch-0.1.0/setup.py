from setuptools import setup, find_packages

setup(
    name="mqtt_backend_SerraWatch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
        "PyYAML",
    ],
    author="Alexandre GRZEGORCZYK",
    author_email="alexandregrzegorczyk2@gmail.com",
    description="This project was created as part of the Internet of Things (IoT) course in the Master's program in Computer Architecture at the Haute École de la Province de Liège (HEPL).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IOTSerraWatch/Client_OnUbuntu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
