# desafio_alpha

## Para rodar, execute cada um em um terminal diferente
python manage.py runserver

celery -A desafio_alpha beat -l info

celery -A desafio_alpha worker -l INFO

(Também é necessario ter o Redis rodando)

## Lista de algumas empresas para teste (fonte dos dados:https://finance.yahoo.com/)

Petrobras - PETR4.SA

IBOVESPA - ^BVSP

Magazine Luiza - MGLU3.SA

Americanas - AMER3.SA
