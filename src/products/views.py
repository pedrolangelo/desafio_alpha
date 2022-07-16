from django.shortcuts import render
from .models import Info
import json
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .forms import InfoForm
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    form = InfoForm(request.POST or None)
    mensagem_confirmacao=None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        form = InfoForm()
        mensagem_confirmacao = "Ativo configurado"
    objs = Info.objects.all()
    context = {
        'form': form,
        'objs': objs,
        'mensagem_confirmacao': mensagem_confirmacao,
    }
    return render(request, 'products/main.html', context)

def editar(request, ativo_id):
    if(request.method == 'GET'):
        ativos = InfoForm()
        ativo = Info.objects.filter(id=ativo_id).first()
        form = InfoForm(instance=ativo)
        print('ativo', ativo)

        context = {
            'objs': ativos,
            'ativo': form,
        }
        return render(request, 'products/ativos.html', context)

    elif (request.method == 'POST'):
        ativo = Info.objects.filter(id=ativo_id).first()
        form = InfoForm(request.POST, instance=ativo)
        if form.is_valid():
            ativo = form.save(commit=False)
            ativo.save()
            return HttpResponseRedirect("/")

        form = InfoForm()

    return render(request, 'products/ativos.html', context)


def ativos(request):
    objs = Info.objects.all()

    form = InfoForm()
    context = {
        'objs': objs,
    }

    return render(request, 'products/ativos.html', context)