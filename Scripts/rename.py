import os
import glob

dataDir = ''  
# Location of data files
newName = os.path.join(dataDir, 'wrfout_') 
# New filename prefix
fnum = 0
# Starting frame number
# Iterate through each file in dataDir
for fName in glob.glob(os.path.join(dataDir, 'wrfout_*')):
	# Create the new file name
	new_fName = newName+str
	(fnum).zfill(3)+'.png'
	# Print the current file name(s) info
	print ('orig: %s     new: %s' % (fName, new_fName))
	# Rename the file
	os.rename(fName, new_fName)
	# Iterate the frame number
	fnum = fnum+ 1