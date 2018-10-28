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
from tenacity import retry, stop_after_attempt


MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_SENDER = os.environ.get("MAIL_SENDER")
MAIL_RECEIVER = os.environ.get("MAIL_RECEIVER")

MAIL_ENCODING = "utf8"

@retry(stop=stop_after_attempt(3))
def get_email_content():


    ######################################## main ########################################
    url0 = 'http://arxiv.org/list/cs.CV/recent'
    # print url0
    # xpath of each page
    xp1 = '//dl[1]//*[@class="list-identifier"]//a[2]//@href'  # pdf href list
    xp2 = '//dl[1]//*[@class="list-title mathjax"]/text()'  # Title: Object Boundary Guided Semantic Segmentation
    xp_date = '//*[@id="dlpage"]/h3[1]/text()'  # date->folder

    htm0 = getHtml(url0)
    cons1 = getContent(htm0, xp1)  # get pdfs' href
    cons2 = getContent(htm0, xp2)  # get papers' title
    cons_date = getContent(htm0, xp_date)  # get date

    folder = cons_date[0].split(', ')  # get date string

    papertile=''
    paperlink=''
    # judge the path exists or not
    for indx in range(0, len(cons1)):
        href = 'http://arxiv.org' + cons1[indx]
        title = cons2[2 * indx + 1]
        paper=paper+'<tr><td>{0}</td><td><a href="{1}">{2}</td></tr>'.fromat(indx+1,href, title)

    html = """
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <div>
                <table border="1">
                {0}
                </table>
            <div>
        </body>
        </html>
    """
    return html.format(paper)


def send_email():

    content = get_email_content()
    message = MIMEText(content, "html", MAIL_ENCODING)
    message["From"] = MAIL_SENDER #Header("paper", MAIL_ENCODING)
    message["To"] = MAIL_RECEIVER #Header("Reader")
    message["Subject"] = Header("SubscribePaper", MAIL_ENCODING)
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
