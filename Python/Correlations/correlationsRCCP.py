#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 09 21:02:37 2017

@author: Diana Maria del Pilar Socha Diaz
         Juan Sebastian Martinez Serna
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def loadExcel(path, sheetname='Transcriptions'):
    '''
    Load a Excel file
    PARAMETERS
    ----------
    path: STRING
        string with the Excel path to load
    sheetname: STRING
        the sheetname to load
    RETURNS
    -------
    xl : DataFrame
        A DataFrame that contains all values from excel file
    '''
    xl = pd.ExcelFile(path).parse(sheetname=sheetname)
    return pd.DataFrame(xl)

def saveCSV(df, path, name='Correlations.csv'):
    '''
    Create a CSV file with the Correlations

    PARAMETERS
    ----------
    df : DataFrame
        contains the transcriptions with its codes to save
    path : STRING
        the path where to save the file
    name : STRING
        the file name
    '''
    df.to_csv(path + name)

def main():

    pathLoad  = input('Excel file : ')
    sheetName = input('Sheet name : ')
    dict1     = input('Dictionary 1 : ')
    dict2     = input('Dictionary 2 : ')
    colName   = input('Column name : ')
    pathSave  = input('CSV to save : ')

    trans = loadExcel(pathLoad, sheetName)

    with open(dict1, 'r', encoding='latin-1') as d1:
        with open(dict2, 'r', encoding='latin-1') as d2:
            ld1 = d1.readlines()
            ld2 = d2.readlines()

            correlations = {}

            transVal = trans[colName]
            for e in transVal.iteritems():
                s = str(e[1])
                for ed1 in ld1:
                    if s.find(ed1) != -1:
                        for ed2 in ld2:
                            try: correlations[ed1][ed2] += s.count(ed2)
                            except:
                                try:correlations[ed1][ed2] = 0
                                except:correlations[ed1] = {ed2 : 0}

            valores = []

            for d1 in dict1:
                row = []
                for d2 in dict2:
                    try: row.append(correlations[d1][d2])
                    except: True
                valores.append(row)

            df = pd.DataFrame(data=valores, columns=dict1, index=dict2)
            saveCSV(df, pathSave)
            print('OK')

main()
