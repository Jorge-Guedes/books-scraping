import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid


def get_books_genres():
    url = "https://quelibroleo.com/web/public/mejores-genero"
    response_page = requests.get(url)
    soup_page = BeautifulSoup(response_page.content, "html.parser")

    books_genres = []

    try:
        genres_div = soup_page.find("div", {"class":"content"})
        a_items = genres_div.find_all("a")
        for item in a_items:
            first_span = item.find("span")
            if first_span:
                span_text = first_span.text.strip().lower()
                refined_text = span_text.replace(", ", "-").replace(" ", "-").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                books_genres.append(refined_text)
        
        return books_genres

    except Exception as e:
        print("Error extrayendo los géneros:", e)
    

book_list = []
def scraping_books(url, enable_limit, limit_per_genre):
    try:
        current_url = url
        
        while current_url:
            response_principal = requests.get(current_url)
            soup_principal = BeautifulSoup(response_principal.content, "html.parser")

            items = soup_principal.find_all("div", {"class": "item"})

            for item in items:

                print(f"TAMAÑO DE LA LISTA: {len(book_list)}")
                if enable_limit and len(book_list) == 50:
                    return

                if limit_per_genre and len(book_list) == 50:
                    return

                try:
                    path_info_book = item.find("a")
                    url_info_book = path_info_book['href']

                    try:
                        response_info = requests.get(url_info_book)
                        soup_info = BeautifulSoup(response_info.content, "html.parser")

                        try:
                            author = soup_info.find("div", {
                                "class": "libro_info"
                            }).h3.small.text.strip()

                            title_book = soup_info.find("div", {
                                "class": "libro_info"
                            }).h3.text.replace(author, "").strip()

                            img_book = soup_info.find("img", {"class": "imgLibros"})['src']
                            genre = soup_info.find("ul", {
                                "class": "list"
                            }).find_all("li")[0].text.replace("Género", "").strip()

                            year_edition = soup_info.find("ul", {
                                "class": "list"
                            }).find_all("li")[2].text.replace("Año de edición",
                                                            "").strip()

                            isbn = soup_info.find("ul", {
                                "class": "list"
                            }).find_all("li")[3].text.replace("ISBN",
                                                            "").strip()

                            rating = soup_info.find("div", {
                                "class": "estadisticas"
                            }).span.text.strip()

                            synopsis = soup_info.find("div", {
                                "class": "content_libro"
                            }).p.text.strip()

                            book = {
                                "id": str(uuid.uuid4()),
                                "title": title_book,
                                "author": author,
                                "coverImage": img_book,
                                "genre": genre,
                                "yearEdition": year_edition,
                                "isbn": isbn,
                                "rating": rating,
                                "synopsis": synopsis,
                                "urlBook": url_info_book
                            }

                            print(book, "\n")
                            book_list.append(book)

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

            pagination = soup_principal.find('ul', {'class': 'pagination justify-content-center'})
            if pagination:
                next_link = pagination.find('a', {'rel': 'next'})
                if next_link:
                    current_url = next_link['href']
                    print(f"Pasando a la siguiente página: {current_url}")
                else:
                    current_url = None
            else:
                current_url = None

    except Exception as e:
        print(f"Error accediendo a la página principal: {e}")

def create_json(name_json):
    current_directory = os.getcwd()
    json_book_directory = os.path.join(current_directory, "Libros_json")

    if not os.path.exists(json_book_directory):
        os.makedirs(json_book_directory)

    book_list_json = json.dumps(book_list, ensure_ascii=False, indent=2)
    print("\n\n")
    print(book_list_json)

    complete_path = os.path.join(json_book_directory, name_json + ".json")
    with open(complete_path, 'w', encoding='utf-8') as f:
        f.write(book_list_json)

def select_genre():
    for index, genre in enumerate(books_genres):
        print((index + 1), genre.replace("-", " "))

    index_genre = int(input("\nSelecciona el género: "))
    genre_selected = books_genres[index_genre - 1]
    return genre_selected

# Obtener los géneros primero
books_genres = get_books_genres()

type_search = input(
    "Seleccionar tipo de búsqueda:\n\t1 - Top 50 por género\n\t2 - Todos los libros por género\n\t3 - Top 50 de cada género\n"
)

if type_search == "1":
    genre_selected = select_genre()
    url = "https://quelibroleo.com/web/public/libros/" + genre_selected
    name_json = genre_selected
    scraping_books(url, True, False)
    create_json(name_json)
elif type_search == "2":
    genre_selected = select_genre()
    url = "https://quelibroleo.com/mejores-genero/" + genre_selected
    name_json = genre_selected
    scraping_books(url, False, False)
    create_json(name_json)
elif type_search == "3":
    for genre in books_genres:
        url = "https://quelibroleo.com/mejores-genero/" + genre
        name_json = genre
        scraping_books(url, False, True)
        create_json(name_json)
        book_list = []
else:
    print("Opción incorrecta")

