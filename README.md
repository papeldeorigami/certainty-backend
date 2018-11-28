# Installation

This installation was tested on a Ubuntu 18.04.1 machine.

## OpenSmile

Install OpenSmile from their website:
[https://www.audeering.com/download/1318/]

Extract the files and execute './buildStandalone.sh'

Notice: in Ubuntu 18.04, it is necessary to add the "-Wno-narrowing" CPP flags to the buildStandalone.sh file (lines 45-46), otherwise it won't compile:

export CXXFLAGS="-O2 -mfpmath=sse -msse2 -Wno-narrowing"
export CFLAGS="-O2 -mfpmath=sse -msse2 -Wno-narrowing"


## Python

We use python version that comes pre-installed with the Ubuntu distribution (python2.7.15rc1). However, a few libs are necessary, and they can be installed with the following command:

sudo apt install python-pip python-pandas python-sklearn
sudo pip install librosa hmmlearn

Notice: if you have an error, that the sklearn.model\_selection library cannot be found, replace it in the classify.sh script with sklearn.cross\_validation (you are probably using an older python version).
