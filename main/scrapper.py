import requests
from models import Tables
from bs4 import BeautifulSoup
# from .schemas import Result
from datetime import datetime
from typing import List


baseUrl = "https://gtu.ac.in/Syllabus"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
}

def get_links(url):
    links = set()
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    urls = soup.find_all("a")
    for url in urls: 
        link = url.get("href")
        if "syllabus" in link.lower():
            continue 
        links.add(link)    
    return links
    

def fetch_data(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find_all("section", {"class": "page-banner"}).text
    data = soup.find("table")
    print(f"Name: {name}")
    # if url == baseUrl:
        # tb = Tables(name = name, link = url, data = data)
    
    # tb = Tables(name = )


    

def crawller():
    # links = get_links(baseUrl)
    data = fetch_data(baseUrl)

    print(data)
    # print(len(links))
    # page = requests.get(url, headers=headers)
    # links = {}
    
    # soup = BeautifulSoup(page.content, "html.parser")
    # table = soup.find("table")
    # # print(table)
    # for index, tag in enumerate(table):
    #     if isinstance(tag, str):
    #         continue
    #     print(f"N-{type(tag)}")
    #     print("________________________________--")

    #     if index >= 2:
    #         break
        

if __name__ == "__main__":
    crawller()
