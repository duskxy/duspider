#!/root/.virtualenv/bishijie/bin/python
from config import myconn,Redis,bmail
import datetime
import smtplib
from email.mime.text import MIMEText
import sys
import logging
import os

now = datetime.datetime.now().strftime('%Y-%m-%d')
alert = ["黑客攻击","黑客窃取","被盗","上线"]
Blog = os.path.dirname((os.path.abspath(__file__)))
logpath = Blog+"/log/bsjalert.log"
print(logpath)    

logging.basicConfig(filename=logpath,filemode="w",level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
               )


class Bsjmail:
    def __init__(self):
        try:
            self.smtpobj = smtplib.SMTP_SSL(bmail['mail_host'],465)
            self.smtpobj.login(bmail['mail_user'],bmail['mail_pass'])
        except smtplib.SMTPException as e:
            logging.error("邮箱登录异常{}".format(e))
    def Sendemail(self,title,content):
        message = MIMEText(content,'plain','utf-8')
        message['From'] = bmail['sender']
        message['To'] = bmail['receiver']
        message['Subject'] = title
        self.smtpobj.sendmail(bmail['sender'],bmail['receiver'],message.as_string())


Bemail = Bsjmail()

cursor = myconn.cursor()
cursor.execute("select title,create_time,content from bsj where substr(crawl_tiem,1,10) = '%s'" % (now))
result = cursor.fetchall()
for i,j,v in result:
    for a in alert:
        if a in i:
            if Redis.exists('altit:{}'.format(i)):
                print("已告警")
                logging.info("{}已告警".format(i))
            else:
                print(i,j,v)
                Bemail.Sendemail(i,"{}{}".format(j,v))
                Redis.set('altit:{}'.format(i),1)
        else:
            pass
