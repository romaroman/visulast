import numpy as np
from datetime import datetime
import os
import random
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

images_directory = f"{PROJ_PATH}images"
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


def figure_to_image(fig):
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
    def draw_world_map(data):
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

        filename = f"{images_directory}/world_map/{get_timestamp()}.png"
        save_fig(filename, fig)
        return filename

    @staticmethod
    def draw_classic_eight_graph(data):
        labels = []
        images = []
        for entity in data:
            images.append(scrappers.ImageScrapper.get_image_by_entity(entity))

            if type(entity.item) == pylast.Artist:
                label = entity.item.name
            else:
                label = entity.item.title

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

        filename = f"{images_directory}/classic_eight/{get_timestamp()}.png"
        save_fig(filename, fig)
        return filename

    @staticmethod
    def draw_pie_graph(data, title):
        random.shuffle(data)
        labels = [shorten_label(t[0]) for t in data]
        weights = [t[1] for t in data]
        # explode = (0.1, 0, 0, 0, 0, 0, 0, 0)

        fig, ax = plt.subplots()
        _, _, texts = ax.pie(weights, labels=labels, autopct='%1.1f%%', startangle=50)
        ax.axis('equal')
        plt.setp(texts, size=8)
        ax.set_title('Pie graph weight representation of ' + title)

        filename = f"{images_directory}/pie/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename

    @staticmethod
    def draw_horizontal_bar_graph(data, title):

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
        ax.set_title('Bar graph weight representation of ' + title)

        filename = f"{images_directory}/horizontal_bar/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename

    @staticmethod
    def draw_heat_map(data):
        tags = []
        friends = []
        for friend, info in data:
            friends.append(friend)
            for tag, value in info:
                if tag not in tags:
                    tags.append(tag)

        map = np.zeros((len(friends), len(tags)))
        i = 0
        for friend, info in data:
            j = 0
            for tag in tags:
                for c_tag in info:
                    if c_tag[0] == tag:
                        map[i][j] += c_tag[1]
                        break
                j += 1
            i += 1

        filename = f"{images_directory}/heat_map/_{get_timestamp()}.png"
        # save_fig(filename, fig, clean=False)
        return filename

    @staticmethod
    def heatmap(data, row_labels, col_labels):
        data = np.array([[3., 3., 3., 3., 2., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 0.],
                      [2., 2., 2., 0., 0., 0., 0., 0., 2., 2., 1., 1., 1., 0., 0., 0.,
                       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 0.],
                      [0., 2., 2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3., 3., 3.,
                       2., 2., 2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 0.],
                      [1., 1., 2., 0., 0., 0., 0., 0., 0., 3., 0., 0., 0., 0., 0., 0.,
                       0., 0., 0., 2., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 0.],
                      [4., 5., 3., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3., 0., 0., 0.,
                       0., 0., 0., 0., 0., 0., 0., 3., 1., 1., 1., 0., 0., 0., 0., 0.,
                       0., 0.],
                      [0., 0., 2., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.,
                       0., 0., 0., 1., 1., 2., 0., 0., 0., 0., 0., 2., 2., 2., 0., 0.,
                       0., 0.],
                      [2., 3., 2., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       0., 2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3., 0., 0., 2., 2.,
                       0., 0.],
                      [0., 2., 2., 0., 2., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1.,
                       1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                       2., 2.]])
        col_labels = ['ambient',
                'electronic',
                'experimental',
                'dark ambient',
                'new wave',
                'shoegaze',
                'trip-hop',
                'post-rock',
                'dubstep',
                'hip-hop',
                'future garage',
                '2-step',
                'electronica',
                'screamo',
                'hardcore',
                'emo',
                'post-hardcore',
                'seen live',
                'real screamo',
                'cloud rap',
                'rap',
                'russian',
                'underground hip-hop',
                'idm',
                'chillout',
                'drone',
                'psychedelic',
                'post-punk',
                'lo-fi',
                'indie',
                'noise rock',
                'noise',
                '80s',
                'industrial']
        row_labels = ['Florian_y',
                   'Hey_Canada',
                   'Mr_Belldom',
                   'ToughGuy4x4',
                   'holkabobra',
                   'MamaObama',
                   'rettside',
                   'Last_August']

        cbarlabel = "harvest [t/year]"
        ax = plt.gca()

        # Plot the heatmap
        im = ax.imshow(data, cmap="YlGn")

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, cmap="YlGn")
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-90, ha="right",
                 rotation_mode="anchor")

        # Turn spines off and create white grid.
        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        # ax.grid(which="minor", color="b", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        plt.show()
        filename = f"{images_directory}/heat_map/_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename
        return im, cbar

    @staticmethod
    def draw_stacked_bar_graph(data, title):
        fig, ax = plt.subplots()

        filename = f"{images_directory}/stacked_bar/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename

    @staticmethod
    def _template(data, title):
        fig, ax = plt.subplots()

        filename = f"{images_directory}/stacked_bar/{title}_{get_timestamp()}.png"
        save_fig(filename, fig, clean=False)
        return filename


if __name__ == '__main__':
    # GeneralView.draw_heat_map(models.UserModel('niedego').get_compatibility_by_friends_and_tags(friends_limit=8, tags_limit=8))

    GeneralView.heatmap(0,0,0)