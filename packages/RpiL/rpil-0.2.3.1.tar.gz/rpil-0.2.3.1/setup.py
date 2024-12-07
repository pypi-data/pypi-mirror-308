from setuptools import setup, find_packages

setup(
    name="RpiL",
    version="0.2.3.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pigpio",
        "gpiozero"
    ],
    extras_require={
        "rpi": [
            "RPi.GPIO",
            "Adafruit_DHT"
        ]
    },
    description="Library for controlling Raspberry Pi hardware.",
    author="Zevi Berlin",
    author_email="zeviberlin@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    long_description="""
    RpiL is a Python library for controlling Raspberry Pi hardware.
    """,
    long_description_content_type="text/x-rst",
    url="https://rpil.readthedocs.io",
)
