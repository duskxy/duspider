#!/root/.virtualenv/bishijie/bin/python
from config import myconn,Redis,bmail
import datetime
import smtplib
from email.mime.text import MIMEText

class Bsjmail:
    def __init__(self):
        self.smtpobj = smtplib.SMTP_SSL(bmail['mail_host'],465)
        self.smtpobj.login(bmail['mail_user'],bmail['mail_pass'])
    def Sendemail(self,title,content):
        message = MIMEText(content,'plain','utf-8')
        message['From'] = bmail['sender']
        message['To'] = bmail['receiver']
        message['Subject'] = title
        self.smtpobj.sendmail(bmail['sender'],bmail['receiver'],message.as_string())

now = datetime.datetime.now().strftime('%Y-%m-%d')
alert = ["黑客攻击"]

Bemail = Bsjmail()

cursor = myconn.cursor()
cursor.execute("select title,create_time,content from bsj")
result = cursor.fetchall()
for i,j,v in result:
    for a in alert:
        if a in i:
            if Redis.exists('altit:{}'.format(i)):
                print("已告警")
            else:
                print(i,j,v)
                Bemail.Sendemail(i,"{}{}".format(j,v))
                Redis.set('altit:{}'.format(i),1)
        else:
            pass
