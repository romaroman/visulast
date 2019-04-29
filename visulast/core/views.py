import numpy as np
from datetime import datetime

import shapefile as shp
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex

from visulast.core import models
from visulast.utils.helpers import get_logger, PROJ_PATH, SHAPE_FILE

logger = get_logger(__name__)


def get_colour_scale(data):
    cmin, cmax = 0, max(data.values(), key=lambda i: i)
    colors = {}
    cmap = plt.cm.RdPu

    for key, value in data.items():
        colors[key] = cmap(np.sqrt((value - cmin) / (cmax - cmin)))[:3]

    return colors


class _View:
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def draw_world_map_basemap(self, data):
        pass

    def draw_histogram(self):
        pass

    def draw_piechart(self):
        pass


class UserView(_View):

    def __init__(self, name='noname'):
        super(UserView, self).__init__(name)

    def draw_world_map_matplotlib(self, data):
        fig = plt.figure(figsize=figaspect(0.5))
        ax = plt.Axes(fig, [0.025, 0, 0.95, 1])
        ax.set_axis_off()
        ax.set_xlim(-180, 180)
        ax.set_ylim(-60, 90)
        fig.add_axes(ax)
        shapes = shp.Reader(SHAPE_FILE, encodingErrors="replace")
        colours = get_colour_scale(data)

        for item in shapes.iterShapeRecords():
            country = item.record['SOVEREIGNT']
            if country in data.keys():
                color = colours[country]
            else:
                color = (1, 1, 1)

            points = item.shape.points
            parts = item.shape.parts
            for i in range(len(parts)):
                ax.add_patch(Polygon(
                    points[parts[i]:] if i == len(parts) - 1 else points[parts[i]:parts[i + 1]],
                    facecolor=rgb2hex(color), edgecolor='k', linewidth=0.5
                ))

        filename = '{}out/graphs/worldmaps/{}_{}.png'.format(
                    PROJ_PATH, self.name, str(datetime.now()).replace(' ', '_')[:-7])
        # plt.show()
        plt.savefig(filename, dpi=200)
        return filename


if __name__ == '__main__':
    logger.debug('drawing')
    a = UserView()
    D = {
        'Russia': 10,
        'China': 25,
        'United Kingdom': 50,
        'United States of America': 75,
        'Australia': 100
    }
    #a.draw_world_map_matplotlib(D)
    # print(a.get_colour_scale({'Russia' : 1, 'China' : 2}))
    m = models.UserModel(name='niedego', chat_id='1111')
    a.draw_world_map_matplotlib(m.get_for_all_countries(what='s', limit=2))
