import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.cm import get_cmap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
#   -- input --
from numpy.ma import arange

sf = shapefile.Reader("./shapefiles/world_countries_boundary_file_world_2002")
cns     = []
for nshp in range(Nshp):
    cns.append(recs[nshp][1])

cm    = get_cmap('Dark2')
cccol = cm(1.*arange(Nshp)/Nshp)
#   -- plot --
fig     = plt.figure()
ax      = fig.add_subplot(111)
for nshp in range(Nshp):
    ptchs   = []
    pts     = shapes[nshp].points
    prt     = shapes[nshp].parts
    par     = list(prt) + [pts.shape[0]]
    for pij in range(len(prt)):
     ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
    ax.add_collection(PatchCollection(ptchs,facecolor=cccol[nshp,:],edgecolor='k', linewidths=.1))
ax.set_xlim(-180,+180)
ax.set_ylim(-90,90)
fig.savefig('test.png')