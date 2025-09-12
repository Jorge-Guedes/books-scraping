import tkinter as tk
from tkinter import messagebox
import threading
import requests
import json
from bs4 import BeautifulSoup
import time
import os
import uuid

booksGenres=["actores","arte","autoayuda","autoayuda-y-espiritualidad","biografias-memorias","ciencias","ciencias-humanas",
             "ciencias-politicas-y-sociales","clasicos-de-la-literatura","cocina","comics-novela-grafica","deportes-y-juegos","derecho",
             "dietetica-y-nutricion","economia","empresa","ensayo","estudios-y-ensayos","fantastica-ciencia-ficcion","ficcion-literaria",
             "filologia","fotografia","guias-de-viaje","historia","historia-del-cine","historica-y-aventuras","humor","infantil-y-juvenil",
             "informatica","juvenil","lecturas-complementarias","literatura-contemporanea","medicina","musica","narrativa","narrativa-historica",
             "no-ficcion","novela-negra-intriga-terror","poesia","poesia-teatro","psicologia-y-pedagogia","romantica-erotica","varios"]

global scrapingRunning
scrapingRunning=""

class PrincipalView:
    def __init__(self,window):
        self.window=window

        #frame superior
        topFrame = tk.Frame(window, bg="#c5eaf0", width=920, height=150)  # width ajustado
        topFrame.place(x=1000, y=0)

        labelNameJsonSelected=tk.Label(topFrame,text="Nombre Json:",font=("arial","12","bold"),bg="#c5eaf0")
        labelNameJsonSelected.place(x=20,y=10)
        nameJsonSelected=tk.Label(topFrame,text="",font=("arial","12"),bg="#c5eaf0")
        nameJsonSelected.place(x=137, y=10)

        labelGenreSelected=tk.Label(topFrame,text="Genero:",font=("arial","12","bold"),bg="#c5eaf0")
        labelGenreSelected.place(x=20,y=40)
        nameGenreSelected=tk.Label(topFrame,text="",font=("arial","12"),bg="#c5eaf0")
        nameGenreSelected.place(x=90,y=40)

        labelSearchType=tk.Label(topFrame,text="Tipo de búsqueda:",font=("arial","12","bold"),bg="#c5eaf0")
        labelSearchType.place(x=20,y=70)
        nameSearchType=tk.Label(topFrame,text="",font=("arial","12"),bg="#c5eaf0")
        nameSearchType.place(x=172,y=70)

        infoBookAgreeBtn=tk.Button(topFrame,text="INICIAR",width=15,font=("arial","10","bold"),command=lambda: startScraping())
        infoBookAgreeBtn.place(x=20,y=100)
        

        #frame izquierdo
        leftFrame = tk.Frame(window, bg="#c5eaf0", width=830, height=930)
        leftFrame.place(x=0, y=0)

        labelJsonName=tk.Label(leftFrame,text="Nombre del archivo Json",bg="#c5eaf0",font=("arial","14","bold"))
        leftFrame.update()#actualizo el frame para poder centrar el label
        labelJsonName.place(x=leftFrame.winfo_width()//2 - labelJsonName.winfo_width()//2, y=20,anchor="center")

        txtNameJson=tk.Entry(leftFrame,width=22,font=("arial","14"))
        txtNameJson.place(x=leftFrame.winfo_width()//2 - labelJsonName.winfo_width()//2, y=45,anchor="center")

        nameJsonBtnAgreeBtn=tk.Button(leftFrame,text="Confirmar Nombre",width=15,font=("arial","10","bold"),command=lambda: setJsonName())
        nameJsonBtnAgreeBtn.place(x=500,y=31)
   
        selectedOption=tk.IntVar()
        rbBestBook = tk.Radiobutton(root, text="Los 50 mejores", variable=selectedOption, value=1, command=lambda: setSearchType(1),bg="#c5eaf0",font=("arial","12","bold"))
        rbAllBook = tk.Radiobutton(root, text="Todo el género", variable=selectedOption, value=2, command=lambda: setSearchType(2),bg="#c5eaf0",font=("arial","12","bold"))
        rbBestBook.place(x=leftFrame.winfo_width()//2 - labelJsonName.winfo_width()//2-80, y=100,anchor="center")
        rbAllBook.place(x=leftFrame.winfo_width()//2 - labelJsonName.winfo_width()//2+80, y=100,anchor="center")

        buttonsFrame=tk.Frame(leftFrame,width=500,height=600,bg="#c5eaf0")
        buttonsFrame.place(x=0,y=180)

        rowButton=0
        columnButton=0
        colorButton="#417531"
        nextColor=0
        for genreButton in booksGenres:
            button=tk.Button(
                    buttonsFrame, 
                    text=genreButton.replace("-"," "),
                    width=22,
                    height=2,
                    bg=colorButton, 
                    borderwidth=3,
                    font=("arial","9","bold"),
                    fg="#e9f2f1",
                    command=lambda buttonName=genreButton: setGenre(buttonName)
                )
            button.grid(row=rowButton, column=columnButton,padx=10,pady=10)
            columnButton+=1

            nextColor+=1

            if nextColor==0:
                colorButton="#417531"
            elif nextColor==1:
                colorButton="#315375"
            else:
                colorButton="#b43a27"

            if nextColor>2:
                nextColor=0
                colorButton="#417531"

            if columnButton>3:
                columnButton=0
                rowButton+=1

        
        #frame muestra de libros scrapeados
        centralFrame = tk.Frame(window, bg="#d4eff3", width=900, height=780)
        centralFrame.place(x=1000, y=150)

        consoleCentralFrame = tk.Listbox(  
            centralFrame,  
            width=125,
            height=42,  
            font="bold",
            selectmode = 'SINGLE',  
            background = "black",
            foreground="green",    
            selectbackground = "#D4AC0D",  
            selectforeground="BLACK"
        )
        consoleCentralFrame.place(x = 22, y = 30)

        
        def setJsonName():
            try:
                nameJsonSelected.config(text=txtNameJson.get())
            except Exception as e:
                print(f"Error al establecer nombre JSON: {e}")

        def setGenre(genre):
            try:
                nameGenreSelected.config(text=genre.replace("-"," "))
            except Exception as e:
                print(f"Error al establecer género: {e}")

        def setSearchType(option):
            try:
                if option==1:
                    nameSearchType.config(text="Los 50 mejores")
                
                if option==2:
                    nameSearchType.config(text="Todo el género")
            except Exception as e:
                print(f"Error al establecer tipo de búsqueda: {e}")


        def startScraping(): 
            try:
                if scrapingRunning:
                        messagebox.showerror("Scraping activo","El programa está scrapeando los datos en este momento")
                else:
                    if nameJsonSelected.cget("text")!="" and nameGenreSelected.cget("text")!="" and nameSearchType.cget("text")!="":
                        print("Se puede empezar")
                        nameJson=nameJsonSelected.cget("text")
                        typeSearch=nameSearchType.cget("text")
                        bookGenre=nameGenreSelected.cget("text").replace(" ","-")
                        t = threading.Thread(target=getSearchDataAndStart, args=(nameJson, typeSearch, bookGenre))
                        t.start()
                        nameJsonSelected.config(text="")
                        nameSearchType.config(text="")
                        nameGenreSelected.config(text="")
                    else:
                        messagebox.showerror("ERROR","Debe de introducir todos los datos")
            except Exception as e:
                messagebox.showerror("ERROR",f"Error al iniciar scraping: {e}")
        

        def getSearchDataAndStart(nameJson,typeSearch,bookGenre):
            global scrapingRunning
            scrapingRunning=True

            try:
                if typeSearch=="Todo el género":
                    url="https://quelibroleo.com/libros/"+bookGenre
                else:
                    url="https://quelibroleo.com/mejores-genero/"+bookGenre
            except Exception as e:
                print(f"Error construyendo URL: {e}")
                scrapingRunning=False
                return

            bookList=[]

            actualScrapedBooks=60;
            actualPage=1;
            while url:
                try:
                    responsePrincipal = requests.get(url)
                    responsePrincipal.raise_for_status()
                except Exception as e:
                    print(f"Error accediendo a página principal: {e}")
                    break

                try:
                    soupPrincipal = BeautifulSoup(responsePrincipal.content, "html.parser")
                    items=soupPrincipal.find_all("div",{"class":"item"})
                except Exception as e:
                    print(f"Error parseando página principal: {e}")
                    break

                for item in items:
                    try:
                        pathInfoBook = item.find("a")
                        if not pathInfoBook or 'href' not in pathInfoBook.attrs:
                            print("No se encontró enlace válido en un item")
                            continue
                            
                        urlInfoBook=pathInfoBook['href']

                        try:
                            responseInfo=requests.get(urlInfoBook)
                            responseInfo.raise_for_status()
                        except Exception as e:
                            print(f"Error accediendo a página del libro: {e}")
                            continue

                        try:
                            soupInfo=BeautifulSoup(responseInfo.content,"html.parser")
                        except Exception as e:
                            print(f"Error parseando página del libro: {e}")
                            continue

                        try:
                            author=soupInfo.find("div", {"class": "libro_info"}).h3.small.text.strip()
                            titleBook = soupInfo.find("div", {"class": "libro_info"}).h3.text.replace(author,"").strip()
                            imgBook=soupInfo.find("img",{"class":"imgLibros"})['src']
                            genre=soupInfo.find("ul",{"class":"list"}).find_all("li")[0].text.replace("Género","").strip()
                            yearEdition=soupInfo.find("ul",{"class":"list"}).find_all("li")[2].text.replace("Año de edición","").strip()
                            rating=soupInfo.find("div",{"class":"estadisticas"}).span.text.strip()
                            synopsis=soupInfo.find("div",{"class":"content_libro"}).p.text.strip()

                            book={
                                "id":str(uuid.uuid4()),
                                "title":titleBook,
                                "author":author,
                                "coverImage":imgBook,
                                "genre":genre,
                                "yearEdition":yearEdition,
                                "rating":rating,
                                "synopsis":synopsis,
                                "urlBook":urlInfoBook

                            }

                            #mostrar en frame
                            consoleCentralFrame.insert(tk.END,book)

                            print(book,"\n")                
                            bookList.append(book);

                            time.sleep(1);

                            if len(bookList)==actualScrapedBooks:
                                continueScraping=messagebox.askyesno("CONFIRMAR",f"Llevas {actualScrapedBooks} libros y vas por la página {actualPage}. Deseas continuar?")
                                if continueScraping:
                                    actualScrapedBooks+=50;
                                else:
                                    url=None;
                                    break;

                        except Exception as e:
                            print("Error extrayendo datos del libro:",e)
                            continue

                    except Exception as e:
                        print(f"Error procesando item: {e}")
                        continue

                # pagina siguiente
                try:
                    pagination = soupPrincipal.find('ul', {'class': 'pagination justify-content-center'});
                    if pagination and url!=None:
                        nextLink = pagination.find('a', {'rel': 'next'});
                        if nextLink:
                            url = nextLink['href'];
                            actualPage+=1;
                        else:
                            url = None;
                    else:
                        url = None;
                except Exception as e:
                    print(f"Error buscando paginación: {e}")
                    url = None
            
            try:
                currentDirectory=os.getcwd()
                jsonBookDirectory=os.path.join(currentDirectory,"Libros_json")

                if not os.path.exists(jsonBookDirectory):
                    os.makedirs(jsonBookDirectory)

                bookListJson=json.dumps(bookList, ensure_ascii=False, indent=2)
                print("\n\n")
                print(bookListJson)

                completePath=os.path.join(jsonBookDirectory,nameJson+".json")
                with open(completePath,'w',encoding='utf-8') as f:
                    f.write(bookListJson)

                messagebox.showinfo("FIN",f"Se ha terminado el scrapeo con un total de {len(bookList)} libros")

            except Exception as e:
                print(f"Error guardando JSON: {e}")
                messagebox.showerror("ERROR",f"Error al guardar el archivo: {e}")

            finally:
                scrapingRunning=False



root=tk.Tk()
view=PrincipalView(root)
root.title("Scraping Libros")
root.geometry("1920x1080")
#root.resizable(0,0)
root.resizable(True, True)
root.configure(bg = "#c5eaf0")
root.mainloop()