import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

humanData = pandas.read_csv("Human_PP_01.csv")
lightningData = pandas.read_csv("Lightning_PP_01.csv")

human = []
lightning = []

ax = plt.subplot(111)

for month in range(1,13):
	currentHumanMonth = humanData.loc[humanData['FIRE_MONTH'] == month]
	human.append(len(currentHumanMonth))
	currentLightningMonth = lightningData.loc[lightningData['FIRE_MONTH'] == month]
	lightning.append(len(currentLightningMonth))
	
for i in range (0,12):
	print (i)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	rects2 = ax.pie([human[i],lightning[i]],labels=["Human", "Lightning"])
	# plt.legend()
	plt.title('Fires in ' + monthDict[i+1])
	# plt.show()
	plt.savefig("Plots/pie" + str(i) + ".png", bbox_inches='tight')
	plt.cla()
	plt.clf()
	plt.close()
