import pandas
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

##########################################################
#nlvls - # of discrete levels to create
#fmap = colormap to use to create the cmap
##########################################################
def create_cmap(nlvls, fmap):
  start = 0
  stop = 1
  cmap = plt.get_cmap(fmap)
  cmap = np.array([cmap(x) for x in np.linspace(start, stop, nlvls)])
  return cmap

def get_marker_color(fireSize):
  fireSize = np.where(fireSize < 1.0, 1, fireSize)  	# set values <1 equal  1
  mrkrSize = np.log10(fireSize)                     	# Convert to Log scale

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

filename = "Human_PP_01.csv"
# filename = "Lightning_PP_01.csv"

data = pandas.read_csv(filename)

for year in range(1992,2000):
	currentYear = data.loc[data['FIRE_YEAR'] == year]
	for month in range(1,13):
		# Pulled this code from Basemap Examples on Github
		m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49, projection='lcc',lat_1=33,lat_2=45,lon_0=-95) 
		shp_info = m.readshapefile('st99_d00','states',drawbounds=True)

		currentMonth = currentYear.loc[currentYear['FIRE_MONTH'] == month]
		# print(currentMonth)
		# tempdata = currentMonth.sample(n=5)
		for i in currentMonth.itertuples():
			lat = i[5]
			lon = i[6]
			x, y = m(lon,lat)
			# determine the size of the circle and color
			size, markerColor = get_marker_color(i[4])
			# print(get_marker_color(i[4]))
			m.plot(x, y, marker = "o", color= markerColor, markersize=size)	

		plt.title('Human Fires on: ' + monthDict[month]+ " "+ str(year))
		plt.savefig("Plots/hfires_"+str(year)+ "_" + str(month)+".png", bbox_inches='tight')
		print(str(year), "  : ", str(month))
		plt.cla()
		plt.clf()
		plt.close()
