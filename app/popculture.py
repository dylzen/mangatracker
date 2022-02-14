import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import config
import re

def search_manga():

    duplicate_links = []
    manga = input("Enter title: ")
    manga_plus = manga.replace(" ", "+")
    manga_separated = manga.split()
    print(manga_separated)
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    search_url = config.popculture_search_url+manga_plus
    print(search_url)
    response = requests.get(search_url, timeout=10, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select_one("div.col-md-6:nth-child(1) > p:nth-child(2)")
    if results == None:
        print("No results.")
        exit()
    print(results.text)
    results_int = [int(s) for s in results.text.split() if s.isdigit()]
    results_number = results_int[0]

    pages = []
    if 0 <= results_number <=100 :
        pages.append(1)
    elif 101 <= results_number <=200 :
        pages.extend(range(1,3))
    elif 201 <= results_number <=300 :
        pages.extend(range(1,4))
    elif 301 <= results_number <=400 :
        pages.extend(range(1,5))
    elif 401 <= results_number <=500 :
        pages.extend(range(1,6))
    elif 501 <= results_number <=600 :
        pages.extend(range(1,7))
    elif 601 <= results_number <=700 :
        pages.extend(range(1,8))
    elif 701 <= results_number <=800 :
        pages.extend(range(1,9))
    elif 801 <= results_number <=900 :
        pages.extend(range(1,10))
    elif 901 <= results_number <=1000 :
        pages.extend(range(1,11))
    elif 1001 <= results_number <=1100 :
        pages.extend(range(1,12))
    else:
        print("Too many results. Please use fewer words.")
        exit()

    print("Page " + str(pages[0]))
    for i in soup.select("a[href*=manga]"):
        result = i.get('href')
        print(result)
        duplicate_links.append(result)
    print("Completed page " + str(pages[0]))

    if len(pages) > 1:
        for page in pages[1:]:
            print("Page " + str(page))
            search_url_multiple = search_url + "&page=" + str(page)
            response = requests.get(search_url_multiple, timeout=10, headers=headers)
            print(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            for i in soup.select("a[href*=manga]"):
                result = i.get('href')
                print(result)
                duplicate_links.append(result)
            print("Completed page "+str(page))
            sleep(randint(1,5))
    links = list(set(duplicate_links))
    links = [item.lower() for item in links]
    links[:] = [url for url in links if all(ignore in url for ignore in manga_separated)]
    links.sort()
    print("Fetched "+str(len(links))+ " results.")
    availability_full_text = []
    page_titles = []
    for link in links:
        print(link)
        response = requests.get(link, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_titles.append(soup.select_one('.productpage_title').text)
        availability = soup.find(text=re.compile('^Data di uscita'))    
        try:
            stripped = availability.parent.previous_element.text.replace(u'\xa0', u' ')
            availability_full_text.append(stripped)
            print("Found release date!")
        except AttributeError as error:
            print("Release date not found...")
            availability_full_text.append("Out of stock")

    lists_merge = list(zip(page_titles, links, availability_full_text))
    print(*lists_merge, sep = "\n")
