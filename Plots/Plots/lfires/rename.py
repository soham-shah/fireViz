import os
import glob
import re

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

dataDir = ''  
# Location of data files
newName = os.path.join(dataDir, 'lfires_') 
# New filename prefix
fnum = 0
# Starting frame number
# Iterate through each file in dataDir
for fName in sorted(glob.glob(os.path.join(dataDir, 'lfires*')),key=numericalSort):
	# Create the new file name
	new_fName = newName+str(fnum).zfill(3)+'.png'
	# Print the current file name(s) info
	print ('orig: %s     new: %s' % (fName, new_fName))
	# Rename the file
	os.rename(fName, new_fName)
	# Iterate the frame number
	fnum = fnum+ 1
