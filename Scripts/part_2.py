FILE_DIR = "/projects/nime1466/week_13/images"
DATA_DIR = "/projects/nime1466/week_13/Data_part2/"

import datetime as dt
import csv
import os
import sys

#Setup and launch Visit
sys.path.append("/curc/tools/x86_64/rh6/software/visit/2.10.2/2.10.2/linux-x86_64/lib/site-packages")

from visit import *

cwDir = DATA_DIR

# Formula for obtaining Translate X from lon
lonMultiplier = 8.5923199679034
lonBias = 783.923147989011

# Formula for obtaining Translate Y from lat

latMultiplier = 17.143816882876708
latBias = -478.4761738407286


def getTranslateValues(lat, lon):
        translateY = (lat * latMultiplier) + latBias
	translateX = (lon * lonMultiplier) + lonBias
	return translateX, translateY

def readLatsLons(f):
	"""
	Reads in the latitudes and longitudes for
	huricane Katrina for each day
	
	Args:
	file: File name of file to read in
	
	Returns: 
	lat: Array of latitude values
	lon: Array of longitude values
	
	Misc:
	cwDir: The path to your current working directory
	"""
	fPath = os.path.join(cwDir, f)
	lat = []
	lon = []
	with open(fPath) as latLonFile:
	    reader = csv.DictReader(latLonFile)
	    for row in reader:
		lat.append(float(row['Lat']))
		lon.append(float(row['Lon']))
	return lat, lon

def readTimes(f):	
	"""
	Reads in the latitudes and longitudes for
	huricane Katrina for each day
	
	Args:
	file: File name of file to read in
	
	Returns: 
	time: Array of latitude values
	lon: Array of longitude values
	
	Misc:
	cwDir: The path to your current working directory	
	"""
	
	fPath = os.path.join(cwDir, f)
	time = []
	with open(fPath) as timeFile:
	    reader = csv.DictReader(timeFile)
	    for row in reader:
		time.append(row['Times'])
	return time

def set_SaveImage_settings(file_dir, file_name):
    saveImgAtts = SaveWindowAttributes()
    saveImgAtts.outputToCurrentDirectory = 0
    saveImgAtts.outputDirectory = file_dir
    saveImgAtts.family = 0
    saveImgAtts.format = saveImgAtts.PNG
    saveImgAtts.width = 1024
    saveImgAtts.height = 1024
    saveImgAtts.quality = 80
    saveImgAtts.fileName = file_name
    return saveImgAtts

def set_View_settings(x, y, z):
    View3DAtts = View3DAttributes()
    View3DAtts.viewNormal = (x, y, z)
    View3DAtts.focus = (220.16, 261.12, 49.5)
    View3DAtts.viewUp = (0.10052, 0.342352, 0.934179)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 345.115
    View3DAtts.nearPlane = -690.23
    View3DAtts.farPlane = 690.23
    View3DAtts.imagePan = (0, 0)
    View3DAtts.imageZoom = 1.75
    View3DAtts.perspective = 1
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (220.16, 261.12, 49.5)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
    return View3DAtts

def add_photo_background():
    OpenDatabase("/projects/nime1466/week_13/Data_part1/katrinaTerrain.png", 0, "Image")
    AddPlot("Truecolor", "color", 1, 0)
    AddOperator("Elevate", 0)
    ElevateAtts = ElevateAttributes()
    ElevateAtts.zeroFlag = 1
    ElevateAtts.variable = "default"
    SetOperatorOptions(ElevateAtts, 0)

    AddOperator("Transform", 0)

    TransformAtts = TransformAttributes()
    TransformAtts.doRotate = 0
    TransformAtts.doScale = 1
    TransformAtts.scaleX = 0.43
    TransformAtts.scaleY = 0.68
    TransformAtts.scaleZ = 1
    TransformAtts.doTranslate = 0
    SetOperatorOptions(TransformAtts, 0)
    DrawPlots()


def create_wind_vector_plot(path, translateX, translateY):
    OpenDatabase(path, 0, "NETCDF")
    DefineVectorExpression("wind", "{U, V, W}")
    DefineScalarExpression("windMag", "magnitude(wind)")
    AddPlot("Vector", "wind", 1, 0)
    SetActivePlots(1)
    AddOperator("Transform", 0)
    TransformAtts = TransformAttributes()
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = translateX
    TransformAtts.translateY = translateY
    TransformAtts.translateZ = 0
    SetOperatorOptions(TransformAtts, 0)
    AddOperator("Slice", 0)
    SliceAtts = SliceAttributes()
    SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
    SliceAtts.axisType = SliceAtts.ZAxis
    SliceAtts.originIntercept = 5
    SliceAtts.normal = (0, 0, 1)
    SliceAtts.project2d = 0
    SetOperatorOptions(SliceAtts, 0)

    VectorAtts = VectorAttributes()
    VectorAtts.glyphLocation = VectorAtts.AdaptsToMeshResolution
    VectorAtts.useStride = 0
    VectorAtts.stride = 1
    VectorAtts.nVectors = 2500
    VectorAtts.lineStyle = VectorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
    VectorAtts.lineWidth = 0
    VectorAtts.scale = 0.25
    VectorAtts.scaleByMagnitude = 1
    VectorAtts.autoScale = 1
    VectorAtts.headSize = 0.25
    VectorAtts.headOn = 1
    VectorAtts.colorByMag = 1
    VectorAtts.useLegend = 0
    VectorAtts.vectorColor = (0, 0, 0, 255)
    VectorAtts.colorTableName = "Default"
    VectorAtts.origOnly = 1
    VectorAtts.glyphType = VectorAtts.Arrow  # Arrow, Ellipsoid
    SetPlotOptions(VectorAtts)

    SetActivePlots((0, 2))
    SetActivePlots(2)
    SetActivePlots(3)
    DrawPlots()


def create_streamline_plot(translateX, translateY):

    AddPlot("Streamline", "wind", 1, 0)
    SetActivePlots(2)
    StreamlineAtts = StreamlineAttributes()
    StreamlineAtts.sourceType = StreamlineAtts.SpecifiedCircle
    StreamlineAtts.planeOrigin = (210, 80, 5)
    StreamlineAtts.planeNormal = (0, 0, 1)
    StreamlineAtts.planeUpAxis = (0, 1, 0)
    StreamlineAtts.radius = 100
    StreamlineAtts.colorTableName = "hot"
    StreamlineAtts.sampleDensity0 = 9
    StreamlineAtts.sampleDensity1 = 4
    StreamlineAtts.singleColor = (0, 0, 0, 255)
    StreamlineAtts.legendFlag = 0
    StreamlineAtts.lightingFlag = 1
    StreamlineAtts.integrationDirection = StreamlineAtts.Both  # Forward, Backward, Both
    StreamlineAtts.limitMaximumTimestep = 1
    StreamlineAtts.maxTimeStep = 0.01
    StreamlineAtts.relTol = 0.0001
    
    AddOperator("Transform", 0)
    TransformAtts = TransformAttributes()
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = translateX
    TransformAtts.translateY = translateY
    TransformAtts.translateZ = 0
    SetOperatorOptions(TransformAtts, 0)

    StreamlineAtts.integrationType = StreamlineAtts.DormandPrince
    StreamlineAtts.parallelizationAlgorithmType = StreamlineAtts.VisItSelects

    StreamlineAtts.coloringVariable = "windMag"

    StreamlineAtts.displayMethod = StreamlineAtts.Tubes  # Lines, Tubes, Ribbons
    StreamlineAtts.varyTubeRadiusVariable = "windMag"
    SetPlotOptions(StreamlineAtts)
    DrawPlots()
    SetActivePlots(1)
    VectorAtts = VectorAttributes()
    VectorAtts.nVectors = 5000
    SetPlotOptions(VectorAtts)
    DrawPlots()


def create_cloud_plot(translateX, translateY):

    AddPlot("Volume", "QCLOUD", 1, 0)
    SetActivePlots(3)
    AddOperator("Transform", 0)
    TransformAtts = TransformAttributes()
    TransformAtts.doScale = 1
    TransformAtts.scaleX = 1
    TransformAtts.scaleY = 1
    TransformAtts.scaleZ = 3
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = translateX
    TransformAtts.translateY = translateY
    TransformAtts.translateZ = 0
    SetOperatorOptions(TransformAtts, 0)

    DrawPlots()
    VolumeAtts = VolumeAttributes()
    VolumeAtts.resampleFlag = 1
    VolumeAtts.legendFlag = 0
    VolumeAtts.resampleTarget = 5000000
    VolumeAtts.colorControlPoints.GetControlPoints(0).colors = (255, 255, 255, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(0).position = 0
    VolumeAtts.colorControlPoints.GetControlPoints(1).colors = (240, 240, 240, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(1).position = 0.125
    VolumeAtts.colorControlPoints.GetControlPoints(2).colors = (217, 217, 217, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(2).position = 0.25
    VolumeAtts.colorControlPoints.GetControlPoints(3).colors = (189, 189, 189, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(3).position = 0.375
    VolumeAtts.colorControlPoints.GetControlPoints(4).colors = (150, 150, 150, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(4).position = 0.5

    SetPlotOptions(VolumeAtts)
    AddPlot("Pseudocolor", "QCLOUD", 1, 0)
    SetActivePlots(4)
    AddOperator("Transform", 0)
    TransformAtts = TransformAttributes()
    TransformAtts.doScale = 1
    TransformAtts.scaleOrigin = (0, 0, 0)
    TransformAtts.scaleX = 1
    TransformAtts.scaleY = 1
    TransformAtts.scaleZ = 3
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = translateX
    TransformAtts.translateY = translateY
    TransformAtts.translateZ = 0


    SetOperatorOptions(TransformAtts, 0)
    AddOperator("Isovolume", 0)
    IsovolumeAtts = IsovolumeAttributes()
    IsovolumeAtts.lbound = 0.0005
    IsovolumeAtts.ubound = 1e+37
    IsovolumeAtts.variable = "default"
    SetOperatorOptions(IsovolumeAtts, 0)
    DrawPlots()

    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.max = 0.0015
    PseudocolorAtts.colorTableName = "Reds"
    PseudocolorAtts.legendFlag = 0

    SetPlotOptions(PseudocolorAtts)
    AddPlot("Pseudocolor", "RAINNC", 1, 0)
    SetActivePlots(5)
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.colorTableName = "hot"
    PseudocolorAtts.legendFlag = 0
    SetPlotOptions(PseudocolorAtts)
    AddOperator("Elevate", 0)
    ElevateAtts = ElevateAttributes()
    ElevateAtts.zeroFlag = 1
    SetOperatorOptions(ElevateAtts, 0)

    AddOperator("Transform", 0)
    TransformAtts = TransformAttributes()
    TransformAtts.scaleX = 1
    TransformAtts.scaleY = 1
    TransformAtts.scaleZ = 1.05
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = translateX
    TransformAtts.translateY = translateY
    TransformAtts.translateZ = 0
    SetOperatorOptions(TransformAtts, 0)
    DrawPlots()
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.colorTableName = "raincc"
    PseudocolorAtts.legendFlag = 0
    PseudocolorAtts.opacityType = PseudocolorAtts.ColorTable
    SetPlotOptions(PseudocolorAtts)


    # Begin spontaneous state
    View3DAtts = View3DAttributes()
    View3DAtts.viewNormal = (-0.298973, -0.858081, 0.417507)
    View3DAtts.focus = (157.5, 154.483, 49.5)
    View3DAtts.viewUp = (0.039275, 0.426083, 0.903831)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 226.101
    View3DAtts.nearPlane = -452.189
    View3DAtts.farPlane = 452.189
    View3DAtts.imagePan = (0, 0)
    View3DAtts.imageZoom = 2.14359
    View3DAtts.perspective = 1
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (157.491, 154.483, 49.5)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
    SetView3D(View3DAtts)
    # End spontaneous state
    light0 = LightAttributes()
    light0.enabledFlag = 1
    light0.type = light0.Object  # Ambient, Object, Camera
    light0.direction = (0, 0, -1)
    light0.color = (255, 255, 255, 255)
    light0.brightness = 0.9
    SetLight(0, light0)

    AnnotationAtts = AnnotationAttributes()
    AnnotationAtts.backgroundColor = (0, 0, 0, 255)
    AnnotationAtts.axes2D.visible = 0
    AnnotationAtts.axes2D.yAxis.grid = 0
    AnnotationAtts.axes3D.visible = 0
    AnnotationAtts.axes3D.triadFlag = 0
    AnnotationAtts.axes3D.bboxFlag = 0
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.databaseInfoFlag = 0
    AnnotationAtts.legendInfoFlag = 0
    SetAnnotationAttributes(AnnotationAtts)
    SetAnnotationAttributes(AnnotationAtts)


def create_final_plot(f_name, date_time, banner):
    RenderingAtts = RenderingAttributes()
    RenderingAtts.antialiasing = 1
    SetRenderingAttributes(RenderingAtts)
    SetActivePlots(4)
    VolumeAtts = VolumeAttributes()
    VolumeAtts.legendFlag = 0
    VolumeAtts.resampleTarget = 50000000
    VolumeAtts.colorControlPoints.GetControlPoints(0).colors = (255, 255, 255, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(0).position = 0
    VolumeAtts.colorControlPoints.GetControlPoints(1).colors = (240, 240, 240, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(1).position = 0.125
    VolumeAtts.colorControlPoints.GetControlPoints(2).colors = (217, 217, 217, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(2).position = 0.25
    VolumeAtts.colorControlPoints.GetControlPoints(3).colors = (189, 189, 189, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(3).position = 0.375
    VolumeAtts.colorControlPoints.GetControlPoints(4).colors = (150, 150, 150, 255)
    VolumeAtts.colorControlPoints.GetControlPoints(4).position = 0.5
    SetPlotOptions(VolumeAtts)
    
    banner.text = date_time
    # Begin spontaneous state
    View3DAtts = View3DAttributes()
    View3DAtts.viewNormal = (-0.583513, -0.740215, 0.334057)
    View3DAtts.focus = (220.16, 261.12, 49.5)
    View3DAtts.viewUp = (0.10052, 0.342352, 0.934179)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 345.115
    View3DAtts.nearPlane = -690.23
    View3DAtts.farPlane = 690.23
    View3DAtts.imagePan = (0, 0)
    View3DAtts.imageZoom = 1.75
    View3DAtts.perspective = 1
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (220.16, 261.12, 49.5)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
    SetView3D(View3DAtts)

    saveImgAtts = set_SaveImage_settings(FILE_DIR, f_name)
    SetSaveWindowAttributes(saveImgAtts)
    SaveWindow()


#####################################################
#                 Main function                      #
#####################################################

if __name__ == '__main__':
	lats, lons = readLatsLons('latslons.csv')
	times = readTimes('Times.csv')
	Launch()
	AnnotationAtts = AnnotationAttributes()
	AnnotationAtts.axes2D.visible = 0
	AnnotationAtts.axes2D.yAxis.grid = 0
	AnnotationAtts.axes3D.visible = 0
	AnnotationAtts.axes3D.triadFlag = 0
	AnnotationAtts.axes3D.bboxFlag = 0
	AnnotationAtts.userInfoFlag = 0
	AnnotationAtts.databaseInfoFlag = 0
	AnnotationAtts.legendInfoFlag = 0
	SetAnnotationAttributes(AnnotationAtts)
    	banner = CreateAnnotationObject("Text2D")        banner.position = (0.5, 0.90)        banner.fontBold = 1
        banner.useForegroundForTextColor = 0
        banner.textColor = (255, 255, 255, 255)

	beg_dt = dt.datetime.strptime('08-29-2005 00', '%m-%d-%Y %H')
	end_dt = dt.datetime.strptime('08-31-2005 09', '%m-%d-%Y %H')
	cur_dt = beg_dt
	special_dt = dt.datetime.strptime('08-29-2005 15', '%m-%d-%Y %H')
	index = 1
	latLonIndex = 0
	add_photo_background()
	file_prefix = "wrfout_d02_"
	while cur_dt <= end_dt:
	    data_file = file_prefix + cur_dt.strftime("%Y-%m-%d_%H")
	    curLat = lats[latLonIndex]
 	    curLon = lons[latLonIndex]
	    curTime = times[latLonIndex]
	    translateX, translateY = getTranslateValues(curLat, curLon)
	    create_wind_vector_plot(data_file, translateX, translateY)
	    create_streamline_plot(translateX, translateY)
	    create_cloud_plot(translateX, translateY)
	    f_name = "katrina_path_{}.png".format(index)
	    index += 1
	    create_final_plot(f_name=f_name, date_time=curTime, banner=banner)
	    if cur_dt == special_dt:
		v1 = set_View_settings(-0.583513, -0.740215, 0.334057)
		v2 = set_View_settings(0.583513, -0.740215, 0.334057)
                v3 = set_View_settings(-0.583513, -0.740215, 0.334057)
		vpts = (v1, v2)
		#Create your weights
		weights = []
		l_vpts = len(vpts)
		for i in range(l_vpts):
		  weights = weights + [float(i)/float(l_vpts - 1)]
	        for i in range(1, 241):
		    t = float(i)/float(241 - 1)
		    p = EvalCubicSpline(t, weights, vpts)
		    SetView3D(p)
		    f_name = "katrina_path_{}.png".format(index)
	    	    index += 1
		    saveImgAtts = set_SaveImage_settings(FILE_DIR, f_name)
		    SetSaveWindowAttributes(saveImgAtts)
		    SaveWindow()
	    SetActivePlots((1, 2, 3, 4, 5))
	    DeleteActivePlots()
	    CloseDatabase(data_file)
	    latLonIndex += 1
	    cur_dt = cur_dt + dt.timedelta(hours=1)

