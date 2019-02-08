import scrapper 
import fileReader as fr
import fileWriter as fw

if __name__== "__main__":
    rawData = fr.readFile('dataCRIS.xls') 
    urlGSList = fr.getGoogleScholarURLList(rawData)

    size = len(urlGSList)
    i = 0
    j = 0.01
    data = {}
    for name, url in urlGSList.items():
        data[name] = scrapper.getStats(url)
        if i >= size*j:
            print('Datos recolectados correctamete: ', str(round(j, 2)*100), '%')
            j+=0.01
        if j > 0.03:
            break
        i+=1
    
    fw.writeJSON(data)
