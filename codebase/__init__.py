from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

base_url = "https://jobs.barco.com/"
re = Request("https://jobs.barco.com/go/All-jobs/4341801")
page = urlopen(re)
soup = BeautifulSoup(page, "html.parser")
page_numbers = soup.find("ul", attrs={"class":"pagination"})

pages = []
for link in page_numbers.find_all("li"):
    pages.append(base_url + link.a.get("href"))
pages = pages[1:-1]

for page in pages:
    re = Request(page)
    job_page = urlopen(re)
    soup = BeautifulSoup(job_page, "html.parser")
    pg = soup.find_all("tr", attrs={"class":"data-row clickable"})
    for p in pg:
        position = p.td.span.a.text
        field = p.find_all("td", attrs={"class":"colDepartment hidden-phone"})[0].span.text
        location = p.find_all("td", attrs={"class":"colLocation hidden-phone"})[0].span.text
        print(position, " ", field, " ", location)