import pandas as pd, geopy, certifi, ssl
from geopy.geocoders import Nominatim

# Generation of a csv file with the GPS coordinates of the cities.
adresse = ["Mont Saint Michel",
"Saint Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="geocodage")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
adresse_list = []
longitude_list = []
latitude_list = []
for x in adresse:
    print(x)
    try:
        longitude = geolocator.geocode(x).longitude
        latitude = geolocator.geocode(x).latitude
        adresse_list.append(x)
        longitude_list.append(longitude)
        latitude_list.append(latitude)
    except:
        print('Adresse non localisée : '+x)

output = pd.DataFrame({'adresse':adresse_list, 'longitude':longitude_list, 'latitude':latitude_list})

# saving the dataframe to a csv file
output.to_csv(rf'geolocalisation.csv', index=False, sep=';', encoding='utf-8')