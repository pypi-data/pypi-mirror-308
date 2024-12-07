from setuptools import setup, find_packages

setup(
    name="RpiL",
    version="0.2.3",
    packages=find_packages(where="src"),  # This finds all packages directly inside 'src'
    package_dir={"": "src"},  # Maps the root package to 'src'
    install_requires=[
        "pigpio",
        "gpiozero"
    ],
    extras_require={
        "rpi": ["RPi.GPIO", "Adafruit_DHT"]  # Raspberry Pi-specific dependencies
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

        For detailed documentation, visit:
        `Documentation <https://rpil.readthedocs.io>`_

        The source code is available on GitHub:
        `GitHub Repository <https://github.com/TrynaThinkOf1/RpiL>`_
        """,
    long_description_content_type="text/x-rst",
    url="https://rpil.readthedocs.io",
)
