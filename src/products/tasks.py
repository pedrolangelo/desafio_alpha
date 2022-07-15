from celery import shared_task
from .models import Info
from celery.decorators import periodic_task
from celery.task.schedules import crontab
import smtplib
import email.message
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime

@shared_task
def teste(name):
    print("teste")

@periodic_task(run_every=(crontab(minute='*/1')))
def enviar_email():
    for i in Info.objects.all():
        x = web.DataReader(i.ativo, data_source='yahoo', start=datetime.date(i.date), end=datetime.now())
        x = pd.DataFrame(x)

        print("Valor da ação", x['Close'])
        print("valor pra venda", i.superior)
        print("valor pra compra", i.inferior)

        if(x['Close'].iloc[0] > i.superior):
            corpo_email = """
            <p>Vender %s</p>
            """%(i.ativo)

            msg = email.message.Message()
            msg['Subject'] = "Teste Celery"
            msg['From'] = 'gfkjyf@gmail.com'
            msg['To'] = i.email
            password = 'onwdolbcsxpawooe' 
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email )

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado para venda da', i.ativo)

        if(x['Close'].iloc[0] < i.inferior):
            corpo_email = """
            <p>Comprar %s</p>
            """%(i.ativo)

            msg = email.message.Message()
            msg['Subject'] = "Teste Celery"
            msg['From'] = 'gfkjyf@gmail.com'
            msg['To'] = i.email
            password = 'onwdolbcsxpawooe' 
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email )

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado para compra da', i.ativo)