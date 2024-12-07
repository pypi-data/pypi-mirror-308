# Copyright 2023-2025 Jeongmin Kang, jarvisNim @ GitHub
# See LICENSE for details.
'''
Prgram 명: pyminerva.indices.py
Author: jeongmin Kang
Mail: jarvisNim@gmail.com
목적: 세계 경제지표들을 조회하는 함수들의 모임
History
- 20241115 create
'''

import sys, os, time
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import urllib

from bs4 import BeautifulSoup
from .utils import constant as cst
from . import base


'''
0. 공통영역 설정
'''
reports_dir = os.getcwd() + '/batch/reports'


#####################################
# funtions
#####################################
'''
1. Containerized Freight Index
- 해상운임지수: 경기가 다시 활성화 되는지 여부 모니터링 (20220906)
'''

def get_container_Freight_index():
    # CCFI (China Containerized Freight Index)
    # 중국컨테이너운임지수는 중국 교통부가 주관하고 상하이 항운교역소가 집계하는 중국발 컨테이너운임지수로 1998년 4월 13일 처음 공시되었다. 
    # 세계컨테이너시황을 객관적으로 반영한 지수이자 중국 해운시황을 나타내는 주요 지수로 평가받고 있다.
    # 1998년 1월 1일을 1,000으로 산정하며 중국의 항구를 기준으로 11개의 주요 루트별 운임을 산정하며, 16개 선사의 운임정보를 기준으로 
    # 매주 금요일에 발표를 하고 있다.
    page = requests.get("https://www.kcla.kr/web/inc/html/4-1_2.asp")
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find_all('table')
    df_ccfi = pd.read_html(str(table))[0]

    df_ccfi = df_ccfi.T
    df_ccfi.drop([0], inplace=True)
    df_ccfi[1] = df_ccfi[1].astype('float')
    df_ccfi.rename(columns={0:'Date', 1:'Idx'}, inplace=True)
    df_ccfi['Date']= pd.to_datetime(df_ccfi['Date'])
    df_ccfi.set_index('Date', inplace=True)

    # SCFI (Shanghai Containerized Freight Index)
    # 상하이컨테이너 운임지수는 상하이거래소(Shanghai Shipping Exchange: SSE)에서 2005년 12월 7일부터 상하이 수출컨테이너 운송시장의 
    # 15개 항로의 스팟(spot) 운임을 반영한 운임지수이다. 기존에는 정기용선운임을 기준으로 하였으나 2009년 10월 16일부터는 20ft 컨테이너(TEU)당 
    # 미달러(USD)의 컨테이너 해상화물운임에 기초하여 산정하고 있다.
    # 운송조건은 CY-CY조건이며 컨테이너의 타입과 화물의 상세는 General Dry Cargo Container로 한정짓고 있고, 개별항로의 운임율은 각 항로의 
    # 모든 운임율의 산술평균이며 해상운송에 기인한 할증 수수료가 포함되어 있다. 운임정보는 정기선 선사와 포워더를 포함한 CCFI의 패널리스트들에게 
    # 제공받고 있다.
    page = requests.get("https://www.kcla.kr/web/inc/html/4-1_3.asp")
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find_all('table')
    df_scfi = pd.read_html(str(table))[0]

    df_scfi = df_scfi.T
    df_scfi.drop([0], inplace=True)
    df_scfi[1] = df_scfi[1].astype('float')
    df_scfi.rename(columns={0:'Date', 1:'Idx'}, inplace=True)
    df_scfi['Date']= pd.to_datetime(df_scfi['Date'])
    df_scfi.set_index('Date', inplace=True)

    # HRCI (Howe Robinson Container Index)
    # 영국의 대표적인 해운컨설팅 및 브로커社인 Howe Robinson社가 발표하는 컨테이너 지수로서 선박을 하루 용선하는 데 소요되는 비용에 대한
    # 컨테이너 시장 용선요율을 나타내고 있다. 이 회사는 1883년 설립되었으며 컨테이너선과 벌크선에 대한 세계에서 가장 크고 독립적인 중개회사 중 
    # 하나로 1997년 1월 1일을 1,000으로 놓고 매주 발표하고 있다.
    page = requests.get("https://www.kcla.kr/web/inc/html/4-1_4.asp")
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find_all('table')
    df_hrci = pd.read_html(str(table))[0]

    df_hrci = df_hrci.T
    df_hrci.drop([0], inplace=True)
    df_hrci[1] = df_hrci[1].astype('float')
    df_hrci.rename(columns={0:'Date', 1:'Idx'}, inplace=True)
    df_hrci['Date']= pd.to_datetime(df_hrci['Date'])
    df_hrci.set_index('Date', inplace=True)


    # BDI (Baltic Dry Index)
    # 발틱운임지수는 발틱해운거래소에서 1999년 11월 1일부터 사용되었으며 1985년부터 건화물(dry cargo)의 운임지수로 사용이 되어온 
    # BFI(Baltic Freight Index)를 대체한 종합운임지수로 1985년 1월 4일을 1,000으로 산정하여 선박의 형태에 따라 발표하고 있다.
    # 선형에 따라 Baltic Capesize Index(BCI), Baltic Panamax Index(BPI), Baltic Supramax Index(BSI), 
    # Baltic Handysize Index(BHSI) 등으로 구성되어 있으며, BDI는 이러한 선형별 정기용선의 4가지 지수를 동일한 가중으로 평균을 산출한 다음 
    # BDI factor를 곱하여 산출하고 있다.
    page = requests.get("https://www.kcla.kr/web/inc/html/4-1_5.asp")
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find_all('table')
    df_bdi = pd.read_html(str(table))[0]

    df_bdi = df_bdi.T
    df_bdi.drop([0], inplace=True)
    df_bdi[1] = df_bdi[1].astype('float')
    df_bdi.rename(columns={0:'Date', 1:'Idx'}, inplace=True)
    df_bdi['Date']= pd.to_datetime(df_bdi['Date'])
    df_bdi.set_index('Date', inplace=True)

    plt.figure(figsize=(15,5))
    plt.title(f"Containerized Freight Index", fontdict={'fontsize':20, 'color':'g'})
    plt.grid()
    plt.plot(df_ccfi, label='China Containerized Freight Index') 
    plt.plot(df_scfi, label='Shanghai Containerized Freight Index') 
    plt.plot(df_hrci, label='Howe Robinson Container Index]')
    plt.plot(df_bdi, label='Baltic Dry Index') 
    plt.legend()
    plt.savefig(reports_dir + '/indices_container_freight_index.png')

    return df_ccfi, df_scfi, df_hrci, df_bdi