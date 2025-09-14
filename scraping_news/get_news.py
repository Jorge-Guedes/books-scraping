import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid

new_books_list = []

def scraping_books(url):
    try:
        response_principal = requests.get(url)
        response_principal.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a la página principal: {e}")
        return

    try:
        soup_principal = BeautifulSoup(response_principal.content, "html.parser")
        new_carousel = soup_principal.find("div", {"class": "carousel novedades"})
        
        if not new_carousel:
            print("No se encontró el carrusel de novedades")
            return
            
        items = new_carousel.find_all("div", {"class": "item"})
    except Exception as e:
        print(f"Error al parsear la página principal: {e}")
        return

    for item in items:
        try:
            path_info_book = item.find("a")
            if not path_info_book or 'href' not in path_info_book.attrs:
                print("No se encontró enlace válido en un item")
                continue
                
            url_info_book = path_info_book['href']

            try:
                response_info = requests.get(url_info_book)
                response_info.raise_for_status()
            except Exception as e:
                print(f"Error al acceder a la página del libro: {e}")
                continue

            try:
                soup_info = BeautifulSoup(response_info.content, "html.parser")
            except Exception as e:
                print(f"Error al parsear la página del libro: {e}")
                continue

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
                }).find_all("li")[2].text.replace("Año de edición", "").strip()

                isbn = soup_info.find("ul", {
                        "class": "list"
                    }).find_all("li")[3].text.replace("ISBN", "").strip()

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
                    "cover_image": img_book,
                    "genre": genre,
                    "year_edition": year_edition,
                    "isbn": isbn,
                    "rating": rating,
                    "synopsis": synopsis,
                    "url_book": url_info_book
                }

                print(book, "\n")
                new_books_list.append(book)

                time.sleep(1)

            except Exception as e:
                print(f"Error extrayendo datos de un libro: {e}")
                continue

        except Exception as e:
            print(f"Error procesando un item: {e}")
            continue

def create_json(name_json):
    try:
        current_directory = os.getcwd()
        json_book_directory = os.path.join(current_directory, "Libros_json")

        if not os.path.exists(json_book_directory):
            os.makedirs(json_book_directory)

        book_list_json = json.dumps(new_books_list, ensure_ascii=False, indent=2)
        print("\n\n")
        print(book_list_json)

        complete_path = os.path.join(json_book_directory, name_json + ".json")
        with open(complete_path, 'w', encoding='utf-8') as f:
            f.write(book_list_json)
            
    except Exception as e:
        print(f"Error creando el JSON: {e}")

url = "https://quelibroleo.com/"
scraping_books(url)
create_json("novedades")