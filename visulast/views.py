import numpy as np
from datetime import datetime

import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize, rgb2hex

from logger import get_logger
from loaders import SHAPE_FILE, SHAPE_READING_FIELD
from scrappers import CountryOfArtistScrapper


logger = get_logger(os.path.basename(__file__))


class _View:
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def draw_world_map(self, data):
        pass

    def draw_histogram(self):
        pass

    def draw_piechart(self):
        pass


class UserView(_View):

    def __init__(self, name):
        super(UserView, self).__init__(name)

    def draw_world_map(self, data):
        """
        :param data: dictionary with scrobble info of user's lib
                          example : {'Russia': 200, 'Japan': 100}
        :return path of saved .png plot
        """
        m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90,
                    llcrnrlon=-180, urcrnrlon=180, resolution='c')
        fig, ax = plt.subplots()
        m.readshapefile(SHAPE_FILE, SHAPE_READING_FIELD)

        vmin, vmax = 0, max(data.values(), key=lambda i: i)
        norm = Normalize(vmin=vmin, vmax=vmax)
        colors = {}
        cmap = plt.cm.cool_r
        coloured_countries = list()

        for shapedict in m.countries_info:
            statename = shapedict['SOVEREIGNT']
            if statename not in coloured_countries and statename in data.keys():
                comp = data[statename]
                colors[statename] = cmap(np.sqrt((comp - vmin) / (vmax - vmin)))[:3]
                coloured_countries.append(statename)

        for seg, info in zip(m.countries, m.countries_info):
            if info['SOVEREIGNT'] in data.keys():
                color = rgb2hex(colors[info['SOVEREIGNT']])
                poly = Polygon(seg, facecolor=color)
                ax.add_patch(poly)

        plt.title('Map of {}\'s most listened countries'.format(self.name))

        ax_c = fig.add_axes([0.2, 0.1, 0.6, 0.03])
        cb = ColorbarBase(ax_c, cmap=cmap, norm=norm, orientation='horizontal',
                          label=r'[number of scrobbles per country]')

        filename = '../out/plots/worldmaps/' + self.name + '_' + str(datetime.now().time())[:8] + '.png'
        plt.savefig(filename, dpi=200)
        return filename


class UserView1(_View):
    pass


if __name__ == '__main__':
    logger.debug('drawing')
    # UserView.draw_countries(CountryOfArtistScrapper.get_all_scrobbles_by_username('niedego', 1), 'niedego')