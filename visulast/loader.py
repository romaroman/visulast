import shapefile as shp

SHAPE_FILE = "../assets/shapefiles/worldmaps/small/ne_10m_admin_0_countries_lakes"
SHAPE_READING_FIELD = "countries"


def extract_countries():
    sf = shp.Reader(SHAPE_FILE, SHAPE_READING_FIELD)
    countries = list()
    for shape in list(sf.iterRecords()):
        country = shape[3]
        if country not in countries:
            countries.append(country)
    return countries


COUNTRIES = extract_countries()
