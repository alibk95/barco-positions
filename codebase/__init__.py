from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

base_url = "https://jobs.barco.com/"
re = Request("https://jobs.barco.com/go/All-jobs/4341801/?q=&sortColumn=referencedate&sortDirection=desc")
page = urlopen(re)
soup = BeautifulSoup(page, "html.parser")
page_numbers = soup.find("ul", attrs={"class":"pagination"})

pages = []
for link in page_numbers.find_all("li"):
    pages.append(base_url + link.a.get("href"))
pages = pages[1:-1]

print(pages)
