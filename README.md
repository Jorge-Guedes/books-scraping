#### **TECH**
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## 🌐 Language / Idioma

- **[English](README.md)** | **[Español](README.es.md)**

---

# Book Scraping - Quelibroleo
Desktop application for scraping book information from the Quelibroleo.com website. Includes three different versions: a command-line version for general scraping, another specialized in literary news, and a complete graphical interface developed with Tkinter.

## Project Description
The project is organized into three main modules:

- **app_console**: Command-line version for general book scraping by literary genres. Allows extracting book information based on specific categories.

- **get_news**: Specialized version for obtaining literary news. Focuses on books recently added or updated on the platform.

- **app_tkinter**: Complete version with graphical interface that integrates all functionalities from previous versions into a desktop application with an intuitive interface.

Each module automatically creates a **Libros_json** folder where scraping results are stored in JSON format.

## Prerequisites
### pip Installation
Python generally includes pip by default in recent versions. To verify if pip is installed:

```bash
python -m pip --version
```

If not installed, follow the instructions according to your operating system:

- **Ubuntu/Debian**:
  ```bash
  sudo apt update  
  sudo apt install python3-pip
  ```

- **Windows**:  
  - Download the official Python installer from python.org, which includes pip by default.

### System Dependencies for Tkinter
- **Ubuntu/Debian**:  
  ```bash
  sudo apt update  
  sudo apt install python3-tk
  ```

- **Windows**:  
  - Tkinter comes included with standard Python installations. To verify: 
  ```bash
  python -m tkinter
  ```

## Installation and Configuration
1. Clone or download the project to your local directory.

2. Create virtual environment (recommended):
    ```bash
    python3 -m venv venv
    ```  
3. Activate virtual environment:

   - **Linux/Mac**:
        ```bash
        source venv/bin/activate
        ```  


   - **Windows**:
        ```bash
        venv\Scripts\activate
        ```  

4. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```  


## Application Usage
### Console Version (General Scraping)
```bash
cd scraping_console 
python3 app_console.py
``` 

### Literary News Version
```bash
cd scraping_news  
python3 get_news.py
```
### Graphical Interface Version
```bash
cd scraping_tkinter  
python3 app_tkinter.py
```
**Important note**: The **Libros_json** folder is automatically created within each corresponding directory when scraping is run for the first time. No need to create it manually.

## Functionalities
### Key Features
- Scraping of different literary genres
- Three operation modes: "Top 50 by genre", "All books by genre" and "Top 50 of each genre"
- Updated literary news retrieval
- Graphical interface with visual parameter selection
- Real-time scraping progress tracking
- Automatic export to JSON format

### Data Extracted per Book
- Complete title and author
- Specific literary genre
- Edition year and ISBN
- Book rating
- Complete synopsis
- Cover image URL
- Direct link to the book on Quelibroleo

## Data Structure
Data is organized in JSON files with the following structure:

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

## Usage Considerations
### Technical Aspects
- The application includes delays between requests to avoid overloading the server
- Integrated error handling to continue scraping even if individual books fail
- URL and data validation before processing

### Ethical Considerations
- Educational use of web scraping
- Respect for Quelibroleo.com's terms of use
- Delay between requests to avoid server saturation
- Local data storage without commercial redistribution


## Technical Dependencies
- Python 3.6+: Required Python version
- requests: For HTTP requests
- beautifulsoup4: For HTML parsing
- tkinter: For graphical interface (Tkinter version)
- uuid: For unique identifier generation

## License and Usage
This project is developed for educational and learning purposes. Use must always respect the terms and conditions of the Quelibroleo.com website. It is recommended to use the application responsibly and ethically.
