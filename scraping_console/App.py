import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid

booksGenres = [
    "actores", "arte", "autoayuda", "autoayuda-y-espiritualidad",
    "biografias-memorias", "ciencias", "ciencias-humanas",
    "ciencias-politicas-y-sociales", "clasicos-de-la-literatura", "cocina",
    "comics-novela-grafica", "deportes-y-juegos", "derecho",
    "dietetica-y-nutricion", "economia", "empresa", "ensayo",
    "estudios-y-ensayos", "fantastica-ciencia-ficcion", "ficcion-literaria",
    "filologia", "fotografia", "guias-de-viaje", "historia",
    "historia-del-cine", "historica-y-aventuras", "humor",
    "infantil-y-juvenil", "informatica", "juvenil", "lecturas-complementarias",
    "literatura-contemporanea", "medicina", "musica", "narrativa",
    "narrativa-historica", "no-ficcion", "novela-negra-intriga-terror",
    "poesia", "poesia-teatro", "psicologia-y-pedagogia", "romantica-erotica",
    "varios"
]

bookList = []

def scrapingBooks(url):
    try:
        current_url = url
        
        while current_url:
            responsePrincipal = requests.get(current_url)
            soupPrincipal = BeautifulSoup(responsePrincipal.content, "html.parser")

            items = soupPrincipal.find_all("div", {"class": "item"})

            for item in items:
                try:
                    pathInfoBook = item.find("a")
                    urlInfoBook = pathInfoBook['href']

                    try:
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
                            }).find_all("li")[2].text.replace("Año de edición",
                                                            "").strip()

                            isbn = soupInfo.find("ul", {
                                "class": "list"
                            }).find_all("li")[3].text.replace("ISBN",
                                                            "").strip()

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
                            bookList.append(book)

                            time.sleep(1)

                        except Exception as e:
                            print("Error extrayendo datos:", e)
                            continue

                    except Exception as e:
                        print(f"Error accediendo a la página de un libro: {e}")
                        continue

                except Exception as e:
                    print(f"Error procesando un item: {e}")
                    continue

            pagination = soupPrincipal.find('ul', {'class': 'pagination justify-content-center'})
            if pagination:
                nextLink = pagination.find('a', {'rel': 'next'})
                if nextLink:
                    current_url = nextLink['href']
                    print(f"Pasando a la siguiente página: {current_url}")
                else:
                    current_url = None
            else:
                current_url = None

    except Exception as e:
        print(f"Error accediendo a la página principal: {e}")

def createJson(nameJson):
    currentDirectory = os.getcwd()
    jsonBookDirectory = os.path.join(currentDirectory, "Libros_json")

    if not os.path.exists(jsonBookDirectory):
        os.makedirs(jsonBookDirectory)

    bookListJson = json.dumps(bookList, ensure_ascii=False, indent=2)
    print("\n\n")
    print(bookListJson)

    completePath = os.path.join(jsonBookDirectory, nameJson + ".json")
    with open(completePath, 'w', encoding='utf-8') as f:
        f.write(bookListJson)

def selectGenre():
    for index, genre in enumerate(booksGenres):
        print((index + 1), genre.replace("-", " "))

    indexGenre = int(input("\nSelecciona el género: "))
    genreSelected = booksGenres[indexGenre - 1]
    return genreSelected

typeSearch = input(
    "Seleccionar tipo de búsqueda:\n\t1 - Los 50 mejores\n\t2 - Todos los libros de un genero\n\t3 - Los 50 mejores de todos los generos\n"
)

if typeSearch == "1":
    genreSelected = selectGenre()
    url = "https://quelibroleo.com/libros/" + genreSelected
    nameJson = genreSelected
    scrapingBooks(url)
    createJson(nameJson)
elif typeSearch == "2":
    genreSelected = selectGenre()
    url = "https://quelibroleo.com/mejores-genero/" + genreSelected
    nameJson = genreSelected
    scrapingBooks(url)
    createJson(nameJson)
elif typeSearch == "3":
    for genre in booksGenres:
        url = "https://quelibroleo.com/mejores-genero/" + genre
        nameJson = genre
        scrapingBooks(url)
        createJson(nameJson)
        bookList = []
else:
    print("Opción incorrecta")