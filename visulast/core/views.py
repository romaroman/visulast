import numpy as np
from datetime import datetime
import os

import pylast
import shapefile
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import figaspect
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex

from visulast.core import scrappers, models
from visulast.utils.helpers import get_logger, PROJ_PATH, SHAPE_FILE

logger = get_logger(__name__)

images_directory = f"{PROJ_PATH}out/images"
mpl.rc('image', cmap='Greys_r')
mpl.rcParams['text.antialiased'] = True


def get_colour_scale(data):
    cmin, cmax = 0, max(data.values(), key=lambda i: i)
    colors = {}
    cmap = plt.cm.RdPu

    for key, value in data.items():
        colors[key] = cmap(np.sqrt((value - cmin) / (cmax - cmin)))[:3]

    return colors


# TODO: implement saving image as numpy array without exceptions
def save_fig(path, fig, clean=True):
    directory = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            logger.warning('Path already exist, continuing...')
            pass
    if clean:
        plt.subplots_adjust(0, 0, 1, 1, 0, 0)
        for ax in fig.axes:
            ax.axis('off')
            ax.margins(0, 0)
            ax.xaxis.set_major_locator(plt.NullLocator())
            ax.yaxis.set_major_locator(plt.NullLocator())
    plt.savefig(path, pad_inches=0, bbox_inches='tight', dpi=150)
    logger.info(f'Saved figure to {path}')


def figure_to_image(plot):
    pass


def get_timestamp():
    return str(datetime.now()).replace(' ', '_')[:-7]


def shorten_label(label):
    if len(label) > 25:
        parts = label.split(' ')
        new_label = ''
        while len(new_label) < 20:
            new_label += parts.pop(0) + ' '
        return new_label + '...'
    else:
        return label


class GeneralView:

    @staticmethod
    def draw_world_map_matplotlib(data):
        fig = plt.figure(figsize=figaspect(0.5))
        ax = plt.Axes(fig, [0.025, 0, 0.95, 1])
        ax.set_axis_off()
        ax.set_xlim(-180, 180)
        ax.set_ylim(-60, 90)
        fig.add_axes(ax)
        shapes = shapefile.Reader(SHAPE_FILE, encodingErrors="replace")
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
                ax.add_patch(
                    Polygon(
                        points[parts[i]:] if i == len(parts) - 1 else points[parts[i]:parts[i + 1]],
                        facecolor=rgb2hex(color), edgecolor='k', linewidth=0.5
                    )
                )

        filename = f"{images_directory}/worldmaps/{get_timestamp()}.png"
        save_fig(filename, fig)
        return filename

    @staticmethod
    def draw_classic_eight(data):
        labels = []
        images = []
        for entity in data:
            images.append(scrappers.ImageScrapper.get_image_by_entity(entity))

            if type(entity.item) == pylast.Artist:
                label = entity.item.name
                t = 'artist'
            else:
                label = entity.item.title
                t = 'album'

            labels.append((label, entity.weight))

        plt.gca().set_axis_off()
        plt.margins(0, 0)
        fig, axs = plt.subplots(nrows=2, ncols=4, gridspec_kw={'wspace': 0, 'hspace': 0})
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, wspace=0, hspace=0)
        axs = axs.flatten()
        labels.reverse()
        for img, ax in zip(images, axs):
            ax.imshow(img, interpolation=None)
            ax.axis('off')

            if labels:
                label, weight = labels.pop()
                ax.text(10, 150, f"{label}\n{weight}", fontsize=9, color='white')

        filename = f"{images_directory}/classic/eight/{t}/{get_timestamp()}.png"
        save_fig(filename, fig)
        return filename

    @staticmethod
    def draw_entities_histogram(data):
        pass

    @staticmethod
    def draw_pie_chart(data, title):

        labels = [shorten_label(t[0]).capitalize() for t in data]
        weights = [t[1] for t in data]
        # explode = (0.1, 0, 0, 0, 0, 0, 0, 0)

        fig, ax = plt.subplots()
        _, _, texts = ax.pie(weights, labels=labels, autopct='%1.1f%%', startangle=50)
        ax.axis('equal')
        plt.setp(texts, size=8)
        ax.set_title('Pie chart weight representation of ' + title)

        filename = f"{images_directory}/charts/pie/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename

    @staticmethod
    def draw_horizontal_bar_chart(data, title):
        labels = [shorten_label(d[0]) for d in data]
        weights = [d[1] for d in data]

        plt.rcdefaults()
        fig, ax = plt.subplots()

        y_pos = np.arange(len(labels))

        ax.barh(y_pos, weights, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        for i, v in enumerate(weights):
            plt.text(v, i, " " + str(v), va='center')

        ax.axes.get_xaxis().set_visible(False)
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        ax.set_xlabel('Weight or playcount')
        ax.set_title('Bar chart weight representation of ' + title)

        filename = f"{images_directory}/charts/bar/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename
