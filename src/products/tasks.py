from celery import shared_task
from .models import Info
import smtplib
import email.message
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime
from django_celery_beat.models import PeriodicTask



@shared_task(name="enviar_email")
def enviar_email(id):
    ativo = Info.objects.get(id=id)
    print(ativo.date)
    x = web.DataReader(ativo.ativo, data_source='yahoo', start=datetime.date(ativo.date), end=datetime.now())
    x = pd.DataFrame(x)

    print("Valor da ação", x['Close'])
    print("valor pra venda", ativo.superior)
    print("valor pra compra", ativo.inferior)

    if(x['Close'].iloc[0] > ativo.superior):
        corpo_email = """
        <p>Vender %s</p>
        """%(ativo.ativo)

        msg = email.message.Message()
        msg['Subject'] = "Teste Celery"
        msg['From'] = 'gfkjyf@gmail.com'
        msg['To'] = ativo.email
        password = 'onwdolbcsxpawooe' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado para venda da', ativo.ativo)

    if(x['Close'].iloc[0] < ativo.inferior):
        corpo_email = """
        <p>Comprar %s</p>
        """%(ativo.ativo)

        msg = email.message.Message()
        msg['Subject'] = "Teste Celery"
        msg['From'] = 'gfkjyf@gmail.com'
        msg['To'] = ativo.email
        password = 'onwdolbcsxpawooe' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado para compra da', ativo.ativo)