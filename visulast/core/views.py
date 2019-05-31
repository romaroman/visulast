import numpy as np
from datetime import datetime
import os

import shapefile as shp
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import figaspect
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex

from visulast.core import scrappers
from visulast.core import models
from visulast.utils.helpers import get_logger, PROJ_PATH, SHAPE_FILE

logger = get_logger(__name__)

images_directory = f"{PROJ_PATH}out/images"
mpl.rc('image', cmap='Greys_r')
mpl.rcParams['text.antialiased'] = False


def get_colour_scale(data):
    cmin, cmax = 0, max(data.values(), key=lambda i: i)
    colors = {}
    cmap = plt.cm.RdPu

    for key, value in data.items():
        colors[key] = cmap(np.sqrt((value - cmin) / (cmax - cmin)))[:3]

    return colors


# TODO: implement saving image as numpy array without exceptions
def save_image(path, image):
    directory = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            logger.warning('Path already exist, continuing...')
            pass

    # cv.imwrite(f'{path}.{ext}', image, [int(cv.IMWRITE_PNG_COMPRESSION), 0])


def get_timestamp():
    return str(datetime.now()).replace(' ', '_')[:-7]


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
    def __init__(self, username):
        self.username = username
        super(UserView, self).__init__(self)

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

        filename = f"{images_directory}/worldmaps/{self.username}_{get_timestamp()}.png"

        if not os.path.exists(images_directory):
            os.makedirs(images_directory)
        plt.savefig(filename, dpi=200)

        return filename

    def draw_classic_eight(self, data):
        labels = []
        images = []
        for i in data:
            images.append(scrappers.ImageScrapper.getAristImage(i.item.name))
            labels.append((i.item.name, i.weight))

        filename = f"{images_directory}/classic/eight/artists/{self.username}_{get_timestamp()}"

        fig, axs = plt.subplots(nrows=2, ncols=4, gridspec_kw={'wspace': 0, 'hspace': 0})
        fig.subplots_adjust(wspace=0, hspace=0)
        axs = axs.flatten()
        labels.reverse()
        for img, ax in zip(images, axs):
            ax.imshow(img, interpolation=None)
            ax.axis('off')

            if labels:
                name, weight = labels.pop()
                ax.text(10, 150, f"{name}\n{weight}", fontsize=12, color='white')

        fig.canvas.draw()
        res_img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        res_img = res_img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.imshow(res_img)
        plt.show()
        pass


if __name__ == '__main__':
    v = UserView('niedego')
    m = models.UserModel('niedego', '1231')
    v.draw_classic_eight(m.get_classic_eight_artists("overall"))
