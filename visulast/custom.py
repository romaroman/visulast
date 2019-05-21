from visulast.core import controllers
import matplotlib.pyplot as plt
from PIL import Image

controller = controllers.UserController('niedego', 1)
file = controller.scrobbles_world_map(10)
img = Image.open(file)
plt.imshow(img)
plt.show()