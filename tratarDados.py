#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Faz o tratamento dos dados de financiamento para campanha presidencial dos EUA de 2016.
Os tratamentos realizados são os seguintes:
- Verifica o valor da contribuição
- Separa a data nos componentes dia, mês e ano
- Cria coluna com o partido dos candidatos
- Cria coluna com o nome dos comites
"""
import csv
import zipcode
import pprint

ESTADO_EUA = "TX"

NOME_ARQUIVO = "P00000001-"+ESTADO_EUA+".csv"
NOME_ARQUIVO_TRATADO = "P00000001-"+ESTADO_EUA+"_tratado.csv"

def recuperar_dados_cidade_pelo_cep(cep):
    """
    Usa um biblioteca de zipcode dos EUA pra equalizar os nomes de cidades
    da base de dados e obter longitude e latidude.
    """
    if cep is not None or cep != "":
        #Utiliza apenas os 5 primeiros digitos do CEP
        numero_cep = cep[0:5]
        try:
            zip = zipcode.isequal(numero_cep)
            if zip is not None:
                return zip.city, zip.lon, zip.lat
            else:
                return "", "", ""
        except ValueError:
            return "", "", ""
    else:
        return "", "", ""

def tratar_valor_contribuicao(valor_contribuicao):
    """
    Converte os valores negativos em positivos e elimina os registros com valor 0
    """
    valor_contribuicao = float(valor_contribuicao)
    valor_contribuicao = abs(valor_contribuicao)
    if (valor_contribuicao == 0):
        return None
    return valor_contribuicao

def tratar_data_contribuicao(data):
    data_separada = data.split('-')
    dia = data_separada[0]
    mes = data_separada[1]
    ano = data_separada[2]
    return dia, mes, ano

def tratar_ocupacao(ocupacao):
    if ocupacao in ["OWNER", "SELF", "BUSINESS OWNER", "SMALL BUSINESS OWNER","SELF EMPLOYED"]:
        return "SELF-EMPLOYED"
    if ocupacao in ["REALTOR", "REAL ESTATE BROKER"]:
        return "REAL ESTATE"
    if ocupacao == "ATTORNEY":
        return "LAWYER"
    if ocupacao in ["PROGRAMMER","WEB DEVELOPER"]:
        return "SOFTWARE DEVELOPER"
    if ocupacao == "PROFESSOR":
        return "TEACHER"
    if ocupacao == "R.N.":
        return "RN"
    if ocupacao == "NONE":
        return "NOT EMPLOYED"
    if ocupacao == "ACCOUNTING":
        return "ACCOUNTANT"
    if ocupacao == "INSURANCE AGENT":
        return "INSURANCE"
    if ocupacao in ["N/A","INFORMATION REQUESTED PER BEST EFFORTS","INFORMATION REQUESTED"]:
        return ""
    if "NURSE" in ocupacao:
        return "NURSE"
    return ocupacao


def adicionar_novos_titulos(header):
    header.append('city')
    header.append('lon')
    header.append('lat')
    header.append('party')
    header.append('cmte_nm')
    header.append('cmte_dsgn')
    header.append('contb_receipt_dt_day')
    header.append('contb_receipt_dt_month')
    header.append('contb_receipt_dt_year')

    return header

def tratar_dados_financiamento(dados, candidatos, comite):
    """
    Faz o tratamento dos dados do dataset
    """
    dados_tratados = []
    for data in dados:
        #Trata valores de contribuições negativas
        valor = tratar_valor_contribuicao(data['contb_receipt_amt'])
        if valor is None:
            continue
        data['contb_receipt_amt'] = valor
#        print(posicao)

        data['contbr_occupation'] = tratar_ocupacao(data['contbr_occupation'])

        data['cmte_nm'] = comite[data['cmte_id']][1]
        data['cmte_dsgn'] = comite[data['cmte_id']][8]

        data['party'] = candidatos[data['cand_id']][2]

        dia, mes, ano = tratar_data_contribuicao(data['contb_receipt_dt'])
        data['contb_receipt_dt_day'] = dia
        data['contb_receipt_dt_month'] = mes
        data['contb_receipt_dt_year'] = ano

        #Recupera dados das cidades com base no CEP
        city, lon, lat = recuperar_dados_cidade_pelo_cep(data['contbr_zip'])
        data['city'] = city
        data['lon'] = lon
        data['lat'] = lat

        del data['memo_cd']
        del data['memo_text']

        dados_tratados.append(data)

    return dados_tratados

def carregar_dados_financiamento(nome_arquivo):
    """
    Carrega os dados de financiamento
    """
    dados = []
    with open(nome_arquivo, 'r') as f:
        reader = csv.DictReader(f)
        titulo = reader.fieldnames
        for row in reader:
            del row['']
            dados.append(row)
    return titulo, dados

def carregar_dados_candidatos(nome_arquivo):
    """
    Carrega os dados dos candidatos
    """
    dados = {}
    with open(nome_arquivo, 'r') as f:
        filedata = csv.reader(f, delimiter='|')
        for row in filedata:
            if row[5] == 'P':
                dados[row[0]] = row

    return dados

def carregar_dados_comite(nome_arquivo):
    """
    Carrega os dados dos comites
    """
    dados = {}
    with open(nome_arquivo, 'r') as f:
        filedata = csv.reader(f, delimiter='|')
        for row in filedata:
            dados[row[0]] = row

    return dados

def grava_dados_financiamento(arquivo_saida, dados_tratados, header):
    """
    Grava o arquivo com os dados a serem analisados
    """
    with open(arquivo_saida, "w") as saida:
        writer = csv.DictWriter(saida, delimiter=",", fieldnames = header)
        writer.writeheader()
        for row in dados_tratados:
            writer.writerow(row)

def executarTratamento():
    header, dados = carregar_dados_financiamento(NOME_ARQUIVO)
    candidatos = carregar_dados_candidatos("cn.txt")
    comite = carregar_dados_comite("cm.txt")
    header = adicionar_novos_titulos(header)
    dados_tratados = tratar_dados_financiamento(dados, candidatos, comite)
    pprint.pprint(dados_tratados[0])
    grava_dados_financiamento(NOME_ARQUIVO_TRATADO, dados_tratados, header)

if __name__ == "__main__":
    executarTratamento()