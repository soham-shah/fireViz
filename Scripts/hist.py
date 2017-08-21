import matplotlib.pyplot as plt
import pandas
import numpy as np


Data = pandas.read_csv("Human_PP_01.csv")
# Data = pandas.read_csv("Lightning_PP_01.csv")

t = np.arange(0.01, 20.0, 0.01)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(Data["FIRE_SIZE"], color='g')#, color='g')
# plt.semilogy(t, np.exp(-t/5.0))
plt.gca().set_yscale("log")
ax.set_ylabel('Number of Fires')
ax.set_xlabel('Size of Fire (Acres)')
plt.title('Human Fires by Size')	
ax.set_ylim([0,200000])
plt.savefig("Plots/size_hfires.png", bbox_inches='tight')