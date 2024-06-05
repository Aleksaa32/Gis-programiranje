from shapely.geometry import Point
import geopandas as gpd
from fiona.crs import from_epsg
import matplotlib.pyplot as plt

# Ubacivanje lokacija stanica (tacke)-koordinata
t_1 = Point(7459007, 5078536)
t_2 = Point(7405071, 5106920)
t_3 = Point(7356492, 5068945)
t_4 = Point(7452151, 5028572)
t_5 = Point(7410292, 5021621)
t_6 = Point(7354621, 4987452)
t_7 = Point(7525331, 5000657)

# Kreiranje liste
lista = [((t_1, "Kikinda")), ((t_2, "Palic")), ((t_3, "Sombor")), ((t_4, "Zrenjanin")),
         ((t_5, "Rimski_sancevi")), ((t_6, "Sid")), ((t_7, "Vrsac"))]

# Kreiranje GeoDataFrame
prostor= gpd.GeoDataFrame()
prostor['geometry'] = None

for ID, (stanica, naziv) in enumerate(lista):
    prostor.loc[ID, 'geometry'] = stanica
    prostor.loc[ID, 'Naziv tacke'] = naziv

# Podešavanje koordinatnog sistema i prikazivanje tačaka
prostor.crs = from_epsg(6316)
prostor.plot(facecolor='red')
plt.title("Meteorološke stanice")
plt.show()

#  Kreiranje novog shp file-a Stanice
out_file = "C:/Users/Administrator/Documents/FAKULTET/GIS Master/GIS PROGRAMIRANJE/projekat/Stanice"
prostor.to_file(out_file)

# Ubacivanje shp file-a sa granicama opština Vojvodine
fp = "C:/Users/Administrator/Documents/FAKULTET/GIS Master/GIS PROGRAMIRANJE/projekat/Vojvodina Opstine/Vojvodina Opstine.shp"

# Čitanje fajla
prostor_poly = gpd.read_file(fp)
print(prostor_poly)
print(prostor_poly.crs)
print(prostor_poly['geometry'].head())

# Preimenovanje atributa
prostor_poly = prostor_poly.rename(columns={'Opstina': 'Naziv opstine'})
print(prostor_poly.columns)
print(prostor_poly)

# Dodat novi atribut površina za svaki red
prostor_poly['Povrsina'] = prostor_poly['geometry'].area / 1000000
print(prostor_poly['Povrsina'].head())
print("Povrsine su jednake (km2):", prostor_poly)

prostor_poly.crs = from_epsg(6316)
print(prostor_poly.crs)

# Prikazivanje karte Vojvodine
prostor_poly.plot(column='Naziv opstine', cmap='tab10', legend=False)
plt.title('Opštine AP Vojvodina')
plt.tight_layout()
plt.show()

# Kreiranje novog shp file-a sa granicom opština Vojvodine i proračunatim površinama
out_file2 = "C:/Users/Administrator/Documents/FAKULTET/GIS Master/GIS PROGRAMIRANJE/projekat/Vojvodina Opstine 2"
prostor_poly.to_file(out_file2)

print(prostor.crs)
print(prostor_poly.crs)

# Spajanje tačaka meteoroloških stanica sa opštinama i prikazivanje rezultata na karti
prostor.to_crs(prostor_poly.crs, inplace=True)
preklapanje = prostor.geometry._append(prostor_poly.geometry)
print(preklapanje.crs)
print(preklapanje)

preklapanje.plot(cmap="Pastel1")
plt.title("Meteorološke stanice na teritoriji AP Vojvodina")
plt.show()
