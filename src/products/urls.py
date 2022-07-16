import py_compile
from django.urls import path
from .views import index, ativos

app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('ativos/', ativos, name='ativos'),

    # path('', cotacao, name='cotacao-ativo')
]