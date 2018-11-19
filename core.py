# !/usr/bin/env python
# coding=utf-8

import datetime
import os
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import requests
from lxml import etree
import os
import time
import re
from multiprocessing.dummy import Pool


MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_SENDER = os.environ.get("MAIL_SENDER")
MAIL_RECEIVER = os.environ.get("MAIL_RECEIVER")
PORT_DATE = os.environ.get("PORT_DATE")

MAIL_ENCODING = "utf8"

# @retry(stop=stop_after_attempt(3))
def get_email_content():


    ######################################## main ########################################
    url0 = 'https://doub.io/sszhfx'
    xp1 = '/html/body/section/div[3]/div/div[1]/div[1]/div[3]/span/strong'  
    xp2 = '/html/body/section/div[3]/div/div[1]/table[1]/tbody/tr[5]/td[3]' 
    xp3= '/html/body/section/div[3]/div/div[1]/table[1]/tbody/tr[5]/td[2]' 

    htm0 = getHtml(url0)
    cons1 = getContent(htm0, xp1)  
    cons2 = getContent(htm0, xp2)   
    cons3 = getContent(htm0, xp3)   
    old_date=PORT_DATE
    if cons1 is old_date:
        return FALSE
    else:
        os.environ.set["PORT_DATE"]=cons1    
        html = """      
         <html>
            <head> {0} </hdead>
            <body>
            <table cellspacing="0" border="1">
                <tr>
                    <td background: #F5FAFA; color: #797268;>{1}</td>
                    <td background: #F5FAFA; color: #797268;>{2}</td>
                </tr>
            </table>
            </body>
        </html>"""
        return html.format(cons1,cons3,cons2)


def send_email():

    content = get_email_content()
    message = MIMEText(content, "html", MAIL_ENCODING)
    message["From"] = MAIL_SENDER #Header("paper", MAIL_ENCODING)
    message["To"] = MAIL_RECEIVER #Header("Reader")
    message["Subject"] = Header("SS_Port", MAIL_ENCODING)
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(MAIL_SENDER, MAIL_RECEIVER, message.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


def getHtml(url):
    html = requests.get(url).content
    selector = etree.HTML(html)
    return selector


def getContent(htm, xpathStr):
    selector = htm
    content = selector.xpath(xpathStr)  # copy from chrome # print content
    return content


if __name__ == "__main__":
    send_email()
