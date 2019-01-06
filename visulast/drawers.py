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

from loaders import SHAPE_FILE, SHAPE_READING_FIELD


class Drawer:
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def draw_histogram(self):
        pass


class ArtistDrawer(Drawer):

    @staticmethod
    def draw_countries(countries, user):
        m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90,
                    llcrnrlon=-180, urcrnrlon=180, resolution='c')
        fig, ax = plt.subplots()
        m.readshapefile(SHAPE_FILE, SHAPE_READING_FIELD)

        vmin, vmax = 0, max(countries.values(), key=lambda i: i)
        norm = Normalize(vmin=vmin, vmax=vmax)
        colors = {}
        cmap = plt.cm.cool_r
        coloured_countries = list()

        for shapedict in m.countries_info:
            statename = shapedict['SOVEREIGNT']
            if statename not in coloured_countries and statename in countries.keys():
                comp = countries[statename]
                colors[statename] = cmap(np.sqrt((comp - vmin) / (vmax - vmin)))[:3]
                coloured_countries.append(statename)

        for seg, info in zip(m.countries, m.countries_info):
            if info['SOVEREIGNT'] in countries.keys():
                color = rgb2hex(colors[info['SOVEREIGNT']])
                poly = Polygon(seg, facecolor=color)
                ax.add_patch(poly)

        plt.title('Map of {}\'s most listened countries'.format(user))

        ax_c = fig.add_axes([0.2, 0.1, 0.6, 0.03])
        cb = ColorbarBase(ax_c, cmap=cmap, norm=norm, orientation='horizontal',
                          label=r'[number of scrobbles per country]')

        # plt.show()
        filename = '../out/plots/worldmaps/' + user + '_' + str(datetime.now().time())[:8] + '.png'
        plt.savefig(filename, dpi=800)
        return filename


if __name__ == '__main__':
    countries = {
        'Russia' : 100,
        'Germany': 40,
        'China': 20,
        'Japan': 5
    }
    ArtistDrawer.draw_countries(countries, 'niedego')
