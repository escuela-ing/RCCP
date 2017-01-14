# -*- coding: utf-8 -*-
"""
Created on Tue Nov 1 09:59:39 2016

@author: Juan Sebastian Martinez Serna,
         Diana Maria del Pilar Socha Diaz
"""

import pandas as pd
import ast

# s = "ferdand\\u00E9"
# prind s.decode('unicode-escape')
# >>> fernandé

def deleteTag(s):
    '''
    Delete the first HTML tag of the string,
    all tags starts with '<' and ends with '>'

    PARAMETERS
    ----------
    s : STRING
        string to delete the first HTML tag

    RETURNS
    -------
    str : string without the first HTML tag
    None: if 's' no contains a HTML tag

    EXAMPLES
    --------
    in["Hello<tag>world"]          -> out["Hello world"]
    in["Hello <tag> again <tag2>"] -> out["Hello  again <tag2>"]
    in["Hello without HTML tags"]  -> out[None]
    '''
    startsTag = s.find('<'); endsTag = s.find('>')
    if startsTag == -1 or endsTag == -1: return None
    elif len(s) == endsTag: return s[:startsTag]
    else: return s[:startsTag] + ' ' + s[endsTag+1:]

def deleteHTMLTags(s):
    '''
    Delete all HTML tags

    PARAMETERS
    ----------
    s : STRING
        string to delete all HTML tags

    RETURNS
    -------
    str : string without HTML tags

    EXAMPLES
    --------
    in["Hello<tag>world"]          -> out["Hello world"]
    in["Hello <tag> again <tag2>"] -> out["Hello   again"]
    in["Hello without HTML tags"]  -> out["Hello without HTML tags"]
    '''
    ok = True
    while ok:
        aux = deleteTag(s)
        if aux is None: ok = False
        else: s = aux

    return s.strip()


def changeCodeToSpace(s):
    '''
    Change all HTML codes '&nbsp;' for a single space ' ', if the string has no
    a code, do nothing, i.e. returns the same string

    PARAMETERS
    ----------
    s : STRING
        string to delete all HTML codes '&nbsp;'

    RETURNS
    -------
    str : string without HTML codes '&nbsp;'

    EXAMPLES
    --------
    in["Hello&nbsp;world"]          -> out["Hello world"]
    in["Hello &nbsp; again &nbsp;"] -> out["Hello   again"]
    in["Hello without HTML codes"]  -> out["Hello without HTML codes"]
    '''
    spaceCode = '&nbsp;'
    startCode = s.find(spaceCode)

    while startCode != -1:
        s = s[:startCode] + ' ' + s[startCode+6:]
        startCode = s.find(spaceCode)

    return s.strip()


def findCode(s):
    '''
    Find and return the first code of manuscripts.
    CODE Struct -> B#[A-Z]###

    PARAMETERS
    ----------
    s : STRING
        string to find code

    RETURNS
    -------
    str : string with the first code

    EXAMPLES
    --------
    in["Hello B2C59 world"]        -> out["B2C59"]
    in["Hello B5N100 again B8U31"] -> out["B5N100"]
    in["Hello without codes"]      -> out[""]

    '''
    startCode = 'B'
    code = ''
    startIndexCode = s.find(startCode)

    if startIndexCode == -1: return code # If 'B' not exist
    if  s[startIndexCode+1].isdigit(): # Verify B#
        if s[startIndexCode+2].isalpha() and s[startIndexCode+3].isdigit(): # Verify B#[A-Z]#
            code = s[startIndexCode:startIndexCode+4]
            if len(s) > startIndexCode+4 and s[startIndexCode+4].isdigit(): # Verify B#[A-Z]##
                code = s[startIndexCode:startIndexCode+5]
                if len(s) > startIndexCode+5 and s[startIndexCode+5].isdigit(): # Verify B#[A-Z]###
                    code = s[startIndexCode:startIndexCode+6]
    else:
        code = findCode(s[startIndexCode + 1:])

    return code.strip()


def deleteDoubleSpace(s):
    '''
    Delete all double space from the string 's' and put a single space

    PARAMETERS
    ----------
    s : STRING
        string to delete all double space

    RETURNS
    -------
    str : string without any double space

    EXAMPLES
    --------
    in["Hello world"]                -> out["Hello world"]
    in["Hello   again "]             -> out["Hello again"]
    in["Hello without double space"] -> out["Hello without double space"]
    '''
    while s.find('  ') != -1: s = s.replace('  ', ' ')
    return s.strip()


def deleteNegativeSymbol(s):
    '''
    Find and remove all negative symbol with or without a space

    PARAMETERS
    ----------
    s : STRING
        string to delete all negative symbol with or without a space

    RETURNS
    -------
    str : string without any negative symbol

    EXAMPLES
    --------
    in["Hello- world"]                  -> out["Helloworld"]
    in["Hello-again "]                  -> out["Helloagain"]
    in["Hello without negative symbol"] -> out["Hello without negative symbol"]
    '''
    return s.replace('- ', '').replace('-', '').replace('_','').strip()


def extractTranscriptions(s, transcriptions=[]):
    '''
    Build a list of tuples with 2 items by touple from string 's', the first
    item is the code of transcription and the second item is the transcription

    PARAMETERS
    ----------
    s : STRING
        string that contains the transcriptions and its codes
    transcriptions : LIST of TUPLES
        have a tuple with two elements, the first is the code, and the second
        is the transcription

    RETURNS
    -------
    l : a list that contains the transcriptions with its codes

    EXAMPLES
    --------
    in["asd B3C4 asdoaijfia"]    -> out[[('B3C4', 'asdoaijfia')]]
    in["B3F5 asfsdf B2U3 sadsd"] -> out[[('B3F5','asdsdf'), ('B2U3','sadfd')]]
    in["String without a code"]  -> out[[]]
    '''
    code = findCode(s)

    if code != '':
        indexCode = s.find(code)
        s = s[indexCode+len(code):].strip() # new s without code
        code2 = findCode(s)

        if code2 != '':
            indexCode2 = s.find(code2)
            aux = s[:indexCode2]
            transcriptions.append((code, aux.strip()))
            s = s[indexCode2:] # new s without previous msnuscript
        else:
            transcriptions.append((code, s.strip()))
    else:
        return transcriptions

    return extractTranscriptions(s, transcriptions)


def loadExcel(path, sheetname='Culled Data'):
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


def loadCSV(path):
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
    cvs = pd.read_csv(path, encoding='utf-8')
    return pd.DataFrame(cvs)


def saveCSV(df, path, name='Transcriptions.csv'):
    '''
    Create a CSV file with the transcriptions and its codes

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


def createDataFrame(l, colCode='Codes', colTranscriptions='Transcriptions'):
    '''
    Create a DataFrame from a list of tuples that contains the transcription
    with its respective code

    PARAMETERS
    ----------
    l : LIST of TUPLES
        contains the transcription with its respective code
    colCode : STRING
        column name for codes
    colTranscriptions : STRING
        column name for transcriptions

    RETURNS
    -------
    df : DataFrame
        The respective DataFrame with names and values by column
    '''
    columnCodes = []
    columnTrans = []

    for (cod, trans) in l:
        columnCodes.append(cod)
        columnTrans.append(trans)

    df = pd.DataFrame()
    df[colCode] = columnCodes
    df[colTranscriptions] = columnTrans

    return df


def deleteTabs(s):
    '''
    Delete all tabs from the string and replaced by a single space

    PARAMETERS
    ----------
    s : STRING
        the string to remove all tabs

    RETURNS
    -------
    s : STRING
        the string without any tab

    EXAMPLES
    --------
    in['Hello\t\tWorld\t']    -> out['Hello  World']
    in['\tHello \t\ŧ\tWorld'] -> out['Hello    world']
    in['Hello again']         -> out['Hello again']
    '''
    return s.replace('\t', ' ')


def dataClean(s, e=[]):
    '''
    Clean the string, i.e. Remove HTML codes, double space and negative symbols
    and delete all elements indicates

    PARAMETERS
    ----------
    s : STRING
        string without clean
    e : LIST
        list of elements to remove of the string

    RETURNS
    -------
    s : STRING
        a clean string

    EXAMPLES
    --------
    in["Hola <asd> wo- rld"]                        -> out["Hola world"]
    in["Heloo&nbsp;my&nbsp;<ds>&nbsp; <sfe> world"] -> out["Heloo my world"]
    in["Hello again again"]                         -> out["Hello again again"]
    '''
    for rmv in e: s.replace(rmv, ' ')

    s = deleteTabs(s)
    s = changeCodeToSpace(s)
    s = deleteDoubleSpace(s)
    s = deleteNegativeSymbol(s)
    s = deleteHTMLTags(s)
    if s.find('  ') != -1 : s = deleteDoubleSpace(s)

    return s

#==============================================================================

def main():

    pathLoad  = input('Excel file : ')
    sheetName = input('Sheet name : ')
    colName   = input('Column name to work : ')
    pathSave  = input('Path to save work files : ')
    path2Del  = input('Path to text file to remove elements: ')

    if sheetName == '': xls = loadExcel(pathLoad)
    else: xls = loadExcel(pathLoad, sheetName)

    li = list(xls[colName])
    t = []

    listFailed = []

    with open(path2Del, 'r') as f:

        elements2del = f.readlines()

        for s in li:
            try:
                s = str(s).replace('"', '')
                s = ast.literal_eval('"' + s + '"')
                aux = extractTranscriptions(dataClean(s, elements2del))
                t += [e for e in aux if e not in t]
            except:
                listFailed.append(s)

    df = createDataFrame(t)
    saveCSV(df, pathSave)

    if len(listFailed) != 0: saveCSV(pd.DataFrame(listFailed), pathSave, 'Failed.csv')

#==============================================================================
# def mainTest():
# 
#     pathLoad  = '~/Proyectos/RCCP/Documents/Data/DS-Plasencia2014-Transcriptions.xlsx'
#     colName   = 'Transriptions'
#     pathSave  = '~/Proyectos/RCCP/Documents/Data/'
#     path2Del  = '/home/JuanSe/Proyectos/RCCP/Documents/Data/toDelete.rccp'
# 
# 
#     xls = loadExcel(pathLoad)
# 
#     li = list(xls[colName])
#     t = []
# 
#     listFailed = []
# 
#     with open(path2Del, 'r') as f:
# 
#         elements2del = f.readlines()
# 
#         for s in li:
#             try:
#                 s = str(s).replace('"', '')
#                 s = ast.literal_eval('"' + s + '"')
#                 aux = extractTranscriptions(dataClean(s, elements2del))
#                 t += [e for e in aux if e not in t]
#             except:
#                 listFailed.append(s)
# 
#     df = createDataFrame(t)
#     saveCSV(df, pathSave)
# 
#     if len(listFailed) != 0: saveCSV(pd.DataFrame(listFailed), pathSave, 'Failed.csv')
#==============================================================================


main()

