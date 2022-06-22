import numpy as np
import os
import glob
import pandas as pd

def Dist2Curv(param):
    curv = np.empty(len(param),dtype=float)
    L = 0.15 #en metros
    param = np.array(param)
    p2 = np.power(param*1e-3, 2)    #llevar d de um a m
    #curv = (2 * param * 1e-6) / (p2 + L * L)
    curv = np.around(2 * param*1e-3/(p2+L*L), 3)
    #
    return curv #curv en 1/m

def CreateTxDataFrame(filepath,dfEDFA, dfParam):
    xEDFA = dfEDFA["xEDFA"].tolist()
    yEDFA = dfEDFA["yEDFA"].tolist()
    xASE = DownSample(xEDFA, 5)
    xRange = [min(xASE), max(xASE)]
    yASE = DownSample(yEDFA, 5)
    files = dfParam["fileName"].tolist()
    param = dfParam["param"].tolist()
    paramStr = []
    os.chdir(filepath)
    filesCSV = glob.glob('*.CSV')
    for i in range(len(param)): # NOF files cycle
        sufix = "0" + str(files[i]) + ".CSV"
        fileName = [this for this in filesCSV if this.startswith("W") and this.endswith(sufix)]
        var=fileName[0]
        paramStr.append(str(param[i]))
        df = pd.read_csv(fileName[0], header=22, names=["Wavelength", paramStr[i]])  # create dataframe
        yi = df[(df['Wavelength'] >= xRange[0]) & (df['Wavelength'] <= xRange[1])][paramStr[i]].tolist()
        if i == 0:
            x0 = df[(df['Wavelength'] >= xRange[0]) & (df['Wavelength'] <= xRange[1])]['Wavelength'].tolist()
            df1 = pd.DataFrame(list(zip(x0, yi-yASE)), columns=['Wavelength', paramStr[i]])
        else:
            df1[paramStr[i]] = yi-yASE
    return df1

def DownSample(x,m):
    xDown = []
    i = 0
    while i <= len(x):
        if (i % m )==0:
             xDown.append(x[i])
        i = i+1
    xDown = np.array(xDown)
    return(xDown)