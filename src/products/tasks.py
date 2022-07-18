from celery import shared_task
from .models import Info
import smtplib
import email.message
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime
from django_celery_beat.models import PeriodicTask
from .utils import mandarEmail


@shared_task(name="enviar_email")
def enviar_email(id):
    ativo = Info.objects.get(id=id)
    print(ativo.date)
    x = web.DataReader(ativo.ativo, data_source='yahoo', start='07-15-2022', end=datetime.now())
    x = pd.DataFrame(x)

    print("Valor da ação", x['Close'])
    print("valor pra venda", ativo.superior)
    print("valor pra compra", ativo.inferior)

    if(x['Close'].iloc[0] > ativo.superior):
        mandarEmail('Vender ', ativo.ativo, ativo.email)

    if(x['Close'].iloc[0] < ativo.inferior):
        mandarEmail('Comprar ', ativo.ativo, ativo.email)
