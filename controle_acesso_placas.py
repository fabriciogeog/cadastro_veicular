#!/usr/bin/python3

"""Controle de acesso veicular com OpenCV."""
#  Importações

import cv2
import numpy as np
import pandas as pd
import pytesseract
import re
from datetime import datetime


# Funções


def consulta_placas(leitura):
    """Realiza a leitura da placa."""
    tabela = pd.read_excel("veiculos_cadastrados.xls")
    busca = tabela.loc[tabela["PLACA"] == leitura]
    if busca.empty:
        pass
    else:
        return busca


def foto_placa(placa_cinza, placa_lida):
    """Registra a foto da placa."""
    foto = np.array(placa_cinza)
    data = str(datetime.today())
    caminho = f"fotos_placas/{placa_lida}{data}" + ".jpg"
    cv2.imwrite(caminho, foto)


def registro_placas(resultado):
    """Tabula os dados da placa."""
    resultado.to_csv(
        "arquivos_csv/registro_placas.csv", mode="a", sep=";", header=False, index=False
    )


def leitura_box(placa_cinza):
    """Processamento e leitura da imagem/placa."""
    caixas = pytesseract.image_to_data(placa_cinza)
    for x, caixa in enumerate(caixas.splitlines()):
        if x != 0:
            caixa = caixa.split()
            if len(caixa) == 12:
                x, y, l, a = (
                    int(caixa[6]),
                    int(caixa[7]),
                    int(caixa[8]),
                    int(caixa[9]),
                )
                placa_lida = str(caixa[11])
                placa_lida = placa_lida.replace("-", "")
                padrao = r"[A-Z]{3}[0-9]{1}[A-Z0-9]{1}[0-9]{2}$"
                match = re.fullmatch(padrao, placa_lida)
                if not match:
                    pass
                else:
                    return placa_lida


def inicia_camera(url):
    """Ativação d câmera. Recebe URL como parâmetro."""
    captura = cv2.VideoCapture(url)
    while True:
        conectado, quadros = captura.read()
        placa_cinza = cv2.cvtColor(quadros, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Controle de Acesso", placa_cinza)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    return placa_cinza
    captura.release()
    cv2.destroyAllWindows()


def aplica_texto(placa_cinza, placa_lida):
    """Aplica texto aos frames exibidos."""
    cv2.putText(
        placa_cinza,
        "Controle de Acesso",
        (50, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 255, 255),
        1,
    )
    cv2.putText(
        placa_cinza,
        placa_lida,
        (450, 100),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 255, 0),
        1,
    )


if __name__ == "__main__":

    captura = cv2.VideoCapture(0)
    while True:
        conectado, quadros = captura.read()
        placa_cinza = cv2.cvtColor(quadros, cv2.COLOR_BGR2GRAY)
        placa_lida = leitura_box(placa_cinza)
        pesquisa = consulta_placas(placa_lida)
        aplica_texto(placa_cinza, placa_lida)
        print(pesquisa)
        cv2.imshow("Controle de Acesso", placa_cinza)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    captura.release()
    cv2.destroyAllWindows()
