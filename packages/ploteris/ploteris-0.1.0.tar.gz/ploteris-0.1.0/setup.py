from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name="ploteris",
    version="0.1.0",
    author="lmacionis",
    email="lmacionis@yahoo.com",
    packages=find_packages(),
    install_requires=[
                      "numpy",
                      "contourpy==1.3.0",
                      "cycler==0.12.1",
                      "fonttools==4.54.1",
                      "kiwisolver==1.4.7",
                      "matplotlib==3.9.2",
                      "packaging==24.1",
                      "pillow==11.0.0",
                      "pyparsing==3.2.0",
                      "python-dateutil==2.9.0.post0",
                      "six==1.16.0"
                      ],
    python_requires=">=3.6"
)

# python ./setup.py sdist bdist_wheel
# twine upload dist/*

