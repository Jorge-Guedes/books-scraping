import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid

newBooksList = []


def scrapingBooks(url):
    responsePrincipal = requests.get(url)
    soupPrincipal = BeautifulSoup(responsePrincipal.content, "html.parser")

    newCarousel = soupPrincipal.find("div", {"class": "carousel novedades"})
    items = newCarousel.find_all("div", {"class": "item"})

    for item in items:
        pathInfoBook = item.find("a")
        urlInfoBook = pathInfoBook['href']

        responseInfo = requests.get(urlInfoBook)
        soupInfo = BeautifulSoup(responseInfo.content, "html.parser")

        try:
            author = soupInfo.find("div", {
                "class": "libro_info"
            }).h3.small.text.strip()

            titleBook = soupInfo.find("div", {
                "class": "libro_info"
            }).h3.text.replace(author, "").strip()

            imgBook = soupInfo.find("img", {"class": "imgLibros"})['src']
            genre = soupInfo.find("ul", {
                "class": "list"
            }).find_all("li")[0].text.replace("Género", "").strip()

            yearEdition = soupInfo.find("ul", {
                "class": "list"
            }).find_all("li")[2].text.replace("Año de edición", "").strip()

            rating = soupInfo.find("div", {
                "class": "estadisticas"
            }).span.text.strip()

            synopsis = soupInfo.find("div", {
                "class": "content_libro"
            }).p.text.strip()

            book = {
                "id": str(uuid.uuid4()),
                "title": titleBook,
                "author": author,
                "coverImage": imgBook,
                "genre": genre,
                "yearEdition": yearEdition,
                "rating": rating,
                "synopsis": synopsis,
                "urlBook": urlInfoBook
            }

            print(book, "\n")
            newBooksList.append(book)

            time.sleep(1)

        except Exception as e:
            print("Error:", e)


def createJson(nameJson):
    currentDirectory = os.getcwd()
    jsonBookDirectory = os.path.join(currentDirectory, "Libros_json")

    if not os.path.exists(jsonBookDirectory):
        os.makedirs(jsonBookDirectory)

    bookListJson = json.dumps(newBooksList, ensure_ascii=False)
    print("\n\n")
    print(bookListJson)

    completePath = os.path.join(jsonBookDirectory, nameJson + ".json")
    with open(completePath, 'w', encoding='utf-8') as f:
        f.write(bookListJson)


url = "https://quelibroleo.com/"
scrapingBooks(url)
createJson("novedades")
