import py_compile
from django.urls import path
from .views import index, ativos, editar

app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('ativos/', ativos, name='ativos'),
    path('editar/<int:ativo_id>', editar, name='editar')

    # path('', cotacao, name='cotacao-ativo')
]