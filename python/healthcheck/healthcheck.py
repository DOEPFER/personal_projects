from typing import List

import os

from dotenv import load_dotenv 

from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

import time

from smtplib import SMTP_SSL, SMTPResponseException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cli import args
from log import setup_logging

load_dotenv(override=True)

def healthcheck(url: str) -> str:
    request = Request(url, data=None, headers={'User-Agent': 'healthcheck/1.0 (doepfer)'})
    try:
        response = urlopen(request)
    except HTTPError as error:
        return str(error.code)
    except URLError: 
        return 'The server could not be found.'
    else:
        return str(response.code)

def mailmessage(message: str) -> None | str:
    host = os.getenv('HOST') or ''
    port = int(os.getenv('PORT') or '465')
    user = os.getenv('SEND_MAIL_ACCOUNT') or ''
    password = os.getenv('PASSWORD') or ''

    to = os.getenv('TO_MAIL_ACCOUNT') or ''
    
    mail = MIMEMultipart()
    mail['From'] = user
    mail['To'] = to
    mail['Subject'] = 'healthcheck | ERROR'
    mail.attach(MIMEText(message, 'plain'))
    
    try:
        mailserver = SMTP_SSL(host, port)

        mailserver.ehlo()
        mailserver.login(user, password)
        mailserver.sendmail(mail['From'], mail['To'], mail.as_string())
        mailserver.quit()
        return None
    except SMTPResponseException as error:
        return str(error)
        
def main(urls: List[str]) -> None:
    
    for url in urls:
        status = healthcheck(url)

        if status == '200':
            logger.info(msg=f'{status} | OK | {url}')
        else:
            logger.error(msg=f'{status} | ERROR | {url}')
            if args.sendmail:
                mailmessage(f'{status} | ERROR | {url}')
            
        time.sleep(2)

logger = setup_logging(logprefix=args.logprefix, verbose=args.verbose)

if args.urls:
    main(args.urls)