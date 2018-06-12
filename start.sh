#!/bin/bash
source ~/.bash_profile
cd /data/py/bsj
workon bishijie
echo `date +%F-%T` >bsj.log 
echo "----------------------------------------------------------------------------------"
nohup scrapy crawl bsj >>bsj.log 2>&1 &
#deactivate
