import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid

newBooksList = []

def scrapingBooks(url):
    try:
        responsePrincipal = requests.get(url)
        responsePrincipal.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a la página principal: {e}")
        return

    try:
        soupPrincipal = BeautifulSoup(responsePrincipal.content, "html.parser")
        newCarousel = soupPrincipal.find("div", {"class": "carousel novedades"})
        
        if not newCarousel:
            print("No se encontró el carrusel de novedades")
            return
            
        items = newCarousel.find_all("div", {"class": "item"})
    except Exception as e:
        print(f"Error al parsear la página principal: {e}")
        return

    for item in items:
        try:
            pathInfoBook = item.find("a")
            if not pathInfoBook or 'href' not in pathInfoBook.attrs:
                print("No se encontró enlace válido en un item")
                continue
                
            urlInfoBook = pathInfoBook['href']

            try:
                responseInfo = requests.get(urlInfoBook)
                responseInfo.raise_for_status()
            except Exception as e:
                print(f"Error al acceder a la página del libro: {e}")
                continue

            try:
                soupInfo = BeautifulSoup(responseInfo.content, "html.parser")
            except Exception as e:
                print(f"Error al parsear la página del libro: {e}")
                continue

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

                isbn = soupInfo.find("ul", {
                        "class": "list"
                    }).find_all("li")[3].text.replace("ISBN", "").strip()

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
                    "isbn": isbn,
                    "rating": rating,
                    "synopsis": synopsis,
                    "urlBook": urlInfoBook
                }

                print(book, "\n")
                newBooksList.append(book)

                time.sleep(1)

            except Exception as e:
                print(f"Error extrayendo datos de un libro: {e}")
                continue

        except Exception as e:
            print(f"Error procesando un item: {e}")
            continue

def createJson(nameJson):
    try:
        currentDirectory = os.getcwd()
        jsonBookDirectory = os.path.join(currentDirectory, "Libros_json")

        if not os.path.exists(jsonBookDirectory):
            os.makedirs(jsonBookDirectory)

        bookListJson = json.dumps(newBooksList, ensure_ascii=False, indent=2)
        print("\n\n")
        print(bookListJson)

        completePath = os.path.join(jsonBookDirectory, nameJson + ".json")
        with open(completePath, 'w', encoding='utf-8') as f:
            f.write(bookListJson)
            
    except Exception as e:
        print(f"Error creando el JSON: {e}")

url = "https://quelibroleo.com/"
scrapingBooks(url)
createJson("novedades")