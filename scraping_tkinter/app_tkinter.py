import tkinter as tk
from tkinter import messagebox
import threading
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

global scraping_running
global stop_requested
scraping_running = False
stop_requested = False

class PrincipalView:
    def __init__(self,window,general_color):
        self.window=window
        self.general_color=general_color

        top_frame = tk.Frame(window, bg=general_color, width=920, height=150)
        top_frame.place(x=1000, y=0)

        label_name_json_selected=tk.Label(top_frame,text="Nombre Json:",font=("arial","12","bold"),bg=general_color,fg="#E0F2E9",padx="5")
        label_name_json_selected.place(x=20,y=10)
        self.name_json_selected=tk.Label(top_frame,text="",font=("arial","12"),bg=general_color, fg="#E0F2E9")
        self.name_json_selected.place(x=150, y=10)

        label_genre_selected=tk.Label(top_frame,text="Genero:",font=("arial","12","bold"),bg=general_color, fg="#E0F2E9", padx="5")
        label_genre_selected.place(x=20,y=40)
        self.name_genre_selected=tk.Label(top_frame,text="",font=("arial","12"),bg=general_color, fg="#E0F2E9")
        self.name_genre_selected.place(x=100,y=40)

        label_search_type=tk.Label(top_frame,text="Tipo de búsqueda:",font=("arial","12","bold"),bg=general_color, fg="#E0F2E9", padx="5")
        label_search_type.place(x=20,y=70)
        self.name_search_type=tk.Label(top_frame,text="",font=("arial","12"),bg=general_color, fg="#E0F2E9")
        self.name_search_type.place(x=190,y=70)

        info_book_agree_btn=tk.Button(top_frame,text="INICIAR",width=15,font=("arial","10","bold"), bg="#38B2AC", fg="#FFFFFF", cursor="hand2", command=self.start_scraping)
        info_book_agree_btn.place(x=20,y=100)

        self.stop_btn = tk.Button(top_frame, text="DETENER", width=15, font=("arial","10","bold"), bg="#E74C3C", fg="#FFFFFF", cursor="hand2", command=self.stop_scraping, state="disabled")
        self.stop_btn.place(x=180, y=100)

        left_frame = tk.Frame(window, bg=general_color, width=1000, height=1080)
        left_frame.place(x=0, y=0)

        label_json_name=tk.Label(left_frame,text="Nombre del archivo Json",bg=general_color, fg="#E0F2E9", font=("arial","14","bold"))
        left_frame.update()
        label_json_name.place(x=left_frame.winfo_width()//2 - label_json_name.winfo_width()//2, y=20,anchor="center")

        self.txt_name_json=tk.Entry(left_frame,width=22,font=("arial","14"))
        self.txt_name_json.place(x=left_frame.winfo_width()//2 - label_json_name.winfo_width()//2, y=45,anchor="center")

        name_json_btn_agree_btn=tk.Button(left_frame,text="Confirmar Nombre",width=15,font=("arial","10","bold"), bg="#38B2AC", fg="#FFFFFF", cursor="hand2", command=self.set_json_name)
        name_json_btn_agree_btn.place(x=630,y=29)
   
        self.selected_option=tk.IntVar()
        radio_frame = tk.Frame(left_frame, bg=general_color)
        radio_frame.place(x=380, y=100)
        rb_best_book = tk.Radiobutton(
            radio_frame, 
            text="Los 50 mejores", 
            variable=self.selected_option, 
            value=1, 
            command=lambda: self.set_search_type(1), 
            bg=general_color, 
            fg="#FFFFFF", 
            font=("arial", "12", "bold"),
            selectcolor="#E74C3C",
            cursor="hand2",
            padx=10,
            pady=5,
            highlightthickness=0,
            bd=0,
        )
        rb_all_book = tk.Radiobutton(
            radio_frame, 
            text="Todo el género", 
            variable=self.selected_option, 
            value=2, 
            command=lambda: self.set_search_type(2), 
            bg=general_color, 
            fg="#FFFFFF", 
            font=("arial", "12", "bold"),
            selectcolor="#E74C3C",
            cursor="hand2",
            padx=10,
            pady=5,
            highlightthickness=0,
            bd=0,
        )
        rb_best_book.pack(side="left", padx=(0, 10))
        rb_all_book.pack(side="left")

        buttons_frame=tk.Frame(left_frame,width=500,height=600,bg=general_color)
        buttons_frame.place(x=60,y=180)

        row_button=0
        column_button=0
        color_button="#398579"

        for genre_button in books_genres:
            button=tk.Button(
                buttons_frame, 
                text=genre_button.replace("-"," ").capitalize(),
                width=22,
                height=2,
                bg=color_button,
                borderwidth=2,
                font=("Montserrat","8","bold"),
                fg="#E0F2E9",
                command=lambda buttonName=genre_button: self.set_genre(buttonName),
                padx=20,
                pady=10,
                cursor="hand2",
            )
            button.grid(row=row_button, column=column_button,padx=10,pady=10)
            column_button+=1

            if column_button>3:
                column_button=0
                row_button+=1

        central_frame = tk.Frame(window, bg=general_color, width=920, height=1080)
        central_frame.place(x=1000, y=150)

        self.console_central_frame = tk.Listbox(  
            central_frame,  
            width=87,
            height=33,  
            font="bold",
            selectmode = 'SINGLE',  
            background = "black",
            foreground="green",    
            selectbackground = "#D4AC0D",  
            selectforeground="BLACK"
        )
        self.console_central_frame.place(x = 22, y = 30)

    def set_json_name(self):
        try:
            self.name_json_selected.config(text=self.txt_name_json.get())
        except Exception as e:
            print(f"Error al establecer nombre JSON: {e}")

    def set_genre(self, genre):
        try:
            self.name_genre_selected.config(text=genre.replace("-"," "))
        except Exception as e:
            print(f"Error al establecer género: {e}")

    def set_search_type(self, option):
        try:
            if option==1:
                self.name_search_type.config(text="Los 50 mejores")
            
            if option==2:
                self.name_search_type.config(text="Todo el género")
        except Exception as e:
            print(f"Error al establecer tipo de búsqueda: {e}")

    def stop_scraping(self):
        global stop_requested
        stop_requested = True
        messagebox.showinfo("Deteniendo", "El scraping se detendrá después del libro actual")

    def start_scraping(self): 
        try:
            global scraping_running, stop_requested
            if scraping_running:
                    messagebox.showerror("Scraping activo","El programa está scrapeando los datos en este momento")
            else:
                if self.name_json_selected.cget("text")!="" and self.name_genre_selected.cget("text")!="" and self.name_search_type.cget("text")!="":
                    stop_requested = False
                    name_json=self.name_json_selected.cget("text")
                    type_search=self.name_search_type.cget("text")
                    book_genre=self.name_genre_selected.cget("text").replace(" ","-")
                    t = threading.Thread(target=self.get_search_data_and_start, args=(name_json, type_search, book_genre))
                    t.start()
                    self.stop_btn.config(state="normal")
                    self.name_json_selected.config(text="")
                    self.name_search_type.config(text="")
                    self.name_genre_selected.config(text="")
                    self.txt_name_json.delete(0, tk.END)
                    self.selected_option.set(0)
                else:
                    messagebox.showerror("ERROR","Debe de introducir todos los datos")
        except Exception as e:
            messagebox.showerror("ERROR",f"Error al iniciar scraping: {e}")

    def get_search_data_and_start(self, name_json, type_search, book_genre):
        global scraping_running, stop_requested
        scraping_running = True

        try:
            if type_search=="Todo el género":
                url="https://quelibroleo.com/libros/"+book_genre
            else:
                url="https://quelibroleo.com/mejores-genero/"+book_genre
        except Exception as e:
            print(f"Error construyendo URL: {e}")
            scraping_running = False
            self.stop_btn.config(state="disabled")
            return

        book_list=[]

        current_scraped_books=60
        current_page=1
        while url and not stop_requested:
            try:
                response_principal = requests.get(url)
                response_principal.raise_for_status()
            except Exception as e:
                print(f"Error accediendo a página principal: {e}")
                break

            try:
                soup_principal = BeautifulSoup(response_principal.content, "html.parser")
                items=soup_principal.find_all("div",{"class":"item"})
            except Exception as e:
                print(f"Error parseando página principal: {e}")
                break

            for item in items:
                if stop_requested:
                    break
                    
                try:
                    path_info_book = item.find("a")
                    if not path_info_book or 'href' not in path_info_book.attrs:
                        print("No se encontró enlace válido en un item")
                        continue
                        
                    url_info_book=path_info_book['href']

                    try:
                        response_info=requests.get(url_info_book)
                        response_info.raise_for_status()
                    except Exception as e:
                        print(f"Error accediendo a página del libro: {e}")
                        continue

                    try:
                        soup_info=BeautifulSoup(response_info.content,"html.parser")
                    except Exception as e:
                        print(f"Error parseando página del libro: {e}")
                        continue

                    try:
                        author=soup_info.find("div", {"class": "libro_info"}).h3.small.text.strip()
                        title_book = soup_info.find("div", {"class": "libro_info"}).h3.text.replace(author,"").strip()
                        img_book=soup_info.find("img",{"class":"imgLibros"})['src']
                        genre=soup_info.find("ul",{"class":"list"}).find_all("li")[0].text.replace("Género","").strip()
                        year_edition=soup_info.find("ul",{"class":"list"}).find_all("li")[2].text.replace("Año de edición","").strip()
                        rating=soup_info.find("div",{"class":"estadisticas"}).span.text.strip()
                        synopsis=soup_info.find("div",{"class":"content_libro"}).p.text.strip()

                        book={
                            "id":str(uuid.uuid4()),
                            "title":title_book,
                            "author":author,
                            "cover_image":img_book,
                            "genre":genre,
                            "year_edition":year_edition,
                            "rating":rating,
                            "synopsis":synopsis,
                            "url_book":url_info_book

                        }

                        self.console_central_frame.insert(tk.END, f" → {book['title']}")

                        print(book,"\n")                
                        book_list.append(book)

                        time.sleep(1)

                        if len(book_list)==current_scraped_books:
                            continue_scraping=messagebox.askyesno("CONFIRMAR",f"Llevas {current_scraped_books} libros y vas por la página {current_page}. Deseas continuar?")
                            if continue_scraping:
                                current_scraped_books+=50
                            else:
                                url=None
                                break

                    except Exception as e:
                        print("Error extrayendo datos del libro:",e)
                        continue

                except Exception as e:
                    print(f"Error procesando item: {e}")
                    continue

            if stop_requested:
                break

            try:
                pagination = soup_principal.find('ul', {'class': 'pagination justify-content-center'})
                if pagination and url!=None:
                    next_link = pagination.find('a', {'rel': 'next'})
                    if next_link:
                        url = next_link['href']
                        current_page+=1
                    else:
                        url = None
                else:
                    url = None
            except Exception as e:
                print(f"Error buscando paginación: {e}")
                url = None
        
        try:
            current_directory=os.getcwd()
            json_book_directory=os.path.join(current_directory,"Libros_json")

            if not os.path.exists(json_book_directory):
                os.makedirs(json_book_directory)

            book_list_json=json.dumps(book_list, ensure_ascii=False, indent=2)
            print("\n\n")
            print(book_list_json)

            complete_path=os.path.join(json_book_directory,name_json+".json")
            with open(complete_path,'w',encoding='utf-8') as f:
                f.write(book_list_json)

            if stop_requested:
                messagebox.showinfo("DETENIDO",f"Scraping detenido manualmente. Se guardaron {len(book_list)} libros")
            else:
                messagebox.showinfo("FIN",f"Se ha terminado el scrapeo con un total de {len(book_list)} libros")

        except Exception as e:
            print(f"Error guardando JSON: {e}")
            messagebox.showerror("ERROR",f"Error al guardar el archivo: {e}")

        finally:
            scraping_running = False
            stop_requested = False
            self.stop_btn.config(state="disabled")


if __name__ == "__main__":
    books_genres = get_books_genres()
    general_color = "#0C2233"

    root=tk.Tk()
    view=PrincipalView(root,general_color)
    root.title("Scraping Libros")
    root.geometry("1920x1080")
    root.resizable(0,0)
    root.mainloop()