# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:18:28 2022

@author: angel
"""
#%%
### Download necessary libraries
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import datetime 
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests

path = r"C:\Users\angel\Final--crypto\data"

def loadData(path):
    #cryptoPrices = pd.read_excel(path + '\CommonAssetClassesPrices.xlsx')
    equityPrices = pd.read_excel(path + '\Equities.xlsx')
    bondPrices = pd.read_excel(path + '\Bonds.xlsx')
    cmdtyPrices = pd.read_excel(path + '\Commodities.xlsx')
    vixPrices = pd.read_excel(path + '\VIX.xlsx')
    cryptoPrices = pd.read_excel(path + '\crypto-prices.xlsx')
    cryptoPrices['Dates'] = pd.to_datetime(cryptoPrices['Dates'])
    
    cryptoPrices.columns = ['Dates', 'BTC', 'ETH', 'XRP', 'XLM']
    
    
    return equityPrices, bondPrices, cmdtyPrices, vixPrices, cryptoPrices

def getStartEnd(*data):
    minDate = datetime.datetime.strptime("30/11/0001","%d/%m/%Y")
    maxDate = datetime.datetime.strptime("30/11/3000","%d/%m/%Y")
    for d in data: 
        end = d['Dates'].iat[-1]
        start = d['Dates'][0]
        
        if end<maxDate:
            maxDate = end
            
        if start>minDate:
            minDate = start
            
    return minDate, maxDate
    
            
def makeDataUniformLength(start, end, assetList, *data):
    cnt = 0
    #aggData = []
    aggData = {}
    for d in data:
        d = d[(d['Dates']>=start)&(d['Dates']<=end)]
        #aggData.append([d])
        aggData[assetList[cnt]] = d
        cnt+=1
    
    return aggData

def mergeDataFrames(dictDf, assetList):
    merged = dictDf[assetList[0]]
    
    for i in range(len(assetList)):
        if i == len(assetList)-1:
            break
        merged = pd.merge(merged, dictDf[assetList[i+1]], on = ['Dates'])

    return merged 

def getBusinessDaysOnly(df):
    isBusinessDay = BDay().onOffset
    #isBusinessDay = BDay().is_on_offset()
    match_series = pd.to_datetime(df['Dates']).map(isBusinessDay)
    return df[match_series]

def calcDailyReturn(price):
    return price.pct_change(1)

def getCorr(df1,df2):
    corr, _ = pearsonr(df1, df2)
    return corr

def plotHeatMap(df):
    lab = df.columns[1:]
    fig, ax = plt.subplots()
    im = ax.imshow(df)
    
    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(lab)), labels=lab)
    ax.set_yticks(np.arange(len(lab)), labels=lab)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(lab)):
        for j in range(len(lab)):
            text = ax.text(j, i, df[i, j],
                           ha="center", va="center", color="w")
    
    ax.set_title("Correlation heatmap")
    fig.tight_layout()
    plt.show()
    
def smoothValues(df,windowLength):
    return df.rolling(window = windowLength).mean().iloc[windowLength:,:]
#%%
assetNamesList = ['equity', 'bond', 'commodity', 'vix', 'crypto']
equity, bond, cmdty, vix, crypto = loadData(path) 
start, end = getStartEnd(equity, bond, cmdty, vix, crypto)
allData = makeDataUniformLength(start, end, assetNamesList, equity, bond, cmdty, vix, crypto)
mergedData = mergeDataFrames(allData, assetNamesList)

dailyRets = {}
for a in assetNamesList:
    dailyRets[a] = calcDailyReturn(allData[a].iloc[:,1:])

mergedDailyRets = calcDailyReturn(mergedData.iloc[:,1:])
mergedDailyRets.index = mergedData.Dates

corrMat = mergedDailyRets.corr()

smoothedDailyRets = smoothValues(mergedDailyRets, 7)
smoothedDailyRets.plot()
