from django.shortcuts import render
from .models import Info
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime
import time
# Create your views here.

def chart_select_view(request):
    print('TESTE REQUEST')
    print(request.POST.get('ativo'))

    print('TESTE COTACAO')
    while True:
        x = web.DataReader('PETR4.SA', data_source='yahoo', start='07-10-2022', end=datetime.now())
        x = pd.DataFrame(x)
        print(x['Close'])
        time.sleep(2)


    # product_df = pd.DataFrame(Product.objects.all().values())
    # purchase_df = pd.DataFrame(Purchase.objects.all().values())
    # context = {
    #     'products' : product_df.to_html(), 
    #     'purchase' : purchase_df.to_html()
    # }

    # return render(request, 'products/main.html', context)


# def cotacao (request):
    # print(request.POST.get('ativo'))
    # abev = abev.history(period="7d",  interval = "1m")
    # print(abev)