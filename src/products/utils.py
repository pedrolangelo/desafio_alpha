from .models import Info
import smtplib
import email.message
from pandas_datareader import data as web
import pandas as pd


def mandarEmail(acao, ativo, para):
        corpo_email = """
        <p>%s  %s</p>
        """%(acao, ativo)

        msg = email.message.Message()
        msg['Subject'] = "Teste Celery"
        msg['From'] = 'gfkjyf@gmail.com'
        msg['To'] = para
        password = 'onwdolbcsxpawooe' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado para venda da', ativo)