from django.shortcuts import render
from .models import Info
import json
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .forms import InfoForm
# Create your views here.

def index(request):
    form = InfoForm(request.POST or None)
    mensagem_confirmacao=None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        form = InfoForm()
        mensagem_confirmacao = "Ativo configurado"
    context = {
        'form': form,
        'mensagem_confirmacao': mensagem_confirmacao,
    }
    return render(request, 'products/main.html', context)

def ativos(request):
    context = {
        'form': 'form',
        'mensagem_confirmacao': 'mensagem_confirmacao',
    }
    return render(request, 'products/main.html', context)