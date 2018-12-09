import shapely
import matplotlib.Basemap


def extract_countries():
    sf = shp.Reader(SHAPE_FILE, SHAPE_READING_FIELD)
    countries = list()
    for shape in list(sf.iterRecords()):
        country = shape[3]
        if country not in countries:
            countries.append(country)
    return countries
