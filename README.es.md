#### **TECH**
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## 🌐 Idioma / Language

-  **[Español](README.es.md)** | **[English](README.md)**

---


# Scraping de Libros - Quelibroleo
Aplicación de escritorio para realizar scraping de información de libros desde el sitio web Quelibroleo.com. Incluye tres versiones diferentes: una de línea de comandos para scraping general, otra especializada en novedades literarias, y una interfaz gráfica completa desarrollada con Tkinter.

## Descripción del Proyecto
El proyecto está organizado en tres módulos principales:

- **app_console**: Versión de línea de comandos para scraping general de libros por géneros literarios. Permite extraer información de libros basándose en categorías específicas.

- **get_news**: Versión especializada en la obtención de novedades literarias. Se enfoca en libros recientemente añadidos o actualizados en la plataforma.

- **app_tkinter**: Versión completa con interfaz gráfica que integra todas las funcionalidades de las versiones anteriores en una aplicación de escritorio con interfaz intuitiva.

Cada módulo genera automáticamente una carpeta **Libros_json** donde se almacenan los resultados del scraping en formato JSON.

## Requisitos Previos
### Instalación de pip
Python generalmente incluye pip por defecto en las versiones recientes. Para verificar si pip está instalado:

```bash
python -m pip --version
```

Si no está instalado, seguir las instrucciones según el sistema operativo:

- **Ubuntu/Debian**:
  ```bash
  sudo apt update  
  sudo apt install python3-pip
  ```

- **Windows**:  
  - Descargar el instalador oficial de Python desde python.org, que incluye pip por defecto.

### Dependencias del sistema para Tkinter
- **Ubuntu/Debian**:  
  ```bash
  sudo apt update  
  sudo apt install python3-tk
  ```

- **Windows**:  
  - Tkinter viene incluido con las instalaciones estándar de Python. Para verificar:  
  ```bash
  python -m tkinter
  ```

## Instalación y Configuración
1. Clonar o descargar el proyecto en el directorio local.

2. Crear entorno virtual (recomendado):
    ```bash
    python3 -m venv venv
    ```  
3. Activar entorno virtual:

   - **Linux/Mac**:
        ```bash
        source venv/bin/activate
        ```  


   - **Windows**:
        ```bash
        venv\Scripts\activate
        ```  

4. Instalar dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```  


## Uso de la Aplicación
### Versión de Consola (Scraping General)
```bash
cd scraping_console 
python3 app_console.py
``` 

### Versión de Novedades Literarias
```bash
cd scraping_news  
python3 get_news.py
```
### Versión con Interfaz Gráfica
```bash
cd scraping_tkinter  
python3 app_tkinter.py
```
**Nota importante**: La carpeta **Libros_json** se crea automáticamente dentro de cada directorio correspondiente cuando se ejecuta el scraping por primera vez. No es necesario crearla manualmente.

## Funcionalidades
### Características Principales
- Scraping de diferentes géneros literarios
- Tres modos de operación: "Top 50 por género", "Todos los líbros por género" y "Top 50 de cada género"
- Obtención de novedades literarias actualizadas
- Interfaz gráfica con selección visual de parámetros
- Progreso en tiempo real del proceso de scraping
- Exportación automática a formato JSON

### Datos Extraídos por Libro
- Título completo y autor
- Género literario específico
- Año de edición e ISBN
- Calificación (rating) del libro
- Sinopsis completa
- URL de la imagen de portada
- Enlace directo al libro en Quelibroleo

## Estructura de Datos
Los datos se organizan en archivos JSON con la siguiente estructura:

```json
{
  "id": "uuid-unico",
  "title": "Título del libro",
  "author": "Autor del libro",
  "cover_image": "URL de la portada",
  "genre": "Género literario",
  "year_edition": "Año de edición",
  "isbn": "ISBN del libro",
  "rating": "Calificación",
  "synopsis": "Sinopsis completa",
  "url_book": "URL del libro en Quelibroleo"
}
```

## Consideraciones de Uso
### Aspectos Técnicos
- La aplicación incluye delays entre peticiones para evitar sobrecargar el servidor
- Manejo de errores integrado para continuar el scraping aunque falle algún libro individual
- Validación de URLs y datos antes del procesamiento

### Consideraciones Éticas
- Uso educativo del scraping web
- Respeto de los términos de uso de Quelibroleo.com
- Delay entre peticiones para no saturar el servidor
- Almacenamiento local de datos sin redistribución comercial


## Dependencias Técnicas
- Python 3.6+: Versión de Python requerida
- requests: Para peticiones HTTP
- beautifulsoup4: Para parsing de HTML
- tkinter: Para la interfaz gráfica (versión Tkinter)
- uuid: Para generación de identificadores únicos

## Licencia y Uso
Este proyecto está desarrollado con fines educativos y de aprendizaje. El uso debe realizarse respetando siempre los términos y condiciones del sitio web Quelibroleo.com. Se recomienda utilizar la aplicación de forma responsable y ética.
