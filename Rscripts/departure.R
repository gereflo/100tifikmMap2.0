library(tidygeocoder)
library(dplyr)
library(tibble)
library(ggplot2)
library(maps)
library(ggrepel)


some_addresses <- tribble(
    ~name,                  ~addr,
    "Mi casa",          "Prolongacion abasolo 242, Actopan, Hidalgo",
    "Una torre",          "La torre de Pisa, Italia",
    "Una pirámide",          "Chichen Itza",
    "Weizmann", "Weizmann Institute of Science",     
    "UNAM",         "Universidad Nacional Autónoma de Mexico, Ciudad de Mexico"                                  
)
lat_longs <- geocode(some_addresses, addr, method = 'arcgis', lat = latitude , long = longitude)
ggplot(lat_longs, aes(longitude, latitude), color = "grey99") +
    borders("world") + geom_point() +
    geom_label_repel(aes(label = name)) +
    theme_void()
reverse <- lat_longs %>%
    reverse_geocode(lat = latitude, long = longitude, method = 'arcgis',
                    address = address_found, full_results = TRUE) %>% t()

######################################################################################



