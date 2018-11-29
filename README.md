# Installation

This installation was tested on a Ubuntu 18.04.1 machine.

## Clone this repository

```
git clone https://github.com/papeldeorigami/certainty-backend
cd certainty-backend
```

## OpenSmile

Install OpenSmile from their website:
[https://www.audeering.com/download/1318/]

Extract the files to the local folder:

```
tar -xvzf opensmile-2.3.0.tar.gz
```

Execute './buildStandalone.sh'

Notice: in Ubuntu 18.04, it is necessary to add the "-Wno-narrowing" CPP flags to the buildStandalone.sh file (lines 45-46), otherwise it won't compile:

```
export CXXFLAGS="-O2 -mfpmath=sse -msse2 -Wno-narrowing"
export CFLAGS="-O2 -mfpmath=sse -msse2 -Wno-narrowing"
```

## Python

We use the python3 from the Ubuntu repositories. However, a few libs are necessary, and they can be installed with the following command:

```
sudo apt install python3-pip python3-pandas python3-sklearn
sudo pip3 install hmmlearn
```

Next, setup the path for the OpenSmile installation in the script below, by editing its source code directly:

```
scripts/classify.py
```

## NodeJS

We recommend installing the [nvm](https://github.com/creationix/nvm) to manage dependencies. Use this command, extracted from their  installation instructions:

```
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```

After the installation is complete, you should type this command:

```
nvm install 11
```

This should be enough to get the NodeJS version 11.x installed (we've tested with v11.1.0).

Then, in the project's folder, execute:

```
npm install
```

That is it. Your backend is ready to be used.


## How to execute

```
npm start
```
