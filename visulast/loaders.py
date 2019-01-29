import shapefile as shp

from utils import get_logger, PROJ_PATH

logger = get_logger(__name__)

SHAPE_FILE = PROJ_PATH + "assets/shapefiles/worldmaps/small/ne_110m_admin_0_countries_lakes"