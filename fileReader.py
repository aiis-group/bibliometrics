import pandas as pd 

def readFile(file):
    df = pd.read_excel(file, sheet_name='main_entities')
    return df

def getGoogleScholarURLList(df):
    gslist = dict(zip(formatNames(df.fullName), formatURL(df.GoogleSchoolar)))
    print(gslist)

def formatNames(names):
    names = [name.replace("[visibility=PUBLIC]", "") for name in names]
    return [" ".join(name.split(", ")[::-1]) for name in names]
    

def formatURL(urls):
    print(urls)
    urls = [url.replace("[visibility=PUBLIC URL=", "") for url in urls if type(url) is str]
    urls = [url.replace("[visibility=PUBLIC URL=]", "") for url in urls if type(url) is str]
    return [url.replace("]Google Scholar", "") for url in urls if type(url) is str]


getGoogleScholarURLList(readFile('./dataCRIS.xls'))