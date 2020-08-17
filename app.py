from flask import Flask, render_template, Response
from datetime import datetime
from logger import *
from constants import *
from util import *

import requests


app = Flask(__name__)
app.secret_key = "5or414C3nP35p37R0Br45"


@app.route('/')
def index():
    try:
        # Consulta a URL de previsao do tempo
        response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall?lat=-21.1775&lon=-47.81028&exclude=current,minutely,hourly&appid=40cc6ad84040b70182525558635153e5")
        # Pega o retorno em JSON
        resposta = response.json()
        # Pega apenas a lista desejada que vem no atributo 'daily'
        lista = resposta['daily']
        # Pega a temperatura atual do primeiro elemento da lista (hoje), tranformando-o de Kelvin para Celsius
        temp_atual = int(float(lista[0]['temp']['day']) - 273.15)
        # Separa os dados necessarios dos 5 primeiros dias da lista
        lista_humidade = []
        lista_dias_quarda_chuva = []
        for item in lista[:5]:
            data = datetime.fromtimestamp(item['dt'])
            elem = {
                'dia': DIAS_SEMANA[data.weekday()],
                'humidade': item['humidity']
            }
            lista_humidade.append(elem)

            # Condicao para apresentar msg para o "dia"
            if float(item['humidity']) > HUMIDADE:
                lista_dias_quarda_chuva.append(DIAS_SEMANA[data.weekday()])

            # Formata a string dos dias da semana, caso existam
            dias_quarda_chuva = ''
            if len(lista_dias_quarda_chuva) > 0:
                dias_quarda_chuva = formatar_string_dias(lista_dias_quarda_chuva)

        # Retorno
        return render_template("index.html", temperatura=temp_atual, humidades=lista_humidade,
                               dias_quarda_chuva=dias_quarda_chuva)
    except Exception as ex:
        msg = "Erro carregando os dados de previsão de tempo."
        logger.exception(msg)
        return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True, port=PORTA)
