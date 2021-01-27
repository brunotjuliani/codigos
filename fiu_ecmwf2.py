import os
import numpy as np
import pandas as pd
import geopandas as gpd

area = gpd.read_file('../Teste/Fiu_area.gpkg')
minx = area.bounds.minx
maxx = area.bounds.maxx
miny = area.bounds.miny
maxy = area.bounds.maxy
