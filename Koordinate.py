import pyproj
import numpy as np
from pyproj import Transformer

lat, lon = 45.15, 21.31667
lat_ca,lon_ca = 45.15, 21.31667
trans_GPS_to_XY = Transformer.from_crs(4326, 6316)
gps = (lat_ca,lon_ca) # centar  Ca
xy = trans_GPS_to_XY.transform(gps[0], gps[1])
print(xy)