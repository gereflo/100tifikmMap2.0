import pickle
import dumper
import os

# # Creamos una clase de prueba
# class Persona:
#
#     def __init__(self, nombre, apellido):
#         self.nombre = nombre
#         self.apellido = apellido
#
#     def __str__(self):
#         return self.nombre + self.apellido
#
#
# # Creamos la lista con los objetos
# personas = []
#
# persona1 = Persona("Aaron", "parez")
# persona2 = Persona("fernande", "parez")
# persona3 = Persona("Carola", "parez")
#
# personas.append(persona1)
# personas.append(persona2)
# personas.append(persona3)
#
# # Escribimos la lista en el fichero con pickle
# import pickle
# f = open(r"personas2.pckl", 'wb')
# pickle.dump(personas, f)
# f.close()
#
# # Leemos la lista del fichero con pickle
# f = open('personas2.pckl', 'rb')
# personas = pickle.load(f)
# f.close()
#
# dumper.dump(personas)
#
# for p in personas:
#     print(p)


#https://pybonacci.org/2017/09/07/como-crear-un-mapa-interactivo-con-folium/
import folium
import branca

# creamos el mapa de nuevo para partir de 0
# mi_mapa = folium.Map(width=700,height=500, location=(39.7, 2.2), zoom_start=8)
mi_mapa = folium.Map(location=(39.890542, 0), zoom_start=2.5)
# La información de los popups la añadiremos usando branca
# La información solo será la posición del marcador
# os dejo a vosotros la innovación
html = "<p>Latitud: 40.0</p><br><br><br><br><br><br><br><br><br><br><br><p>Longitud: 2.1</p>"
iframe1 = branca.element.IFrame(html=html, width=300, height=200)
html = "<p>Latitud: 40.0</p><p>Longitud: 3.5</p>"
iframe2 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 2.1</p>"
iframe3 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 3.5</p>"
iframe4 = branca.element.IFrame(html=html, width=500, height=300)
# creamos 4 marcadores y añadimos la información del popup usando folium.Popup
# además, añadimos un icono que será de un color para los marcadores al este
# y de otro color para los marcadores del oeste.
marcador1 = folium.Marker(
    location=(40, 2.1),
    popup=folium.Popup(iframe1, max_width=500),
    icon=folium.Icon(color="purple")
)
marcador2 = folium.Marker(
    location=(40, 3.5),
    popup=folium.Popup(iframe2, max_width=500),
    icon=folium.Icon(color="gray", icon="glyphicon-star")
)
marcador3 = folium.Marker(
    location=(39, 2.1),
    popup=folium.Popup(iframe3, max_width=500),
    icon=folium.Icon(color="black",icon="apple", prefix='fa')
)
marcador4 = folium.Marker(
    location=(39, 3.5),
    popup=folium.Popup(iframe4, max_width=500),
    icon=folium.Icon(color="gray")
)
# Creamos dos grupos para los marcadores
grp_este = folium.FeatureGroup(name='Estessssssssssssssssssssssssssssssssssssssssssssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
grp_oeste = folium.FeatureGroup(name='Oeste')
# Añadimos los marcadores AL GRUPO AL QUE CORRESPONDAN (NO AL MAPA)
marcador1.add_to(grp_oeste)
marcador2.add_to(grp_este)
marcador3.add_to(grp_oeste)
marcador4.add_to(grp_este)
# Y ahora añadimos los grupos al mapa
grp_este.add_to(mi_mapa)
grp_oeste.add_to(mi_mapa)
# Y añadimos, además, el control de capas
folium.LayerControl().add_to(mi_mapa)
# Y guardamos el mapa
mi_mapa.save("mapa.html")
os.system("mapa.html")

# from difflib import SequenceMatcher as SM
#
# s1 = 'Autonomous University of Mexico City'
# s2 = 'Universidad Nacional Autónoma de Mexico'
# print(SM(None, s1, s2).ratio())
#
# s2 = 'Universidad Nacional Autónoma de México Ciudad de México'
# print(SM(None, s1, s2).ratio())

