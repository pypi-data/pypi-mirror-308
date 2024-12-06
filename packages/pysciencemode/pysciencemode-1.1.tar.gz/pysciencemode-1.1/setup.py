from setuptools import setup

setup(
    name="pyScienceMode",
    version="1.1",
    packages=[
        ".",
        "sciencemode_cffi-1.0.0-cp310-cp310-win_amd64.whl",
        # "crccheck",
        # "colorama",
        # "pyserial",
        # "typing",
        "pyScienceMode"],
    url="https://github.com/s2mLab/pyScienceMode.git",
    license="",
    author="S2M Lab",
    author_email="kevin.co@umontreal.ca",
    description="Python interface to control the Rehastim2 and RehastimP24 devices.",
    python_requires=">=3.8",
    zip_safe=False,
)
