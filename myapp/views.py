from django.shortcuts import render
import xlwings as xw
import pandas as pd
from .models import Projeto
import sqlite3

#from typing import overload
#import openpyxl
#from openpyxl import load_workbook
#import os
#import zipfile
#import xlrd

# Função responsável por converter a matrícula/ função do colaborador em uma "chave":
def chave_matricula(matricula, função_colaborador):
    
    if matricula == 0:
        chave_matricula = função_colaborador.replace(' ', '')
    else:
        chave = str(matricula)
        chave_convertida = []
        
        for i in chave:
            if i == '0':
                chave_convertida.append('a')
            elif i == '1':
                chave_convertida.append('b')
            elif i == '2':
                chave_convertida.append('c')
            elif i == '3':
                chave_convertida.append('d')
            elif i == '4':
                chave_convertida.append('e')
            elif i == '5':
                chave_convertida.append('f')
            elif i == '6':
                chave_convertida.append('g')
            elif i == '7':
                chave_convertida.append('h')
            elif i == '8':
                chave_convertida.append('i')
            else:
                chave_convertida.append('j')
            
        chave_matricula = ''.join(chave_convertida)

    return chave_matricula

# Função responsável por armazenar os dados das planilhas no banco de dados:
def banco_dados(nome_projeto, nome_cliente, status_projeto,
    mês_início_projeto, ano_início_projeto, duração_projeto, matricula_colaborador,
    chave_matricula,colaborador, função_colaborador, alocação_mensal, resumo):
    projeto = Projeto()
    projeto.nome_projeto = nome_projeto
    projeto.nome_cliente = nome_cliente
    projeto.status_projeto = status_projeto
    projeto.mês_início_projeto = mês_início_projeto
    projeto.ano_início_projeto = ano_início_projeto
    projeto.duração_projeto = duração_projeto
    projeto.matricula_colaborador = matricula_colaborador
    projeto.chave_matricula = chave_matricula
    projeto.colaborador = colaborador
    projeto.função_colaborador = função_colaborador
    projeto.alocação_mensal = alocação_mensal
    projeto.resumo = resumo
    projeto.save()

# Função responsável por gerar uma lista de projetos "em andamento":
def lista_projetos():

    projetos = list()

    status_procurado = 'Em Andamento'

    connection = sqlite3.connect('db.sqlite3')
    c = connection.cursor()

    sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'

    for row in c.execute(sql, (status_procurado,)):
        converter_lista = eval(row[10])
        if converter_lista[0] not in projetos:
            projetos.append(converter_lista[0])
        
    connection.close()

    return projetos

# Função responsável por gerar uma lista de projetos "em negociação":
def projetos_prospeccao():

    projetos_prospeccao = list()

    status_procurado_1 = 'Em Negociação 1'
    status_procurado_2 = 'Em Negociação 2'

    connection = sqlite3.connect('db.sqlite3')
    c = connection.cursor()

    sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ? or status_projeto = ?'
    
    for row in c.execute(sql, (status_procurado_1, status_procurado_2,)):
        converter_lista = eval(row[10])
        if converter_lista[0] not in projetos_prospeccao:
            projetos_prospeccao.append(converter_lista[0])
        
    connection.close()

    return projetos_prospeccao

# Função responsável por agrupar as alocações dos colaboradores:
def agrupar_alocacoes(excel_data_geral):
    
    excel_data = list()
    lista_matriculas = list()
    lista_funcao = list()

    # Selecionar os colaboradores não repetidos:

    for row1 in excel_data_geral:
        count = 0
        for row2 in excel_data_geral: 
            if row1[6] != 0 and row1[6] == row2[6]:
                count += 1
                row1[0] = 'Agrupado'
            if row1[6] == 0 and row1[9] == row2[9]: # Filtra pela função
                count += 1
                row1[0] = 'Agrupado'
            
        if count == 1:
            excel_data.append(row1)

    # Selecionar os colaboradores repetidos:

    excel_data_repetidos = list()

    for row1 in excel_data_geral:
        count = 0
        for row2 in excel_data_geral:
            if row1[6] != 0 and row1[6] == row2[6]:
                count += 1
            if row1[6] == 0 and row1[9] == row2[9]: # Filtra pelo função
                count += 1
        
        if count > 1:
            excel_data_repetidos.append(row1)

    # Agrupar as alocações dos colaboradores repetidos:

    count1 = 0
    for row1 in excel_data_repetidos:
        count2 = 0   
        for row2 in excel_data_repetidos:
            if row1[6] != 0 and row1[7] == row2[7] and row1[6] == row2[6]: # Filtra pela matrícula
                if count1 < count2:
                    for posicao in range(10,22):
                        row1[posicao] += row2[posicao]
                    row1[0] = 'Agrupado'
            if row1[6] == 0 and row1[7] == row2[7] and row1[9] == row2[9]: # Filtra pelo função
                if count1 < count2:
                    for posicao in range(10,22):
                        row1[posicao] += row2[posicao]
                    row1[0] = 'Agrupado'

            count2 += 1
        count1 += 1
        
        if row1[6] != 0 and row1[6] not in lista_matriculas:
            excel_data.append(row1)
            lista_matriculas.append(row1[6])
        if row1[6] == 0 and row1[9] not in lista_funcao:
            excel_data.append(row1)
            lista_funcao.append(row1[9])
                
    return excel_data

# Função responsável por renderizar os projetos "em andamento":
def andamento(request):

    if "GET" == request.method:
        return render(request, 'myapp/index.html', {})
    else:
        status_procurado = 'Em Andamento'
        
        excel_data_geral = list()
        excel_data = list()
        
        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'

        for row in c.execute(sql, (status_procurado,)):
            converter_lista = eval(row[10])
            excel_data_geral.append(converter_lista)
            
        connection.close()

        projetos = list()
        projetos = lista_projetos()
        prospeccao = list()
        prospeccao = projetos_prospeccao()

        # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
        excel_data = agrupar_alocacoes(excel_data_geral)

        # Fazer outra consulta ao banco e acrescentar ao excel_data:
        converter_lista_1 = list()

        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql_1 = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'

        for row in c.execute(sql_1, (status_procurado,)):
            converter_lista_1 = eval(row[10])
            excel_data.append(converter_lista_1)
            
        connection.close()

        return render(request, 'myapp/index.html', {"excel_data":excel_data, "projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por renderizar os projetos "em andamento" mesclados com "em negociação":
def negociacao(request):

    if "GET" == request.method:
        return render(request, 'myapp/index.html', {})
    else:
        lista_proj_negociacao = list()
        lista_proj_negociacao = request.POST.getlist('projeto')

        status_procurado = 'Em Andamento'
        
        excel_data_geral = list()
        excel_data = list()
        
        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        # Trazer somente projetos "Em Andamento":
        sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'
        for row in c.execute(sql, (status_procurado,)):
            converter_lista = eval(row[10])
            excel_data_geral.append(converter_lista)

        # Trazer somente projetos "Em Negociação" conforme lista do botão:
        for row1 in lista_proj_negociacao:
            sql = 'SELECT * FROM myapp_projeto WHERE nome_projeto = ?'
            for row2 in c.execute(sql, (row1,)):
                converter_lista = eval(row2[10])
                excel_data_geral.append(converter_lista)
            
        connection.close()

        # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
        excel_data = agrupar_alocacoes(excel_data_geral)

        # Fazer outra consulta ao banco e acrescentar ao excel_data:
        converter_lista = list()

        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        # Trazer somente "Em Andamento":
        sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'
        for row in c.execute(sql, (status_procurado,)):
            converter_lista = eval(row[10])
            excel_data.append(converter_lista)

        # Trazer somente "Em Negociação" conforme lista do botão:
        for row1 in lista_proj_negociacao:
            sql = 'SELECT * FROM myapp_projeto WHERE nome_projeto = ?'
            for row2 in c.execute(sql, (row1,)):
                converter_lista = eval(row2[10])
                excel_data.append(converter_lista)
    
        connection.close()

        projetos = list()
        projetos = lista_projetos()
        prospeccao = list()
        prospeccao = projetos_prospeccao()

        return render(request, 'myapp/index.html', {"excel_data":excel_data, "projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por pesquisar um colaborador:
def colaborador(request):

    if "GET" == request.method:
        return render(request, 'myapp/index.html', {})
    else:
        try:
            colaborador_procurado = request.POST['colaborador']

            excel_data_geral = list()
            excel_data = list()
            
            connection = sqlite3.connect('db.sqlite3')
            c = connection.cursor()

            sql_1 = 'SELECT * FROM myapp_projeto WHERE colaborador = ?'

            for row in c.execute(sql_1, (colaborador_procurado,)):
                converter_lista = eval(row[10])
                matricula = converter_lista[6]

            if matricula != 0:
                sql_2 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ?'

                for row in c.execute(sql_2, (matricula,)):
                    converter_lista = eval(row[10])
                    excel_data_geral.append(converter_lista)

            else:
                sql_3 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ? and colaborador = ?'

                for row in c.execute(sql_3, (matricula, colaborador_procurado,)):
                    converter_lista = eval(row[10])
                    excel_data_geral.append(converter_lista)
                
            connection.close()

            projetos = list()
            projetos = lista_projetos()

            prospeccao = list()
            prospeccao = projetos_prospeccao()

            # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
            excel_data = agrupar_alocacoes(excel_data_geral)
            
            # Fazer outra consulta ao banco e acrescentar ao excel_data:
            converter_lista_1 = list()

            connection = sqlite3.connect('db.sqlite3')
            c = connection.cursor()

            if matricula != 0:
                sql_2 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ?'

                for row in c.execute(sql_2, (matricula,)):
                    converter_lista_1 = eval(row[10])
                    excel_data.append(converter_lista_1)

            else:
                sql_3 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ? and colaborador = ?'

                for row in c.execute(sql_3, (matricula, colaborador_procurado,)):
                    converter_lista_1 = eval(row[10])
                    excel_data.append(converter_lista_1)

            connection.close()

        except:
            projetos = list()
            projetos = lista_projetos()
            prospeccao = list()
            prospeccao = projetos_prospeccao()

            mensagem = 'COLABORADOR NÃO ENCONTRADO OU NOME DIGITADO INCORRETAMENTE.'

            return render(request, 'myapp/detalheColaborador.html', {"mensagem": mensagem, "projetos":projetos, "projetos_prospeccao":prospeccao})
        
        return render(request, 'myapp/detalheColaborador.html', {"excel_data":excel_data, "projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por rederizar a tela inicial e fazer o upload das planilhas:
def index(request):

    if "GET" == request.method:
        projetos = list()
        projetos = lista_projetos()
        prospeccao = list()
        prospeccao = projetos_prospeccao()
        return render(request, 'myapp/index.html', {"projetos":projetos, "projetos_prospeccao":prospeccao})
    else:
        # Apaga todas as planilhas que estão no banco antes do upload das novas planilhas:
        # projeto = Projeto.objects.all()
        # projeto.delete()

        lista_excel_file = request.FILES.getlist("excel_file")

        for planilha in lista_excel_file:
        
            #############################################################
            # OPÇÃO 1: Subir várias planilhas fechadas (Versão Pandas):
            
            wb = pd.ExcelFile(planilha)
            worksheet1 = pd.read_excel(wb, sheet_name='Geral')
            worksheet2 = pd.read_excel(wb, sheet_name='RH CLT')
            worksheet2.fillna(0, inplace=True)

            # Fim da opção 1.
            #############################################################

            #############################################################
            # OPÇÃO 2: Subir várias planilha abertas (Versão xlwings):

            # file_name = str(planilha)
            # wb = xw.Book(file_name)
            # df1 = wb.sheets['Geral']
            # worksheet1 = df1['A1:N112'].options(pd.DataFrame, index=False, header=True).value
            # df2 = wb.sheets['RH CLT']
            # worksheet2 = df2['A1:AV30'].options(pd.DataFrame, index=False, header=True).value
            # worksheet2.fillna(0, inplace=True)

            ### Fim da opção 2.
            #############################################################

            # Apaga apenas uma planilha (caso já exista no banco) antes do upload substituindo pela nova planilha:
            nomeProjeto = str(worksheet1.loc[5][4])
            projeto = Projeto.objects.filter(nome_projeto=nomeProjeto)
            projeto.delete()

            excel_data_geral = list()
            
            row = 6
            count1 = 0

            while count1 < 12: 
                
                row_data = list()
                
                if worksheet2.loc[row][1] != 0 or worksheet2.loc[row][2] != 0 or worksheet2.loc[row][4] != 0:
                    
                    row_data.append(str(worksheet1.loc[5][4])) # Nome do Projeto
                    row_data.append(str(worksheet1.loc[7][4])) # Nome do Cliente
                    row_data.append(str(worksheet1.loc[15][9])) # Status do Projeto
                    row_data.append(str(worksheet1.loc[24][4])) # Mês de Início do Projeto
                    row_data.append(int(worksheet1.loc[24][10])) # Ano de Início do Projeto
                    row_data.append(int(worksheet1.loc[26][4])) # Duração do Projeto
                    row_data.append(int(worksheet2.loc[row][1])) # Matrícula do Colaborador

                    chave = chave_matricula(worksheet2.loc[row][1], str(worksheet2.loc[row][4]))
                    row_data.append(chave) # Chave da Matrícula

                    row_data.append(str(worksheet2.loc[row][2])) # Colaborador
                    row_data.append(str(worksheet2.loc[row][4])) # Função do colaborador

                    col = 28
                    count2 = 0
                    alocação_mensal = list()                    

                    # Considerar sempre um ano corrente (12 meses):
                    while count2 < 12:
                        row_data.append(int(worksheet2.loc[row][col]*100))
                        alocação_mensal.append(int(worksheet2.loc[row][col]*100)) # Alocação mensal
                        count2 += 1
                        col += 1

                    excel_data_geral.append(row_data)

                    # SALVA AS PLANILHAS NO BANCO DE DADOS:
                    banco_dados(
                        str(worksheet1.loc[5][4]),
                        str(worksheet1.loc[7][4]),
                        str(worksheet1.loc[15][9]),
                        str(worksheet1.loc[24][4]),
                        int(worksheet1.loc[24][10]),
                        int(worksheet1.loc[26][4]),
                        int(worksheet2.loc[row][1]),
                        chave,
                        str(worksheet2.loc[row][2]),
                        str(worksheet2.loc[row][4]),
                        alocação_mensal,
                        row_data)

                row += 1
                count1 += 1
        
        projetos = list()
        projetos = lista_projetos()
        prospeccao = list()
        prospeccao = projetos_prospeccao()

        # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
        excel_data = list()
        excel_data = agrupar_alocacoes(excel_data_geral)

        return render(request, 'myapp/index.html', {"excel_data":excel_data, "projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por pesquisar um projeto "em andamento":
def pesquisar_projeto(request, nome_projeto):

    if "POST" == request.method:
        return render(request, 'myapp/index.html', {})
    else: 
        pesquisar_projeto = nome_projeto
        excel_data = list()

        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql = 'SELECT * FROM myapp_projeto WHERE nome_projeto = ?'

        for row in c.execute(sql, (pesquisar_projeto,)):
            converter_lista = eval(row[10])
            excel_data.append(converter_lista)
            
        connection.close()

        projetos = list()
        projetos = lista_projetos()

        prospeccao = list()
        prospeccao = projetos_prospeccao()

        return render(request, 'myapp/pesquisarProjeto.html', {"excel_data":excel_data, "projeto": nome_projeto,"projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por gerar a lista de projetos por colaborador:
def detalheColaborador(request, colaborador):

    if "POST" == request.method:
        return render(request, 'myapp/index.html', {})
    else:
        colaborador_procurado = colaborador

        excel_data_geral = list()
        
        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql_1 = 'SELECT * FROM myapp_projeto WHERE colaborador = ?'

        for row in c.execute(sql_1, (colaborador_procurado,)):
            converter_lista = eval(row[10])
            matricula = converter_lista[6]

        if matricula != 0:
            sql_2 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ?'

            for row in c.execute(sql_2, (matricula,)):
                converter_lista = eval(row[10])
                excel_data_geral.append(converter_lista)

        else:
            sql_3 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ? and colaborador = ?'

            for row in c.execute(sql_3, (matricula, colaborador_procurado,)):
                converter_lista = eval(row[10])
                excel_data_geral.append(converter_lista)

        connection.close()

        # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
        excel_data = list()
        excel_data = agrupar_alocacoes(excel_data_geral)

        # Fazer outra consulta ao banco e acrescentar ao excel_data:
        converter_lista_1 = list()

        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        if matricula != 0:
            sql_2 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ?'

            for row in c.execute(sql_2, (matricula,)):
                converter_lista_1 = eval(row[10])
                excel_data.append(converter_lista_1)

        else:
            sql_3 = 'SELECT * FROM myapp_projeto WHERE matricula_colaborador = ? and colaborador = ?'

            for row in c.execute(sql_3, (matricula, colaborador_procurado,)):
                converter_lista_1 = eval(row[10])
                excel_data.append(converter_lista_1)

        connection.close()
        
        projetos = list()
        projetos = lista_projetos()

        prospeccao = list()
        prospeccao = projetos_prospeccao()

    return render(request, 'myapp/detalheColaborador.html', {"excel_data":excel_data, "projetos":projetos, "projetos_prospeccao":prospeccao})

# Função responsável por sugerir a equalização das alocações:
def match(request):

    if "GET" == request.method:
        return render(request, 'myapp/index.html', {})
    else:
        status_procurado = 'Em Andamento'
        
        excel_data_geral = list()
        excel_data = list()
        
        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'

        for row in c.execute(sql, (status_procurado,)):
            converter_lista = eval(row[10])
            excel_data_geral.append(converter_lista)
            
        connection.close()

        projetos = list()
        projetos = lista_projetos()
        prospeccao = list()
        prospeccao = projetos_prospeccao()

        # FUNÇÃO PARA AGRUPAR AS ALOCAÇÕES POR COLABORADOR:
        excel_data = agrupar_alocacoes(excel_data_geral)

        # Fazer outra consulta ao banco e acrescentar ao excel_data:
        converter_lista_1 = list()

        connection = sqlite3.connect('db.sqlite3')
        c = connection.cursor()

        sql_1 = 'SELECT * FROM myapp_projeto WHERE status_projeto = ?'

        for row in c.execute(sql_1, (status_procurado,)):
            converter_lista_1 = eval(row[10])
            excel_data.append(converter_lista_1)
            
        connection.close()

        colaboradores_overAllocation = list()

        # Declaração do valor máximo para as Alocações Agrupadas:
        alocacao_agrupada = 100

        for row in excel_data:
            if row[0] == 'Agrupado':
                for posicao in range(10,22):
                    if row[posicao] > alocacao_agrupada:
                        colaboradores_overAllocation.append(row)
                        break

        lista_colaboradores_overAllocation = list()

        for row1 in colaboradores_overAllocation:
            for row2 in excel_data:
                if row1[6] == row2[6] and row1[7] == row2[7]:
                    lista_colaboradores_overAllocation.append(row2)

        colaboradores_match = list()
        lista_match = list()

        for row1 in lista_colaboradores_overAllocation:
            if row1[0] != 'Agrupado':
                for row2 in excel_data:
                    if row2[0] == 'Agrupado':
                        if row1[6] != row2[6] and row1[7] != row2[7] and row1[9] == row2[9]:
                            contador = 0
                            for posicao in range(10,22):
                                if row1[posicao] <= (100 - row2[posicao]):
                                    contador += 1
                                else:
                                    break
                            if contador == 12:
                                if row2 not in lista_match:
                                    colaboradores_match.append(row2)
                                    lista_match.append(row2)

        lista_colaboradores_match = list()

        for row1 in colaboradores_match:
            for row2 in excel_data:
                if row1[6] == row2[6] and row1[7] == row2[7]:
                    lista_colaboradores_match.append(row2)

        if not lista_colaboradores_match:
            mensagem = 'NÃO HÁ MATCH POSSÍVEL PARA AS PLANILHAS CARREGADAS.'
            return render(request, 'myapp/match.html', {"mensagem": mensagem, "projetos":projetos, "projetos_prospeccao":prospeccao})
        else:
            return render(request, 'myapp/match.html', {"lista_colaboradores_overAllocation":lista_colaboradores_overAllocation, "lista_colaboradores_match": lista_colaboradores_match, "projetos":projetos, "projetos_prospeccao":prospeccao})

