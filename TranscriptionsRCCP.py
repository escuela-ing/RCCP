# -*- coding: utf-8 -*-
"""
Created on Tue Nov 1 09:59:39 2016

@author: Juan Sebastian Martinez Serna,
         Diana Maria del Pilar Socha Diaz
"""

import pandas as pd

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
    in["Hello<tag>word"]           -> out["Hello word"]
    in["Hello <tag> again <tag2>"] -> out["Hello  again <tag2>"]
    in["Hello without HTML tags"]  -> out[None]
    '''
    startsTag = s.find('<'); endsTag = s.find('>')
    if startsTag == -1 or endsTag == -1: return None
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
    in["Hello<tag>word"]           -> out["Hello word"]
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
    in["Hello&nbsp;word"]           -> out["Hello word"]
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
    in["Hello B2C59 word"]         -> out["B2C59"]
    in["Hello B5N100 again B8U31"] -> out["B5N100"]
    in["Hello without codes"]      -> out[""]
    
    '''
    startCode = 'B'
    code = ''
    startIndexCode = s.find(startCode)
    
    if startIndexCode == -1: return code # If 'B' not exist
    # Verify B#[A-Z]#
    if  s[startIndexCode+1].isdigit() and s[startIndexCode+2].isalpha() and s[startIndexCode+3].isdigit():
        code = s[startIndexCode:startIndexCode+4]
        if s[startIndexCode+4].isdigit(): # Verify B#[A-Z]##
            code = s[startIndexCode:startIndexCode+5]
            if s[startIndexCode+5].isdigit(): # Verify B#[A-Z]###
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
    in["Hello word"]                 -> out["Hello word"]
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
    in["Hello- word"]                   -> out["Helloword"]
    in["Hello-again "]                  -> out["Helloagain"]
    in["Hello without negative symbol"] -> out["Hello without negative symbol"]
    '''
    s = s.replace('- ', ''); s = s.replace('-', '')
    return s.strip()
    
def extractManuscript(s, manuscript={}):
    '''
    Build a dictionary from string 's', the keys of dictionary 'manuscript' are
    the codes of manuscripts and the values are the transcriptions
    
    PARAMETERS
    ----------
    s : STRING
        string that contains the transcriptions and its codes
    manuscript : DICTIONARY
        KEYS are the transcriptions codes as string
        VALUES are the transcriptions as string
        
    RETURNS
    -------
    Dictionary : a dictionary that contains the transcriptions with its codes
    
    EXAMPLES
    --------
    in["asd B3C4 asdoaijfia"]       -> out[{"B3C4":"asdoaijfia"}]
    in["B3F56 asfsdf B2U34 sadsd"]  -> out[{"B3F56":"asdsdf", "B2U34":"sadfd"}]
    in["String without a code"]     -> out[{}]
    '''
    code = findCode(s)
    
    if code != '':
        indexCode = s.find(code)
        s = s[indexCode+len(code):].strip() # new s without code
        code2 = findCode(s)
        
        if code2 != '':
            indexCode2 = s.find(code2)
            aux = s[:indexCode2]
            manuscript[code] = aux
            s = s[indexCode2:] # new s without previous msnuscript
        else:
            manuscript[code] = s.strip()
    else:
        return manuscript
    
    return extractManuscript(s, manuscript)

def printManuscript(s):
    '''
    '''
    for k,v in s.items(): print('CODE: ' + k + '\nMANUSCRIPT:\n' + v, end='\n\n')

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

def createDataFrame(d, colCode='Codes', colTranscriptions='Transcriptions'):
    '''
    Create a DataFrame from a Dictionary of transcriptions
    
    PARAMETERS
    ----------
    d : DICTIONARY
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
    df = pd.DataFrame()
    df[colCode] = list(m.keys())
    df[colTranscriptions] = list(m.values())
    return df

    
    

#########
# STUBS #
#########

stubString1 = u'''
Group 3<br>Manuscript Image B2U37<br>rentas                  que sea contador a Dn Alfonso<br>
Garcia, Arcediano de Troxillo que esta-<br>ba presente; los quales sobredichos
y&nbsp;<br>cada uno dellos que estaban presentes&nbsp;<br>otorgaron los dichos
oficios, e ficieron&nbsp;<br>cada uno dellos juramento en la se-<br>\u00f1al
dela Cruz corporalmente por ellos<br>en vida y en sus manos y alas pala-<br>bras
delos Santos Evangelios, de man<br>delos dichos oficios fiel y berdaderamte<br>y
traer provecho y verdad en el y de<br>non facer en ello solucion alguna&nbsp;
<br>ni perdida alguna en quanto lo su-<br><br><br>Group 3<br>Manuscript Image
B2U39<br>reparadas e fizose entero con ellas&nbsp;<br>e el dicho cabillo
otorgogelas como<br>dicho es; para lo qual ambas las par-<br>tes otorgaron
dos contratos de un te-<br>nor por antemi Pedro Gonzalez Ra-<br>cionero
''' 
d = extractManuscript(deleteNegativeSymbol(deleteDoubleSpace(changeCodeToSpace(deleteHTMLTags(stubString1)))))
#a = loadExcel('~/Proyectos/RCCP/Documents/Data/DS-Plasencia2014-Transcriptions.xlsx')
#print(list(a['Transriptions']))

#printManuscript(m)
df = createDataFrame(d)
saveCSV(df, '~/Proyectos/RCCP/Documents/Data/')