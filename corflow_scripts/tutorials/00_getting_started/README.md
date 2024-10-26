# Getting Started

## Prerequisites

### Install Python

To use Corflow and the additional .py scripts and functions in this repository, you have to install _Python_ on your system. How to install Python depends on your OS (operating system). If you use Linux, run

```shell
python3 --version
```

in your (shell) terminal, to check, whether Python is installed or not. If it isn't, enter the following commands in your terminal to install Python on your Linux system (Debian, Ubuntu, Mint).

```shell
sudo apt update
```

```shell
sudo apt upgrade
```

```shell
sudo apt install python3
```

If you use Windows, macOS, another Linux distribution or if you have problems installing Python, check out [How to Install Python on Your System: A Guide](https://realpython.com/installing-python/) or another Guide you find on the internet.

You may want to use an IDE (integrated development environment) like [Visual Studio Code](https://code.visualstudio.com/) when working on your scripts.

### Install pip

Depending on the method you used to install Python, you may or may not have to install Python's package manager _pip_. On Linux, check, whether pip is installed or not:

```shell
pip --version
```

If it isn't, run the following command to install it on your Linux system (Debian, Ubuntu, Mint):

```shell
sudo apt install python3-pip
```

If you use another OS or if you encounter problems installing pip, check out the [official documentation](https://pip.pypa.io/en/stable/installation/). The above steps are based on [this Guide](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers).

### Install venv

Install the _venv_ module to create virtual environments:

```shell
sudo apt install python3-venv
```
Create a new virtual environment in your current directory named _my\_venv_ (you can choose another name or path):

```shell
python3 -m venv my-venv
```

Activate your new virtual environment:

```shell
source my-venv/bin/activate
```

Run the following command to make sure, that you use the correct interpreter and successfully activated your new virtual environment:

```shell
pip list
```

This should display something similar to:

```console
Package Version
------- -------
pip     24.0
```

If you encounter problems creating a virtual environment, check out the [official documentation](https://docs.python.org/3/library/venv.html) for the venv module.

## Install Corflow

Open your terminal, navigate to your virtual environment and activate it, and enter the following command:

```shell
pip install corflow
```