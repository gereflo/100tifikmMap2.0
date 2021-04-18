import pickle
import sys

import dumper
import os
import functions
import pickle

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as OptionsF
from selenium.webdriver.edge.options import Options as OptionsE
from selenium.webdriver.chrome.options import Options as OptionsC
from selenium.webdriver.common.keys import Keys
from colored import fg, bg, attr


# ---------------------Clases---------------------------

class PaperData:

    def __init__(self, title, authors, link):
        self.title = title
        self.authors = authors
        self.link = link
        self.places = []
        self.citedBy = []

    def add_places(self, p):
        self.places.append(p)

    def add_citedBy(self, c):
        self.citedBy.append(c)


class Place:
    def __init__(self, place, adress, latitude, longitude):
        self.place = place
        self.adress = adress
        self.latitude = latitude
        self.longitude = longitude
        self.papers = []

    def add_paper(self, c):
        self.papers = c


class SimplePaper:
    def __init__(self, title, authors, link):
        self.title = title
        self.authors = authors
        self.link = link
        self.citedBy = []

    def add_citedBy(self, c):
        self.citedBy.append(c)


# -------------Entry Variables--------------------------

term = 'Garcia-Campos+MA'
# term = 'Hernández-Lemus E'
# term = '78547745441'
pubMed = 'https://pubmed.ncbi.nlm.nih.gov/'
engine = "Edge"
headless = False

# --------Global Variables-------

bingKey = "Ag7ceErbHJORhQmZYkcqitAhObbQo42dg_ucM65A7O0GBi6JTaKWVLMIgtP6mqV2"
# Las palabras clave sirven para encontrar el tipo de institucion en los papers
keyWords = ['University', 'Université', 'Universidad', 'Institute', 'Research', 'Laboratory', 'Academy', 'Facility',
            'Hospital', 'Center', 'Centre']
highlight = fg(198)
ok = fg(34)
ok2 = fg('blue')
error = bg(1) + fg('white')
reset = attr('reset')
globalPlacesList = []
objCitas = []

# --------------------------------Main--------------------------------
if __name__ == "__main__":

    try:
        f = open('Citados.pckl', 'rb')
        print("Se ha encontrado un pepinillo de papers guardado ¿Desea cargar pepinillo? S/N")
        load = input()
        if load == 'S' or load == 's':
            objCitas = pickle.load(f)
            globalPlacesList = pickle.load(f)
            f.close()
            print(highlight, "Pepinillo cargadon con exito!!!! :3", reset)
    except:
        print(highlight, "Pepinillo no encontrado ejecucion normal", reset)

    if len(objCitas) == 0:

        if engine == 'Firefox':
            firefox_options = OptionsF()
            if headless:
                firefox_options.add_argument("--headless")

            browser = webdriver.Firefox(executable_path=r"webdrivers\geckodriver.exe",
                                        options=firefox_options)
        elif engine == 'Chrome':
            chrome_options = OptionsC()
            if headless:
                chrome_options.add_argument("--headless")

            browser = webdriver.Chrome(executable_path=r"webdrivers\chromedriver.exe",
                                       options=chrome_options)
        elif engine == 'Edge':
            edge_options = OptionsE()
            if headless:
                print('Edge no puede correr en Headdles mode, Normal Mode')
            browser = webdriver.Edge(executable_path=r"webdrivers\msedgedriver.exe")

        else:
            print('Seleccionar un navegador: Firefox, Chrome, Edge')
            sys.exit("No browser Selected")

        browser.get(pubMed + "?term=" + term)
        # browser.maximize_window()

        print(browser.title)

        papers = []
        try:
            loadButton = browser.find_element_by_class_name('load-button')
            pages = loadButton.get_attribute('data-last-page')
            # print('paginas: ' + pages)
            pages = range(1, int(pages) + 1)
            currentlink = browser.current_url
            for page in pages:
                link = currentlink + '&page=' + str(page)
                tabla = functions.paginasDPapers(browser, link)
                papers = papers + tabla

        except NoSuchElementException:
            # print('Investigador con menos de 10 papers')
            currentlink = browser.current_url
            tabla = functions.paginasDPapers(browser, currentlink)
            papers = tabla


        except:
            print("Error inesperado")
            sys.exit(-1)

        print("Total de papers de " + term + " : " + str(len(papers)))

        for i, paperId in enumerate(papers):
            browser.get(pubMed + paperId)
            # Nombre del paper Principal
            paperTitle = browser.title
            paperTitle = paperTitle.replace(" - PubMed", "")
            print("\t" + str(i + 1) + " :" + paperTitle + ",  dataArticlesId: " + paperId)

            # Autores del paper principal
            authorsString = functions.getAuthors(browser)
            # print("Authors: ", authorsString)

            # Lugares del Paper Principal
            temporalPlaces = functions.getPlaces(browser, keyWords, False)
            try:
                temporalPlaces = list(set(temporalPlaces))
                # print(temporalPlaces)
                # Se agregan los nuevos lugares encontrados a la lista de de lugares Global para mostrar en el mapa
                # los papers que se generaron en ese lugar
                globalPlacesList = globalPlacesList + temporalPlaces
            except:
                print(error, 'Hay un elemento desconocido en la lista', reset)

            # Creando el objeto de paper principal
            principal = PaperData(paperTitle, authorsString, pubMed + paperId)

            for temporalPlace in temporalPlaces:
                principal.add_places(temporalPlace)

            # dumper.dump(principal)

            # --- Papers que citan al principal
            browser.get(pubMed + "?linkname=pubmed_pubmed_citedin&from_uid=" + paperId)
            citedByPapers = []
            try:
                loadButton = browser.find_element_by_class_name('load-button')
                pages = loadButton.get_attribute('data-last-page')
                pages = range(1, int(pages) + 1)
                currentlink = browser.current_url
                for page in pages:
                    link = currentlink + '&page=' + str(page)
                    tabla = functions.paginasDPapers(browser, link)
                    citedByPapers = citedByPapers + tabla
            except NoSuchElementException:
                currentlink = browser.current_url
                tabla = functions.paginasDPapers(browser, currentlink)
                citedByPapers = tabla

            print("\t\t Citas de " + paperId + " = " + str(len(citedByPapers)))

            for paperIdCited in citedByPapers:
                browser.get(pubMed + paperIdCited)
                # Nombre del paper que cita
                paperTitleC = browser.title
                paperTitleC = paperTitleC.replace(" - PubMed", "")
                # print("\t" + str(i + 1) + " :" + paperTitle + ",  dataArticlesId: " + paperId)

                # Autores del paper que cita
                authorsStringC = functions.getAuthors(browser)
                # print("Authors: ", authorsString)

                # Lugares del Paper Principal
                temporalPlacesC = functions.getPlaces(browser, keyWords, False)
                try:
                    temporalPlacesC = list(set(temporalPlacesC))
                    # Se agregan los nuevos lugares encontrados a la lista de de lugares Global para mostrar en el mapa
                    # los papers que se generaron en ese lugar
                    globalPlacesList = globalPlacesList + temporalPlacesC
                except:
                    print(error, 'Hay un elemento desconocido en la lista', reset)

                citedBy = PaperData(paperTitleC, authorsStringC, pubMed + paperIdCited)

                for temporalPlace in temporalPlacesC:
                    citedBy.add_places(temporalPlace)

                principal.add_citedBy(citedBy)

            # print('Dumping principal')
            # dumper.dump(principal)
            objCitas.append(principal)

        browser.quit()
        print('---------------------------------Haciendo el pepinillo de papers----------------------------------------')
        print("Objcitas = ", str(len(objCitas)))
        f = open(r"Citados.pckl", 'wb')
        pickle.dump(objCitas, f)
        globalPlacesList = list(set(globalPlacesList))
        pickle.dump(globalPlacesList, f)
        f.close()

    # dumper.dump(objCitas)
    globalPlacesList = list(set(globalPlacesList))
    globalPlacesList = sorted(globalPlacesList)
    # dumper.dump(globalPlacesList)

    # ------------------------------Second Step---------------------------------
    placesAcc = []

    try:
        f = open('Places.pckl', 'rb')
        print("Se ha encontrado un pepinillo de Coordenadas guardado ¿Desea cargar pepinillo? S/N")
        load = input()
        if load == 'S' or load == 's':
            placesAcc = pickle.load(f)
            f.close()
            print(highlight, "Pepinillo cargadon con exito!!!! :3", reset)
    except:
        print(highlight, "Pepinillo no encontrado ejecucion normal 2", reset)

    if len(placesAcc) == 0:
        for place in globalPlacesList:
            try:
                points = functions.placePoints(place, bingKey)
                place = Place(place, points[0], points[1][0], points[1][1])
                placesAcc.append(place)
                dumper.dump(place)
            except:
                print(error, "Something went wrong", reset)
                continue

        print('---------------------------------Hciendo el pepinillo Places------------------------')
        f = open(r"Places.pckl", 'wb')
        pickle.dump(placesAcc, f)
        f.close()
    # dumper.dump(placesAcc)

    # ----------------------------Third Step --------------------------------------

    for place in placesAcc:  # Lugares donde se cito
        # print(ok, "-", place.place, reset)
        # print(ok, "-", place.longitude, reset)
        # print(ok, "-", place.latitude, reset)
        # Algo muy complicado y enredoso aqui
        cit = []
        place.add_paper(cit)
        for obj in objCitas:
            paperscitados = []
            for cited in obj.citedBy:
                for placeCited in cited.places:
                    if placeCited == place.place:
                        paperscitados.append(cited)
            # Resultado
            if len(paperscitados) != 0:
                # Paper que se cita
                # print(ok2, "---", obj.title, reset)
                # print(ok2, "---", obj.authors, reset)
                # print(ok2, "---", obj.link, reset)
                cita2 = []
                ci = SimplePaper(obj.title, obj.authors, obj.link)
                ci.add_citedBy(cita2)
                cit.append(ci)
                for p in paperscitados:
                    # Papers que citaron el Paper en cierto lugar
                    # print("--------", p.title)
                    # print("--------", p.authors)
                    # print("--------", p.link)
                    c = SimplePaper(p.title, p.authors, p.link)
                    cita2.append(c)

    # dumper.max_depth = 10
    # dumper.dump(placesAcc)
    # -----------Step Four------ Create a map ---------------------------
    functions.toMap(placesAcc)