#!/bin/zsh

echo "Installing pyenv..."
# pyenv install for CentOS 6.5 x86_64 
yum install -y  gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel

git clone git://github.com/yyuu/pyenv.git ~/.pyenv

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

cat << _PYENVCONF_ >> ~/.zshrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
_PYENVCONF_

echo "Installing python 3.7.2"
pyenv install 3.7.2
yum -y install zlib
yum -y install libffi-devel

echo "Installing pip"
# pip install
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

echo "Installing Dependencies"
pip install xlrd==1.2.0
pip install xlwt==1.3.0
pip install pandas==0.24.1
pip install urllib==1.24.1
pip install firebase_admin==2.16.0
pip install beautifulsoup4==4.7.1

echo "Installation finished"



