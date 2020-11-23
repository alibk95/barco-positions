from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
# import pygsheets
# from google.oauth2 import service_account

# from oauth2client.service_account import ServiceAccountCredentials
##########################################

#with open('ace-server-284012-ad303bc8a912.json') as source:
#    info = json.load(source)
#credentials = service_account.Credentials.from_service_account_info(info)
#gc = pygsheets.authorize(service_file='ace-server-284012-fdb6676e8597.json')
#sh = gc.open('email-scrape')



# because the part that we want to scrape is actually loading with a script I used chrome driver to
# emulate such a behavior and scroll till the end of the page and retrieve all the information needed
url = "https://onemarketingplace.es/busqueda/diseno%20web"
# The location of the chrome driver.
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get(url)

# Automatically scroll till the end of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

# Give it a 10 second rest to load whatever left behind : )) and then close the browser.
time.sleep(10)
page = driver.page_source
driver.quit()

# Make the soup here...magic happens here!
soup = BeautifulSoup(page, 'html.parser')
# the part that is loaded by the script is accessible
pg = soup.find("div", attrs={"class":"listado__izquierda"})
p = pg.find_all("article", attrs={"class":"item_from_search margen_top_20"})

# the base url for the more information part
base = "https://onemarketingplace.es"
# Just wanted to check how many records we got
# print(len(p))

# dataframe
df = pd.DataFrame(columns=['title', 'email'])

for s in p:
    # p consists of all the different articles in the webpage and the following path leads to the "title"
    print(s.h2.text)
    # retrieving the more info link to access the email information from there
    s1 = s.find("div", attrs={"class":"item_more_info"})
    link = s1.a.get("href")
    # concat the base link and the retrieved one and ready to access that as well
    complete_link = base+link
    # print(complete_link)
    req = Request(complete_link)
    pge = urlopen(req)
    # sp now consists of the page with information for each article. e.g. email
    sp = BeautifulSoup(pge, "html.parser")
    email = sp.find("a", attrs={"class":"contenido__correo"}).get("href")
    if email == "mailto:":
        email = ""
    print(email)
    # add the info's to the data frame.
    df = df.append({'title': s.h2.text, 'email': email[7:]}, ignore_index=True)
    # the most important thing is the object destructive function as we create a new object in each iteration
    # there's gonna be a heavy load on the system if we keep them all
    # So after each iteration we delete it
    del(sp)
    print("#####################")

print(df)
# Write the dataframe to a .csv file.
df.to_csv(r'./information.csv', index = False, header=True)

