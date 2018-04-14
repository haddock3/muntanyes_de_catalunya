# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 19:47:35 2018

@author: jach
"""

import urllib.request

#funció per descarregar l'html
def download(url, user_agent='wswp',num_retries=2):
    print('Downloading: ',url)
    headers={'User-agent': user_agent}
    request=urllib.request.Request(url, headers=headers)
    try:
        resp=urllib.request.urlopen(request)
        html=resp.read()
    except urllib.error as e:
        print('Downloading error', e.HTTPError)
        html= None
        if num_retries >0:
            print(num_retries)
            if hasattr(e, 'code') and 500<= e.code <600:
                #recursively retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)
    return html

html=download('https://ca.wikipedia.org/wiki/Llista_de_muntanyes_de_Catalunya')

from bs4 import BeautifulSoup

#generar el soup
soup=BeautifulSoup(html,'html.parser')

#trobem la taula que necessitem
table = soup.find_all('table', class_="wikitable")[0]

#definim e inicialitzem les variable
result=""
i=0

#obrim l'arxiu on descarregarem les dades
file = open('output.csv', 'wb')

for row in table.findAll("tr"):#per cada fila de la taula....
    for cell in row.findAll("td"):#per a cada una de les cel.les de la fila
        if result == "": #si es el primer <td> l'afexeixo a resultat
            result = cell.find(text=True)
        elif len(cell.findAll('a',text=True)) > 1:#si dintre d'una cel.la hi ha més d'un <a>
            for a in cell.findAll('a', text=True):
                if i == 0:#si el el primer <a> li poso un punt i coma (per el csv)
                    result = result + "; " + a.find(text=True)
                    i = i+1
                else:#si no es el primer vaig afegint comes (per el csv)
                    result = result + ", " + a.find(text=True)
            i=0 
        elif len(cell.findAll("sup")) != 0:#aquesta condicio busca un <sup>
            result = result + ";"+cell.find(text=True) 
        else:#si no es el primer <td> poso el ; (per al csv)
            result = result + "; " + cell.find(text=True)
        result = result.replace("\n", "")
        result = result.replace(" (", "")
        result = result.replace(")", "")
    result = result + "\n"        
    print(result)
    file.write(result.encode('utf-8'))
    result = ""#buido 'result'per pasar a la següent fila
    
file.close()