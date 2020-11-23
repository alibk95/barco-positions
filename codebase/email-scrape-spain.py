from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd
import pygsheets
from google.oauth2 import service_account
import json
from oauth2client.service_account import ServiceAccountCredentials
##########################################

#with open('ace-server-284012-ad303bc8a912.json') as source:
#    info = json.load(source)
#credentials = service_account.Credentials.from_service_account_info(info)
#gc = pygsheets.authorize(service_file='ace-server-284012-fdb6676e8597.json')
#sh = gc.open('email-scrape')




url = "https://onemarketingplace.es/busqueda/diseno%20web"
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get(url)

#while driver.find_element_by_tag_name('div'):
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    Divs = driver.find_element_by_tag_name('div').text
#    if 'End of Results' in Divs:
#        break
#    else:
#        continue

time.sleep(3)
page = driver.page_source
driver.quit()

soup = BeautifulSoup(page, 'html.parser')

pg = soup.find("div", attrs={"class":"listado__izquierda"})
p = pg.find_all("article", attrs={"class":"item_from_search margen_top_20"})
base = "https://onemarketingplace.es"
print(len(p))

# dataframe
df = pd.DataFrame(columns=['title', 'email'])

for s in p:
    print(s.h2.text)

    s1 = s.find("div", attrs={"class":"item_more_info"})
    link = s1.a.get("href")
    complete_link = base+link
    #print(complete_link)
    req = Request(complete_link)
    pge = urlopen(req)
    sp = BeautifulSoup(pge, "html.parser")
    email = sp.find("a", attrs={"class":"contenido__correo"}).get("href")
    if email == "mailto:":
        email = ""
    print(email)

    df = df.append({'title': s.h2.text, 'email': email[7:]}, ignore_index=True)
    print("#####################")

print(df)
df.to_csv(r'./information.csv', index = False, header=True)
####################################################################
#base_url = "https://onemarketingplace.es/busqueda/diseno%20web"

#res = requests.get("https://onemarketingplace.es/busqueda/diseno%20web")
#print(res)
#re = Request(base_url)

#page = urlopen(re)
#soup = BeautifulSoup(page, "html.parser")
#print(soup)
#pg = soup.find("div", attrs={"id":"resultAjax"})
