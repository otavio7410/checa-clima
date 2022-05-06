from configparser import ConfigParser
from urllib import parse, request, error
import sys
import json


URL_BASE_API = "https://api.weatherbit.io/v2.0/current"
lingua = "pt" 

def _pegar_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["apiweatherbit"]["api_key"]

def busca_url_clima(cidade, pais="", metrica=False):
    api_key = _pegar_api_key()
    #ajustando o nome da cidade trocando espaços por '+'
    cidadeNome = parse.quote_plus(cidade)
    paisNome = parse.quote_plus(pais) if pais != "" else ""

    url_cidade_pais = f"{cidadeNome}" + (
                      f"&country={paisNome}" if pais != "" else ""
                                        )

    url = (f"{URL_BASE_API}?key={api_key}"
           f"&city={url_cidade_pais}"
           f"&lang={lingua}"
           )

    return url

def busca_dados_clima(url):
    try:
        response = request.urlopen(url)
    except error.HTTPError as  http_error:
        if http_error.code == 401:
            sys.exit("Acesso negado, cheque a sua chave API.")
        elif http_error.code == 404:
            sys.exit("Cidade não encontrada.")
        else:
            sys.exit(f"Algo deu errado: {http_error.code}")

    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("O programa não conseguiu ler a resposta do servidor")


def mostrar_dados(dados_clima):
    cidade = dados_clima["data"][0]["city_name"]
    pais = dados_clima["data"][0]["country_code"]
    temp_celsius = dados_clima["data"][0]["temp"]
#    temp_fahrenheit = dados_clima["current"]["temp_f"]
    condicao_clima = dados_clima["data"][0]["weather"]["description"]
#    hora_ultima_checagem = dados_clima["current"]["last_updated"]

    print(f"{cidade}, {pais}", end="")
    print(f"\t{condicao_clima}, {temp_celsius}ºC")
#    print(f"Última checagem em: {hora_ultima_checagem.split()[1]} (horário local)")



if __name__ == "__main__":
    cidade = "São Paulo"
    pais = ""
    url_clima = busca_url_clima(cidade, pais)
    dados_clima = busca_dados_clima(url_clima)
    mostrar_dados(dados_clima) 
