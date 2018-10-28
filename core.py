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
# from tenacity import retry, stop_after_attempt


MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_SENDER = os.environ.get("MAIL_SENDER")
MAIL_RECEIVER = os.environ.get("MAIL_RECEIVER")

MAIL_ENCODING = "utf8"

# @retry(stop=stop_after_attempt(3))
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
    paper=''
    # judge the path exists or not
    for indx in range(0, len(cons1)):
        href = 'http://arxiv.org' + cons1[indx]
        title = cons2[2 * indx + 1]
        if (indx % 2) == 0:
            paper=paper+'<tr><td>{0}</td><td><a href="{1}">{2}</td></tr>'.format(indx+1,href, title)
        else:
            paper=paper+'<tr><td class="alt">{0}</td><td class="alt"><a href="{1}">{2}</td></tr>'.format(indx+1,href, title)

    html = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN""http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        {0}
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>CSS Tables</title>
        <link href="styles.css" rel="stylesheet" type="text/css" />
        </head>
        <style type="text/css">

        body {
        font: normal 11px auto "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
         color: #4f6b72;
         background: #E6EAE9;
        }

        a {
         color: #c75f3e;
        }
        caption {
         padding: 0 0 5px 0;
         width: 700px;  
         font: italic 11px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
         text-align: right;
        }
        th {
         font: bold 11px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
         color: #4f6b72;
         border-right: 1px solid #C1DAD7;
         border-bottom: 1px solid #C1DAD7;
         border-top: 1px solid #C1DAD7;
         letter-spacing: 2px;
         text-transform: uppercase;
         text-align: left;
         padding: 6px 6px 6px 12px;
         background: #CAE8EA url(images/bg_header.jpg) no-repeat;
        }
        th.nobg {
         border-top: 0;
         border-left: 0;
         border-right: 1px solid #C1DAD7;
         background: none;
        }
        td {
         border-right: 1px solid #C1DAD7;
         border-bottom: 1px solid #C1DAD7;
         background: #fff;
         font-size:11px;
         padding: 6px 6px 6px 12px;
         color: #4f6b72;
        }
        td.alt {
         background: #F5FAFA;
         color: #797268;
        }
        th.spec {
         border-left: 1px solid #C1DAD7;
         border-top: 0;
         background: #fff url(images/bullet1.gif) no-repeat;
         font: bold 10px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
        }
        th.specalt {
         border-left: 1px solid #C1DAD7;
         border-top: 0;
         background: #f5fafa url(images/bullet2.gif) no-repeat;
         font: bold 10px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
         color: #797268;
        }
        </style>
        <body>
        <table cellspacing="0" >
                {1}
                </table>
        </body>
        </html>
    """
    return html.format(folder[1],paper)


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
