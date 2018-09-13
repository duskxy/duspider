#!/bin/bash
source ~/.bash_profile
ppath=/data/py/bsj/utils
cd $ppath
workon bishijie
echo `date +%F" "%T`
proxychains4 -q python premproxy3.py
