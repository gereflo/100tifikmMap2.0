import time
import dumper
import folium
import branca
import os

from geopy import geocoders
from selenium.common.exceptions import NoSuchElementException
from colored import fg, bg, attr

highlight = fg(198)
ok = fg(34)
error = bg(1) + fg('white')
reset = attr('reset')


def placePoints(serchQuery, key):
    # Se debe de obtener una clave de Bing para este paso
    geolocator = geocoders.Bing(key)

    # address, (latitude, longitude) = geolocator.geocode("Weizmann Institute of Science")
    location = geolocator.geocode(serchQuery, timeout=10)
    # print(location.address)
    # print(location.latitude)
    # print(location.longitude)
    # print(location.raw)

    return [location.address, [location.latitude, location.longitude]]
    # return [serchQuery, [10, 20]]


def waiting(wait, mensaje=""):
    for i in range(wait + 1):
        idx = "Espere " + str(wait - i) + " " + mensaje
        # print('\r', idx, end='')
        print("'\r{0}".format(idx), end='')
        time.sleep(1)
    print("", "\r", end='')


def placesDisplay(place, abuscar, pais=False, retZero=False):
    contries = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica",
                "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas",
                "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan",
                "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil",
                "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi",
                "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad",
                "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo",
                "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire",
                "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
                "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
                "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France",
                "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon",
                "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe",
                "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands",
                "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia",
                "Iran (Islamic Republic of)", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
                "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of",
                "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia",
                "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
                "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
                "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico",
                "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat",
                "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles",
                "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island",
                "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
                "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion",
                "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
                "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
                "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)", "Slovenia",
                "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain",
                "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname",
                "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic",
                "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo",
                "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
                "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
                "Uk", "Usa",
                "United States", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu",
                "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)",
                "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

    # abuscar.extend(contries)

    respuesta = 0
    flag = True

    for palabra in abuscar:
        for element in place:
            e = element.lower().replace('.', '')
            p = palabra.lower()
            if e.find(p) != -1 and flag:
                element = ''.join([i for i in element if not i.isdigit()])
                element = element.strip()
                respuesta = element.replace('.', '')
                flag = False
            if e.capitalize() in contries and flag == False and pais == True:
                respuesta = respuesta + ', ' + e.capitalize()
                flag = 2

    if respuesta == 0:
        for palabra in contries:
            for element in place:
                e = element.lower().replace('.', '')
                p = palabra.lower()
                if e.find(p) != -1 and flag:
                    element = ''.join([i for i in element if not i.isdigit()])
                    # element = element.strip()
                    respuesta = palabra

    if respuesta == 0:
        return place

    return respuesta


def paginasDPapers(browser, pag):
    browser.get(pag)
    # table = browser.find_elements_by_class_name('docsum-content')
    try:
        table = browser.find_elements_by_class_name('docsum-title')
    except NoSuchElementException:
        return []
    # print("Papers en " + pag + " = " + str(len(table)))
    dataArticlesId = []
    for article in table:
        data = article.get_attribute('data-article-id')
        if data is not None:
            dataArticlesId.append(data)
    # dumper.dump(dataArticlesId)
    return dataArticlesId


def getAuthors(browser):
    authorsList = browser.find_element_by_class_name('authors-list')
    authors = authorsList.find_elements_by_class_name('full-name')
    authorsString = ""
    for author in authors:
        authorsString = authorsString + author.get_attribute('textContent') + ", "
    return authorsString


def getPlaces(browser, keyWords, paises):
    expandedAuthors = browser.find_element_by_id('expanded-authors')
    itemList = expandedAuthors.find_elements_by_css_selector('li')
    temporalPlaces = []
    for li in itemList:
        text = li.get_attribute('textContent').split(', ')
        place = placesDisplay(text, keyWords, paises)
        if isinstance(place, str):
            temporalPlaces.append(place)
        else:
            print(error, '#########Lugar no Identificado###########', place, reset)
    return temporalPlaces


def toMap(placesAcc):
    # creamos el mapa de nuevo para partir de 0

    # mi_mapa = folium.Map(width=700,height=500, location=(39.7, 2.2), zoom_start=8)
    mi_mapa = folium.Map(location=(39.890542, 0), zoom_start=2.5)

    for place in placesAcc:
        # print("Lugar: ", place.place)
        # print("Direccion: ", place.adress)
        # print("Latitud: ", place.latitude)
        # print("Longitud: ", place.longitude)
        html = "<h1>" + place.place + "</h1>"
        for principalPaper in place.papers:
            # print("--Paper Principal: ", principalPaper.title)
            # print("--Autores: ", principalPaper.authors)
            # print("--Link: ", principalPaper.link)
            html = html + "<div style='border: thin solid grey'>" \
                            "<h4>" \
                                "<a href='" + principalPaper.link+ "' target='_blank'>" \
                                    + principalPaper.title + \
                            "</a></h4><ul>"
            for simple in principalPaper.citedBy:
                for s in simple:
                    # print("-----", s.title)
                    # print("-----", s.authors)
                    # print("-----", s.link)
                    html = html + "<li><h5><a href='" + s.link + "' target='_blank'>" + s.title + "</a></h5></li>"
            html = html + "</ul></div><br>"
        # print("html: ", html)
        iframe = branca.element.IFrame(html=html, width=400, height=250)
        marcador = folium.Marker(
            location=(place.latitude, place.longitude),
            popup=folium.Popup(iframe, max_width=500),
            icon=folium.Icon(color="black")
        )
        marcador.add_to(mi_mapa)

    mi_mapa.save("mapa.html")
    os.system("mapa.html")


