import pandas
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def create_cmap(nlvls, fmap):
  start = 0
  stop = 1
  cmap = plt.get_cmap(fmap)
  cmap = np.array([cmap(x) for x in np.linspace(start, stop, nlvls)])
  return cmap

def get_marker_color(fireSize):
  fireSize = np.where(fireSize < 1.0, 1, fireSize)    # set values <1 equal  1
  mrkrSize = np.log10(fireSize)                       # Convert to Log scale

  mrkrAdj = 1.5 #3.0                                  #Amplification of marker size
  nlvls = 8
  fmap = 'YlOrRd'
  cmap = create_cmap(nlvls, fmap)                     # Get colormap

  if mrkrSize < 1.:
    mrkrColor = cmap[0:][0]
  elif mrkrSize < 2.:
    mrkrColor = cmap[1:][0]
  elif mrkrSize < 3.:
    mrkrColor = cmap[2:][0]
  elif mrkrSize < 4.:
    mrkrColor = cmap[3:][0]
  elif mrkrSize < 5.:
    mrkrColor = cmap[4:][0]
  elif mrkrSize < 6.:
    mrkrColor = cmap[5:][0]
  elif mrkrSize < 7.:
    mrkrColor = cmap[6:][0]
  else:
    mrkrColor = cmap[7:][0]

  return mrkrSize + mrkrAdj, mrkrColor

##########################################################
# Create the marker legend for the basemap plots
##########################################################
def createMarkers(df):
  print("in create markets")
  m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49, projection='lcc',lat_1=33,lat_2=45,lon_0=-95) 
  lons = np.array(df.LONGITUDE)
  lats = np.array(df.LATITUDE)
  x, y = m(lons, lats)

  fSizes = df.FIRE_SIZE

  x, y = m(lons, lats)

  print("got to here", str(fSizes))
  for i in fSizes:
    mrkrSize, mrkrColor = get_marker_color(i)
    szLabel = '>' + str(i) + ' acres'
    m.plot(x, y, marker='o', color=mrkrColor, markersize=mrkrSize, markeredgecolor=[.3, .3, .3],label=szLabel)
    plt.legend()#fontsize=16)#, weight='bold')
    if (i %100 == 0):
      print(str(i))

  print("out of loop")
  # Save plot
  iName = 'Plates\Marker_LEGEND2.png'
  print(iName)
  plt.savefig(iName, bbox_inches='tight', pad_inches=0.25)
  #plt.show()

filename = "Lightning_PP_01.csv"
data = pandas.read_csv(filename)
createMarkers(data)