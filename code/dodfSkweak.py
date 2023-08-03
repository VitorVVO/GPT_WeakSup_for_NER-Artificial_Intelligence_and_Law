# CODIGO DAS LABEL FUNCIONS E SUPERVISÃO FRACA

import re
import pandas as pd
import spacy
import skweak
from spacy.tokens import DocBin
import os


class LabelFunctionsContratos:
    '''
    Classe que armazena as Label Functions para a aplicacao da supervisao fraca em contratos

    Atributos: 
        self.docs = base de dados de contratos, no formato de um vetor de strings onde cada string representa um contrato
        self.vet = vetor auxiliar para detecção de entidades nas Label Functions
    '''

    def __init__(self, dados):
        nlp = spacy.load('pt_core_news_sm', disable=["ner", "lemmatizer"])
        self.docs = list(nlp.pipe(dados))

    def contrato_(self, doc):
        '''
        label function para extracao de contratos usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"([C|c][O|o][N|n|][T|t][R|r][A|a][T|t][O|o][\s\S].*?[s|:]?.+?(?=[0-9]).*?|[C|c][O|o][N|n|][V|v][E|e|Ê|ê][N|n][I|i][O|o][\s\S].*?[s|:]?.+?(?=[0-9]).*?)(\d*[^;|,|a-zA-Z]*)"
        match = re.search(expression, str(doc))
        if match:
            flag = 0
            for token in doc:
                if match.span(2)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                    if(doc[token.i].text == ':'):
                        start = doc[token.i+1]
                    else:
                        start = token
                    flag = 1
                if token.idx >= match.span(2)[1] and flag == 1 and token.i > start.i:
                    if(doc[token.i-1].text in ['.', '-', '—', ':']):
                        end = doc[token.i-1]
                    else:
                        end = token
                    yield start.i, end.i, "CONTRATO"
                    break

    def processo_(self, doc):
        '''
        label function para extracao de processo usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[P|p][R|r][O|o][C|c][E|e][S|s][S|s][O|o][\s\S].*?[s|:]?.+?(?=[0-9]).*?(\d*[^;|,|a-zA-Z]*)"
        match = re.search(expression, str(doc))
        if match:
            flag = 0
            for token in doc:
                if match.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                    if(doc[token.i].text == ':'):
                        start = doc[token.i+1]
                    else:
                        start = token
                    flag = 1
                if token.idx >= match.span(1)[1] and flag == 1 and token.i > start.i:
                    if(doc[token.i-1].text in ['.', '-', '—', ':']):
                        end = doc[token.i-1]
                    else:
                        end = token
                    yield start.i, end.i, "PROCESSO"
                    break

    def data_assinatura_(self, doc):
        '''
        label function para extracao de data de assinatura usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[A|a][S|s][S|s][I|i][N|n][A|a][T|t][U|u][R|r][A|a]:.*?[\s\S](\d{2}\/\d{2}\/\d{4}|\d{2}[\s\S]\w+[\s\S]\w+[\s\S]\w+[\s\S]\d{4})"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(1)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "DATA_ASS."
                        break

    def valor_(self, doc):
        '''
        label function para extracao de valor usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[V][a|A][l|L][o|O][r|R].*?[\s\S].*?([\d\.]*,\d{2})"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(1)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "VALOR"
                        break

    def unidade_orcamento_(self, doc):
        '''
        label function para extracao de unidade orcamentaria usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[u|U][n|N][i|I][d|D][a|A][d|D][e|E][\s\S][o|O][r|R][c|C|ç|Ç][a|A][m|M][e|E][n|N][t|T][a|A|á|Á][r|R][i|I][a|A].*?[\s\S].*?(\d+.\d+)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(1)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "UNI_ORC."
                        break
        expression = r"([U][.][O].*?[\s\S].*?|[U][O][\s|:].*?[\s\S].*?)(\d+.\d+)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(2)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(2)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "UNI_ORC."
                        break

    def programa_trabalho_(self, doc):
        '''
        label function para extracao de programa de trabalho usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[P|p][R|r][O|o][g|G][r|R][a|A][m|M][a|A][\s|\S][d|D][e|E|O|o|A|a][\s|\S][T|t][R|r][A|a][B|b][A|a][L|l][H|h][O|o].*?[:|;|[\s\S].*?(\d*[^;|,|–|a-zA-Z]*)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(1)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "PROG_TRAB."
                        break
        expression = r"([P][.][T].*?[\s\S].*?|[P][T][\s|:].*?[\s\S].*?)(\d*[^;|,|–|a-zA-Z]*)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(2)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(2)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "PROG_TRAB."
                        break

    def natureza_despesa_(self, doc):
        '''
        label function para extracao de natureza de despesa usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"[N|n][a|A][t|T][u|U][r|R][e|E][z|Z][a|A][\s\S][D|d][e|E|a|A][\s\S][d|D][e|E][s|S][p|P][e|E][s|S][a|A][\s\S].*?(\d*[^;|,|–|(|a-zA-Z]*)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(1)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(1)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "NAT_DESP."
                        break
        expression = r"([N][.][D].*?[\s\S].*?|[N][D][\s|:].*?[\s\S].*?)(\d*[^;|,|–|(|a-zA-Z]*)"
        match = re.finditer(expression, str(doc))
        if match:
            for grupo in match:
                flag = 0
                for token in doc:
                    if grupo.span(2)[0]+1 in range(token.idx, (token.idx+len(token))+1) and flag == 0:
                        if(doc[token.i].text == ':'):
                            start = doc[token.i+1]
                        else:
                            start = token
                        flag = 1
                    if token.idx >= grupo.span(2)[1] and flag == 1 and token.i > start.i:
                        if(doc[token.i-1].text in ['.', '-', '—', ':']):
                            end = doc[token.i-1]
                        else:
                            end = token
                        yield start.i, end.i, "NAT_DESP."
                        break

    def nota_empenho_(self, doc):
        '''
        label function para extracao de nota de empenho usando regex

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        expression = r"(\d+NE\d+)"
        for match in re.finditer(expression, doc.text):
            if(match.groups):
                grupo = (match.groups()[0])
                grupo_copy = grupo
                if ("(" or ")") in grupo:
                    grupo = grupo.replace("(", "\(")
                    grupo = grupo.replace(")", "\)")
                tamanho = len(grupo.split())
                start = re.search(grupo, doc.text).span()[0]
                end = re.search(grupo, doc.text).span()[1]
                span = str(doc.char_span(start, end))
                x = re.findall(r'[\(|\)]', span)
                for token in doc:
                    if(grupo_copy in str(doc[token.i: token.i+tamanho+len(x)])):
                        yield token.i, token.i+tamanho+len(x), "NOTA_EMP."
                #         break
                # break

    def contrato_detector_fun(self, doc):
        '''
        label function para extracao de contrato com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        flag = 0
        for token in doc:
            if token.text in ['CONTRATO', 'Contrato', 'CONVÊNIO', 'CONVENIO', 'Convênio', 'Convenio']:
                if token.i+2 < len(doc):
                    for x in range(1, len(doc)-token.i):
                        if doc[token.i+x].text[0].isdigit() and doc[token.i+x].i < doc[token.i+x].i+1:
                            k = 0
                            if token.i+x+1 < len(doc):
                                if(doc[token.i+x+1].text[0].isdigit()):
                                    k = 1
                                yield doc[token.i+x].i, doc[token.i+x].i+1+k, "CONTRATO",
                                flag = 1
                                break
                    if flag == 1:
                        break

    def processo_detector_fun(self, doc):
        '''
        label function para extracao de processos com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.text in ['Processo', 'PROCESSO', 'Processo:', 'PROCESSO:']:
                if token.i+2 < len(doc):
                    for x in range(1, len(doc)-token.i):
                        if doc[token.i+x].text[0].isdigit() and doc[token.i+x].i < doc[token.i+x].i+1:
                            k = 0
                            if token.i+x+1 < len(doc):
                                if(doc[token.i+x+1].text[0].isdigit()):
                                    k = 1
                            yield doc[token.i+x].i, doc[token.i+x].i+1+k, "PROCESSO",
                            break

    def partes_detector_fun(self, doc):
        '''
        label function para extracao de partes com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            for y in ['Partes', 'PARTES', 'Partes:', 'partes:', 'partícipes', 'partícipes:', 'Partícipes', 'Partícipes:', 'CONTRATADAS:', 'Contratadas:', 'CONTRATADAS', 'Contratadas', 'CONTRATANTES:', 'Contratantes:', 'Contratantes', 'CONTRATANTES', 'CONTRATANTES:']:
                if token.i+2 < len(doc):
                    if y in token.text:
                        k = 0
                        if(doc[token.i+1].text == ':'):
                            k += 1
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Processo', 'PROCESSO', 'Processo:', 'PROCESSO:', 'Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "PARTES"
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "PARTES"
                                break

    def objeto_detector_fun(self, doc):
        '''
        label function para extracao de objeto com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        flag = 0
        for token in doc:
            if token.i+2 < len(doc):
                if token.text in ['Objeto', 'OBJETO']:
                    k = 0
                    if(doc[token.i+1].text == ':'):
                        k += 1
                    for x in range(1+k, len(doc)-token.i):
                        if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                            flag = 1
                            yield token.i+1+k, token.i+x, "OBJETO"
                            break
                        elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                            yield token.i+1+k, token.i+x+1, "OBJETO"
                            break
            if token.i+3 < len(doc):
                if token.text in ['Do', 'DO'] and doc[token.i+1].text in ['objeto', 'objeto:']:
                    k = 0
                    if(doc[token.i+2].text == ':'):
                        k += 1
                    for x in range(2+k, len(doc)-token.i):
                        if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                            flag = 1
                            yield token.i+1+k, token.i+x, "OBJETO"
                            break
                        elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                            yield token.i+1+k, token.i+x+1, "OBJETO"
                            break
            if token.i+4 < len(doc):
                if token.text in ['tem', 'Tem'] and doc[token.i+1].text in ['por', 'POR'] and doc[token.i+2].text in ['objeto', 'Objeto', 'OBJETO'] and flag == 0:
                    k = 0
                    if(doc[token.i+3].text == ':'):
                        k += 1
                    for x in range(3+k, len(doc)-token.i):
                        if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i < token.i+x:
                            yield token.i, token.i+x, "OBJETO"
                            break
                        elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                            yield token.i+1+k, token.i+x+1, "OBJETO"
                            break

    def valor_detector_fun(self, doc):
        '''
        label function para extracao de valor com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+3 < len(doc):
                for y in ['Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:']:
                    if y in token.text:
                        for x in range(1, len(doc)-token.i-2):
                            if (doc[token.i+x].text in ['R$', '$', '$$'] and doc[token.i+x+1].text[0].isdigit()) and doc[token.i+x].i+1 < doc[token.i+x].i+2:
                                yield doc[token.i+x].i+1, doc[token.i+x].i+2, "VALOR",
                                break
            if token.i+4 < len(doc):
                if token.text in ['Do', 'DO'] and doc[token.i+1].text in ['valor', 'valor:']:
                    for x in range(2, len(doc)-token.i-2):
                        if (doc[token.i+x].text in ['R$', '$', '$$'] and doc[token.i+x+1].text[0].isdigit()) and doc[token.i+x].i+1 < doc[token.i+x].i+2:
                            yield doc[token.i+x].i+1, doc[token.i+x].i+2, "VALOR",
                            break
            if token.i+4 < len(doc):
                if 'valor' in token.text and doc[token.i+1].text in ['TOTAL', 'Total', 'total', 'TOTAL:', 'Total:', 'total:']:
                    for x in range(2, len(doc)-token.i-2):
                        if (doc[token.i+x].text in ['R$', '$', '$$'] and doc[token.i+x+1].text[0].isdigit()) and doc[token.i+x].i+1 < doc[token.i+x].i+2:
                            yield doc[token.i+x].i+1, doc[token.i+x].i+2, "VALOR",
                            break
            if token.i+5 < len(doc):
                if 'valor' in token.text and doc[token.i+1].text in ['DO', 'Do', 'do'] and doc[token.i+2].text in ['CONTRATO', 'Contrato', 'contrato', 'CONTRATO:', 'Contrato:', 'contrato:']:
                    for x in range(3, len(doc)-token.i-2):
                        if (doc[token.i+x].text in ['R$', '$', '$$'] and doc[token.i+x+1].text[0].isdigit()) and doc[token.i+x].i+1 < doc[token.i+x].i+2:
                            yield doc[token.i+x].i+1, doc[token.i+x].i+2, "VALOR",
                            break

    def unidade_orc_detector_fun(self, doc):
        '''
        label function para extracao de unidade orcamentaria com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+4 < len(doc):
                for y in ['Unidade', 'UNIDADE', 'unidade']:
                    if y in token.text and doc[token.i+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:']:
                        k = 0
                        if(len(doc[token.i+2].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+3].text) <= 2):
                            k += 1
                        if(doc[token.i+2+k].text.isalpha()):
                            break
                        for x in range(2+k, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';'] and token.i+2+k < token.i+x):
                                yield token.i+2+k, token.i+x, "UNI_ORC."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "UNI_ORC."
                                break
            if token.i+3 < len(doc):
                for y in ["U.O", "UO"]:
                    if y == token.text:
                        k = 0
                        if(len(doc[token.i+1].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+2].text) <= 2):
                            k += 1
                        if(doc[token.i+1+k].text.isalpha()):
                            break
                        for x in range(1+k, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "UNI_ORC."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "UNI_ORC."
                                break

    def programa_trab_detector_fun(self, doc):
        '''
        label function para extracao de programa de trabalho com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+5 < len(doc):
                for y in ['Programa', 'PROGRAMA', 'programa']:
                    if y in token.text and doc[token.i+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:']:
                        k = 0
                        if(len(doc[token.i+3].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+4].text) <= 2):
                            k += 1
                        if(doc[token.i+3+k].text.isalpha()):
                            break
                        for x in range(3+k, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+3+k < token.i+x:
                                yield token.i+3+k, token.i+x, "PROG_TRAB."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "PROG_TRAB."
                                break
            if token.i+3 < len(doc):
                for y in ["P.T", "PT"]:
                    if y == token.text:
                        k = 0
                        if(len(doc[token.i+1].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+2].text) <= 2):
                            k += 1
                        if(doc[token.i+1+k].text.isalpha()):
                            break
                        for x in range(1+k, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "PROG_TRAB."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "PROG_TRAB."
                                break

    def natureza_desp_detector_fun(self, doc):
        '''
        label function para extracao de natureza de despesa com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+5 < len(doc):
                for y in ['Natureza', 'NATUREZA', 'natureza']:
                    if y in token.text and doc[token.i+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA', 'DAS', 'das'] and doc[token.i+2].text in ['despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:']:
                        k = 0
                        if(len(doc[token.i+3].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+4].text) <= 2):
                            k += 1
                        if(doc[token.i+3+k].text.isalpha()):
                            break
                        for x in range(3, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+3+k < token.i+x:
                                yield token.i+3+k, token.i+x, "NAT_DESP."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+3+k < token.i+x+1:
                                yield token.i+3+k, token.i+x+1, "NAT_DESP."
                                break
            if token.i+3 < len(doc):
                for y in ["N.D", "ND"]:
                    if y == token.text:
                        k = 0
                        if(len(doc[token.i+1].text) <= 2):
                            k += 1
                        if(k >= 1 and len(doc[token.i+2].text) <= 2):
                            k += 1
                        if(doc[token.i+1+k].text.isalpha()):
                            break
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "NAT_DESP."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "NAT_DESP."
                                break

    def data_detector_fun(self, doc):
        '''
        label function para extracao de data de assinatura com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+5 < len(doc):
                for y in ['DATA', 'Data', 'data', 'Da', 'DA']:
                    if y in token.text and doc[token.i+1].text in ['Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'assinatura'] and doc[token.i+2].text in ['Do', 'DO', 'do'] and doc[token.i+3].text in ['CONTRATO', 'Contrato', 'contrato', 'Contrato:', 'contrato:', 'CONVÊNIO', 'CONVENIO', 'Convênio', 'Convenio', 'convênio', 'convenio', 'Convênio:', 'Convenio:', 'convênio:', 'convenio:']:
                        k = 0
                        if(doc[token.i+4].text == ':'):
                            k += 1
                        for x in range(4, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ',', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+4+k < token.i+x:
                                yield token.i+4+k, token.i+x, "DATA_ASS."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+4+k < token.i+x+1:
                                yield token.i+4+k, token.i+x+1, "DATA_ASS."
                                break
            if token.i+4 < len(doc):
                for y in ['DATA', 'Data', 'data']:
                    if y in token.text and doc[token.i+1].text in ['de', 'da', 'De', 'Da', 'DE', 'DA'] and doc[token.i+2].text in ['Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']:
                        k = 0
                        if(doc[token.i+3].text == ':'):
                            k += 1
                        for x in range(3, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ',', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+3+k < token.i+x:
                                yield token.i+3+k, token.i+x, "DATA_ASS."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+3+k < token.i+x+1:
                                yield token.i+3+k, token.i+x+1, "DATA_ASS."
                                break
            if token.i+2 < len(doc):
                for y in ['Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']:
                    if y in token.text:
                        k = 0
                        if(doc[token.i+1].text == ':'):
                            k += 1
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ',', ';'] or (doc[token.i+x].text in ['Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "DATA_ASS."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "DATA_ASS."
                                break

    def vigencia_detector_fun(self, doc):
        '''
        label function para extracao de vigencia com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+2 < len(doc):
                for y in ['VIGÊNCIA', 'VIGENCIA', 'Vigência:', 'VIGÊNCIA:', 'VIGENCIA:', 'Vigencia:', 'Vigencia', 'Vigência', 'vigência:', 'vigencia:']:
                    if y in token.text:
                        k = 0
                        if(doc[token.i+1].text == ':'):
                            k += 1
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', '-', '–', ';']) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "VIGENCIA"
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "VIGENCIA"
                                break
            if token.i+3 < len(doc):
                for y in ['Da', 'DA']:
                    if y in token.text and doc[token.i+1].text in ['vigência', 'vigencia']:
                        k = 0
                        if(doc[token.i+2].text == ':'):
                            k += 1
                        for x in range(2, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', '-', '–', ';']) and token.i+2+k < token.i+x:
                                yield token.i+2+k, token.i+x, "VIGENCIA"
                                break
                            elif token.i+x+1 >= len(doc) and token.i+2+k < token.i+x+1:
                                yield token.i+2+k, token.i+x+1, "VIGENCIA"
                                break

    def nota_emp_detector_fun(self, doc):
        '''
        label function para extracao de nota de empenho com comparacoes de listas

        parametros:
            doc: uma string respresentando o texto de um dos contratos oferecidos no vetor da base de dados
        '''
        for token in doc:
            if token.i+2 < len(doc):
                for y in ['Empenho', 'EMPENHO', 'Empenho:', 'EMPENHO:', 'empenho:']:
                    if y in token.text:
                        k = 0
                        if((len(doc[token.i+1].text) <= 2 or doc[token.i+1].text in ['No', 'NO', 'no', 'Nº', 'nº', 'N°', 'n°', 'n', 'n.', 'n.º'])):
                            if 'R$' in doc[token.i+1].text:
                                break
                            k += 1
                        if(k >= 1 and (len(doc[token.i+2].text) <= 2 or doc[token.i+2].text in ['No', 'NO', 'no', 'Nº', 'nº', 'N°', 'n°', 'n', 'n.', 'n.º'])):
                            if 'R$' in doc[token.i+2].text:
                                break
                            k += 1
                        if(doc[token.i+1+k].text.isalpha()):
                            break
                        for x in range(1+k, len(doc)-token.i):
                            if 'R$' in doc[token.i+x].text:
                                break
                            if (doc[token.i+x].text.isalpha() or doc[token.i+x].text in ['.', ',', ';']) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "NOTA_EMP."
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "NOTA_EMP."
                                break

    def contratante_detector_fun(self, doc):
        for token in doc:
            for y in ['CONTRATANTE:', 'Contratante:', 'Contratante', 'CONTRATANTE']:
                if token.i+2 < len(doc):
                    if y == token.text and doc[token.i-1].text not in ['P/', 'Pela', 'PELA', 'pela', 'Pelo', 'PELO', 'pelo', 'de', 'da', 'De', 'Da', 'DE', 'DA']:
                        k = 0
                        if(doc[token.i+1].text == ':'):
                            k += 1
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Processo', 'PROCESSO', 'Processo:', 'PROCESSO:', 'Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "CONTRATANTE"
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "CONTRATANTE"
                                break

    def contratada_detector_fun(self, doc):
        for token in doc:
            for y in ['CONTRATADA:', 'Contratada:', 'CONTRATADA', 'Contratada']:
                if token.i+2 < len(doc):
                    if y in token.text and doc[token.i-1].text not in ['P/', 'Pela', 'PELA', 'pela', 'Pelo', 'PELO', 'pelo', 'de', 'da', 'De', 'Da', 'DE', 'DA']:
                        k = 0
                        if(doc[token.i+1].text == ':'):
                            k += 1
                        for x in range(1, len(doc)-token.i):
                            if (doc[token.i+x].text in ['.', ';'] or (doc[token.i+x].text in ['Processo', 'PROCESSO', 'Processo:', 'PROCESSO:', 'Partes', 'PARTES', 'partes:', 'Objeto', 'OBJETO', 'Valor', 'VALOR', 'Valor:', 'VALOR:', 'valor:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:', 'SIGNATÁRIOS', 'SIGNATARIOS', 'Signatários:', 'SIGNATÁRIOS:', 'SIGNATARIOS:', 'Signatarios:', 'Signatarios', 'Assinantes', 'ASSINANTES', 'Assinantes:', 'ASSINANTES:', '<>END OF BLOCK<>', 'END OF BLOCK', 'EOB']) or ((doc[token.i+x].i+1 < len(doc)) and (doc[token.i+x].text in ['Dotação', 'DOTAÇÃO', 'dotação', 'DOTACAO', 'Dotacao', 'dotacao:',  'Unidade', 'UNIDADE'] and doc[token.i+x+1].text in ['Orçamentária', 'Orcamentaria', 'ORÇAMENTÁRIA', 'ORCAMENTARIA', 'orcamentaria', 'orçamentária', 'Orçamentária:', 'Orcamentaria:', 'ORÇAMENTÁRIA:', 'ORCAMENTARIA:', 'orcamentaria:', 'orçamentária:'])) or ((doc[token.i+x].i+2 < len(doc)) and (doc[token.i+x].text in ['Programa', 'PROGRAMA', 'Natureza', 'NATUREZA', 'Data', 'DATA'] and doc[token.i+x+1].text in ['de', 'do', 'da', 'DE', 'DO', 'DA'] and doc[token.i+x+2].text in ['trabalho', 'Trabalho', 'TRABALHO', 'trabalho:', 'Trabalho:', 'TRABALHO:', 'despesa', 'Despesa', 'DESPESA', 'despesa:', 'Despesa:', 'DESPESA:', 'despesas', 'Despesas', 'DESPESAS', 'despesas:', 'Despesas:', 'DESPESAS:', 'Assinatura', 'ASSINATURA', 'assinatura:', 'Assinatura:', 'ASSINATURA:']))) and token.i+1+k < token.i+x:
                                yield token.i+1+k, token.i+x, "CONTRATADA"
                                break
                            elif token.i+x+1 >= len(doc) and token.i+1+k < token.i+x+1:
                                yield token.i+1+k, token.i+x+1, "CONTRATADA"
                                break


class SkweakContratos(LabelFunctionsContratos):
    '''
    Classe que aplica as Label Functions e realiza o processo de supervisao fraca
    Para seu funcionamento idel, eh necessario inicializa-da com um dataset de contratos

    Atributos: 
        dados = base de dados de contratos, no formato de um vetor de strings onde cada string representa um contrato
        self.df = dataframe inicial vazio para o armazenamento de entidades, texto do contrato e labels IOB
    '''

    def __init__(self, dados):
        ''' Inicializa o docs e o dataframe '''
        super().__init__(dados)
        self.df = pd.DataFrame(columns=["CONTRATO", "PROCESSO", "PARTES", "CONTRATANTE", "CONTRATADA", "OBJETO", "VALOR", "UNI_ORC.",
                                        "PROG_TRAB.", "NAT_DESP.", "NOTA_EMP.", "DATA_ASS.", "VIGENCIA", "text", "labels"])

    def apply_label_functions(self):
        '''
        Aplica as label functions na base de contratos e extrai as entidades
        '''
        doc = self.docs
        detec_contrato = skweak.heuristics.FunctionAnnotator(
            "detec_contrato", self.contrato_)
        doc = list(detec_contrato.pipe(doc))

        detec_processo = skweak.heuristics.FunctionAnnotator(
            "detec_processo", self.processo_)
        doc = list(detec_processo.pipe(doc))

        detec_data = skweak.heuristics.FunctionAnnotator(
            "detec_data", self.data_assinatura_)
        doc = list(detec_data.pipe(doc))

        detec_valor = skweak.heuristics.FunctionAnnotator(
            "detec_valor", self.valor_)
        doc = list(detec_valor.pipe(doc))

        detec_unidade = skweak.heuristics.FunctionAnnotator(
            "detec_unidade", self.unidade_orcamento_)
        doc = list(detec_unidade.pipe(doc))

        detec_programa = skweak.heuristics.FunctionAnnotator(
            "detec_programa", self.programa_trabalho_)
        doc = list(detec_programa.pipe(doc))

        detec_natureza = skweak.heuristics.FunctionAnnotator(
            "detec_natureza", self.natureza_despesa_)
        doc = list(detec_natureza.pipe(doc))

        detec_nota = skweak.heuristics.FunctionAnnotator(
            "detec_nota", self.nota_empenho_)
        doc = list(detec_nota.pipe(doc))

        contrato_detector = skweak.heuristics.FunctionAnnotator(
            "contrato_detector", self.contrato_detector_fun)
        doc = list(contrato_detector.pipe(doc))

        processo_detector = skweak.heuristics.FunctionAnnotator(
            "processo_detector", self.processo_detector_fun)
        doc = list(processo_detector.pipe(doc))

        partes_detector = skweak.heuristics.FunctionAnnotator(
            "partes_detector", self.partes_detector_fun)
        doc = list(partes_detector.pipe(doc))

        objeto_detector = skweak.heuristics.FunctionAnnotator(
            "objeto_detector", self.objeto_detector_fun)
        doc = list(objeto_detector.pipe(doc))

        valor_detector = skweak.heuristics.FunctionAnnotator(
            "valor_detector", self.valor_detector_fun)
        doc = list(valor_detector.pipe(doc))

        unidade_orc_detector = skweak.heuristics.FunctionAnnotator(
            "unidade_orc_detector", self.unidade_orc_detector_fun)
        doc = list(unidade_orc_detector.pipe(doc))

        programa_trab_detector = skweak.heuristics.FunctionAnnotator(
            "programa_trab_detector", self.programa_trab_detector_fun)
        doc = list(programa_trab_detector.pipe(doc))

        natureza_desp_detector = skweak.heuristics.FunctionAnnotator(
            "natureza_desp_detector", self.natureza_desp_detector_fun)
        doc = list(natureza_desp_detector.pipe(doc))

        data_detector = skweak.heuristics.FunctionAnnotator(
            "data_detector", self.data_detector_fun)
        doc = list(data_detector.pipe(doc))

        vigencia_detector = skweak.heuristics.FunctionAnnotator(
            "vigencia_detector", self.vigencia_detector_fun)
        doc = list(vigencia_detector.pipe(doc))

        nota_emp_detector = skweak.heuristics.FunctionAnnotator(
            "nota_emp_detector", self.nota_emp_detector_fun)
        doc = list(nota_emp_detector.pipe(doc))

        contratante_detector = skweak.heuristics.FunctionAnnotator(
            "contratante_detector", self.contratante_detector_fun)
        doc = list(contratante_detector.pipe(doc))

        contratada_detector = skweak.heuristics.FunctionAnnotator(
            "contratada_detector", self.contratada_detector_fun)
        doc = list(contratada_detector.pipe(doc))

        self.docs = doc

    def train_HMM_Dodf(self):
        '''
        treina o modelo HMM para refinar e agregar a entidades extraidas pelas label functions
        '''
        model = skweak.aggregation.HMM("hmm", ["CONTRATO", "PROCESSO", "PARTES", "CONTRATANTE", "CONTRATADA", "OBJETO", "VALOR", "UNI_ORC.", "PROG_TRAB.",
                                               "NAT_DESP.", "NOTA_EMP.", "DATA_ASS.",  "VIGENCIA"], sequence_labelling=True)

        self.docs = model.fit_and_aggregate(self.docs)

        for doc in self.docs:
            if "hmm" in doc.spans:
                doc.ents = doc.spans["hmm"]
            else:
                doc.ents = []

        ''' Salvando modelo HMM em uma pasta data '''
        if os.path.isdir("./data"):
            skweak.utils.docbin_writer(self.docs, "./data/reuters_small.spacy")
        else:
            os.mkdir("./data")
            skweak.utils.docbin_writer(self.docs, "./data/reuters_small.spacy")

    def get_IOB(self):
        '''
        retorna os resultados das entidades extraidas em IOB
        '''
        nlp = spacy.blank("pt")
        doc_bin = DocBin().from_disk("./data/reuters_small.spacy")
        examples = []

        for doc in doc_bin.get_docs(nlp.vocab):
            lista_iob = []
            for i in range(0, len(doc)):
                label_iob = ""
                _txt_ = doc[i].text
                _label_ = doc[i].ent_iob_
                _ent_ = doc[i].ent_type_
                if _txt_ not in ["", " ", "  ", "   "]:
                    if(_label_ != "O"):
                        label_iob += f'{_txt_} {_label_}-{_ent_}'
                    else:
                        label_iob += f'{_txt_} {_label_}'
                    lista_iob.append(label_iob)
            examples.append(lista_iob)

        return examples

    def list_spans_specific(self, x):
        '''
        Mostra os spans HMM (entidades finais resultantes da aplicacao do HMM ) de um doc da base de dados especifico

        parametros:
            x: inteiro representano a posicao do doc no vetor de contratos da base de dados
        '''
        print(self.docs[x].spans["hmm"])

    def list_spans_all(self):
        '''
        Mostra os spans HMM (entidades finais resultantes da aplicacao do HMM ) de toda a base de dados
        '''
        for doc in self.docs:
            print(doc.spans["hmm"])

    # Retorna o dataframe com todas as entidades, textos e IOB para cada documento
    def get_hmm_dataframe(self):
        '''
        Retorna o dataframe final com todas as entidades, textos e labels-IOB para cada documento da base de dados
        '''
        nlp = spacy.blank("pt")
        doc_bin = DocBin().from_disk("./data/reuters_small.spacy")

        for doc in doc_bin.get_docs(nlp.vocab):
            aux = {"CONTRATO": "", "PROCESSO": "", "PARTES": "", "CONTRATANTE": "", "CONTRATADA": "", "OBJETO": "", "VALOR": "", "UNI_ORC.": "", "PROG_TRAB.": "",
                   "NAT_DESP.": "", "NOTA_EMP.": "", "DATA_ASS.": "", "VIGENCIA": "", "text": "", "labels": ""}

            for entity in doc.ents:
                aux[entity[0].ent_type_] = entity.text

            for token in doc:
                aux["text"] += token.text + ' '

            for i in range(0, len(doc)):
                _txt_ = doc[i].text
                _label_ = doc[i].ent_iob_
                _ent_ = doc[i].ent_type_
                if _txt_ not in ["", " ", "  ", "   "]:
                    if(_label_ != "O"):
                        aux["labels"] += f'{_label_}-{_ent_} '
                    else:
                        aux["labels"] += f'{_label_} '

            self.df = self.df.append(aux, ignore_index=True)

        return self.df

    def save_dataframe_csv(self, name):
        '''
        Salva o dataframe em um .csv

        parametros:
            name: string representado o nome com o qual deseja salvar o dataframe
        '''
        nome = str(name)+".csv"
        self.df.to_csv(nome)
