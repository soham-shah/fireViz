#!/usr/bin/python

import numpy as np
import pandas as pd
import os
import sys
sys.path.append("/curc/tools/x86_64/rh6/software/visit/2.10.0/2.10.0/linux-x86_64/lib/site-packages")
from visit import *
import time

def closeDatabases(indexString):
  CloseDatabase("localhost:/projects/joki9146/week_13/Data_part2/wrfout_" + indexString + ".nc")
  CloseDatabase("localhost:/projects/joki9146/week_13/Data_part1/katrinaTerrain.png")

#open db
def openDB(indexString):
  filename = "localhost:/projects/joki9146/week_13/Data_part2/wrfout_" + indexString + ".nc"
  OpenDatabase(filename, 0, "NETCDF")
  ActivateDatabase(filename)

#load bg image
def loadBGImage(lat, lon):
  OpenDatabase("localhost:/projects/joki9146/week_13/Data_part1/katrinaTerrain.png", 0, "Image")
  ActivateDatabase("localhost:/projects/joki9146/week_13/Data_part1/katrinaTerrain.png")
  AddPlot("Truecolor", "color", 1, 0)
  TruecolorAtts = TruecolorAttributes()
  TruecolorAtts.opacity = 1
  TruecolorAtts.lightingFlag = 0
  SetPlotOptions(TruecolorAtts)

  #add elevate
  SetActivePlots(1)
  AddOperator("Elevate", 0)
  ElevateAtts = ElevateAttributes()
  ElevateAtts.zeroFlag = 1
  SetOperatorOptions(ElevateAtts, 0)

  #add transform
  AddOperator("Transform", 0)
  TransformAtts = TransformAttributes()
  TransformAtts.doScale = 1
  TransformAtts.scaleX = 0.43
  TransformAtts.scaleY = 0.68
  TransformAtts.scaleZ = 1
  SetOperatorOptions(TransformAtts, 1)

  #add transform
  AddOperator("Transform", 0)
  TransformAtts = TransformAttributes()
  TransformAtts.doTranslate = 1
  TransformAtts.translateX = -lon
  TransformAtts.translateY = -lat
  TransformAtts.translateZ = 0
  SetOperatorOptions(TransformAtts, 2)


def plotWind():
  DefineVectorExpression("wind", "{U, V, W}")
  DefineScalarExpression("windMag", "magnitude(wind)")
  AddPlot("Vector", "wind")

  #add slice
  AddOperator("Slice", 0)
  SliceAtts = SliceAttributes()
  SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
  SliceAtts.originIntercept = 5
  SliceAtts.normal = (0, 0, 1)
  SliceAtts.axisType = SliceAtts.ZAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
  SliceAtts.upAxis = (0, 1, 0)
  SliceAtts.project2d = 0
  SliceAtts.meshName = "as_zonal/mesh315x309"
  SetOperatorOptions(SliceAtts, 0)

  #wind vec attrs
  VectorAtts = VectorAttributes()
  VectorAtts.nVectors = 4000
  VectorAtts.lineStyle = VectorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
  VectorAtts.scale = 0.08
  VectorAtts.scaleByMagnitude = 1
  VectorAtts.autoScale = 0
  VectorAtts.headSize = 0.3
  VectorAtts.headOn = 1
  VectorAtts.colorByMag = 1
  VectorAtts.lineStem = VectorAtts.Cylinder  # Cylinder, Line
  VectorAtts.stemWidth = 0.1
  VectorAtts.glyphType = VectorAtts.Arrow  # Arrow, Ellipsoid
  VectorAtts.vectorOrigin = VectorAtts.Middle  # Head, Middle, Tail
  VectorAtts.geometryQuality = VectorAtts.High  # Fast, High
  VectorAtts.useLegend = 0
  SetPlotOptions(VectorAtts)

def plotStreamtline():
  AddPlot("Streamline", "wind")
  StreamlineAtts = StreamlineAttributes()
  StreamlineAtts.sourceType = StreamlineAtts.SpecifiedCircle  # SpecifiedPoint, SpecifiedPointList, SpecifiedLine, SpecifiedCircle, SpecifiedPlane, SpecifiedSphere, SpecifiedBox, Selection
  StreamlineAtts.planeOrigin = (155, 155, 5)
  StreamlineAtts.planeNormal = (0, 0, 1)
  StreamlineAtts.planeUpAxis = (0, 1, 0)
  StreamlineAtts.radius = 100
  StreamlineAtts.sampleDensity0 = 9
  StreamlineAtts.sampleDensity1 = 4
  StreamlineAtts.integrationDirection = StreamlineAtts.Both  # Forward, Backward, Both
  StreamlineAtts.maxSteps = 1000
  StreamlineAtts.limitMaximumTimestep = 1
  StreamlineAtts.maxTimeStep = 0.01
  StreamlineAtts.displayMethod = StreamlineAtts.Tubes  # Lines, Tubes, Ribbons
  StreamlineAtts.varyTubeRadius = StreamlineAtts.Scalar  # None, Scalar
  StreamlineAtts.varyTubeRadiusFactor = 10
  StreamlineAtts.colorTableName = "hot"
  StreamlineAtts.coloringMethod = StreamlineAtts.ColorByVariable  # Solid, ColorBySpeed, ColorByVorticity, ColorByLength, ColorByTime, ColorBySeedPointID, ColorByVariable, ColorByCorrelationDistance, ColorByNumberDomainsVisited
  StreamlineAtts.coloringVariable = "windMag"
  StreamlineAtts.tubeRadiusAbsolute = 0.125
  StreamlineAtts.tubeRadiusBBox = 0.0025
  StreamlineAtts.showSeeds = 0
  StreamlineAtts.varyTubeRadius = StreamlineAtts.Scalar  # None, Scalar
  StreamlineAtts.varyTubeRadiusFactor = 6
  StreamlineAtts.varyTubeRadiusVariable = "windMag"
  StreamlineAtts.legendFlag = 0
  SetPlotOptions(StreamlineAtts)

#SetActivePlots(3)
#RemoveOperator(0, 0)

#add clouds
def addClouds():
  AddPlot("Volume", "QCLOUD", 1, 0)
  SetActivePlots(4)
  AddOperator("Transform", 0)
  TransformAtts = TransformAttributes()
  TransformAtts.doScale = 1
  TransformAtts.scaleOrigin = (0, 0, 0)
  TransformAtts.scaleX = 1
  TransformAtts.scaleY = 1
  TransformAtts.scaleZ = 3
  SetOperatorOptions(TransformAtts, 0)
  VolumeAtts = VolumeAttributes()
  VolumeAtts.legendFlag = 0
  VolumeAtts.colorControlPoints.GetControlPoints(0).colors = (220, 220, 220, 0)
  VolumeAtts.colorControlPoints.GetControlPoints(0).position = 0
  VolumeAtts.colorControlPoints.GetControlPoints(1).colors = (240, 240, 240, 255)
  VolumeAtts.colorControlPoints.GetControlPoints(1).position = 0.34106
  VolumeAtts.colorControlPoints.GetControlPoints(2).colors = (255, 255, 255, 255)
  VolumeAtts.colorControlPoints.GetControlPoints(2).position = 1
  VolumeAtts.colorControlPoints.smoothing = VolumeAtts.colorControlPoints.Linear  # None, Linear, CubicSpline
  VolumeAtts.colorControlPoints.equalSpacingFlag = 0
  VolumeAtts.colorControlPoints.discreteFlag = 0
  VolumeAtts.opacityAttenuation = 1
  VolumeAtts.opacityMode = VolumeAtts.ColorTableMode  # FreeformMode, GaussianMode, ColorTableMode
  VolumeAtts.resampleFlag = 1
  VolumeAtts.resampleTarget = 10000000
  VolumeAtts.rendererType = VolumeAtts.Splatting  # Splatting, Texture3D, RayCasting, RayCastingIntegration, SLIVR, RayCastingSLIVR, Tuvok
  VolumeAtts.gradientType = VolumeAtts.SobelOperator  # CenteredDifferences, SobelOperator
  VolumeAtts.transferFunctionDim = 1
  SetPlotOptions(VolumeAtts)

#add hot towers
def addHotTowers():
  AddPlot("Pseudocolor", "QCLOUD", 1, 0)
  SetActivePlots(5)
  AddOperator("Transform", 0)
  TransformAtts = TransformAttributes()
  TransformAtts.doScale = 1
  TransformAtts.scaleOrigin = (0, 0, 0)
  TransformAtts.scaleX = 1
  TransformAtts.scaleY = 1
  TransformAtts.scaleZ = 3
  SetOperatorOptions(TransformAtts, 0)
  AddOperator("Isovolume", 0)
  IsovolumeAtts = IsovolumeAttributes()
  IsovolumeAtts.lbound = 0.0005
  IsovolumeAtts.ubound = 1e+37
  IsovolumeAtts.variable = "default"
  SetOperatorOptions(IsovolumeAtts, 0)
  PseudocolorAtts = PseudocolorAttributes()
  PseudocolorAtts.maxFlag = 1
  PseudocolorAtts.max = 0.0015
  PseudocolorAtts.centering = PseudocolorAtts.Zonal  # Natural, Nodal, Zonal
  PseudocolorAtts.colorTableName = "Reds"
  PseudocolorAtts.legendFlag = 0
  PseudocolorAtts.smoothingLevel = 2
  SetPlotOptions(PseudocolorAtts)

#add rainfall
def addRainfall():
  AddPlot("Pseudocolor", "RAINNC", 1, 0)
  SetActivePlots(6)
  PseudocolorAtts = PseudocolorAttributes()
  PseudocolorAtts.colorTableName = "RAINNC"
  PseudocolorAtts.opacityType = PseudocolorAtts.ColorTable  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
  PseudocolorAtts.lightingFlag = 0
  PseudocolorAtts.legendFlag = 0
  SetPlotOptions(PseudocolorAtts)
  AddOperator("Elevate", 0)
  ElevateAtts = ElevateAttributes()
  ElevateAtts.zeroFlag = 1
  SetOperatorOptions(ElevateAtts, 0)
  AddOperator("Transform", 0)
  TransformAtts = TransformAttributes()
  TransformAtts.doTranslate = 1
  TransformAtts.translateX = 0
  TransformAtts.translateY = 0
  TransformAtts.translateZ = 0.05
  SetOperatorOptions(TransformAtts, 0)

#add light
def addLight():
  light1 = LightAttributes()
  light1.enabledFlag = 1
  light1.type = light1.Object  # Ambient, Object, Camera
  light1.direction = (0, 0, -1)
  light1.color = (255, 255, 255, 255)
  light1.brightness = 0.5
  SetLight(1, light1)

def annotation():
  AnnotationAtts = AnnotationAttributes()
  AnnotationAtts.axes2D.visible = 0
  AnnotationAtts.axes3D.visible = 0
  AnnotationAtts.axes3D.triadFlag = 0
  AnnotationAtts.axes3D.bboxFlag = 0
  AnnotationAtts.userInfoFlag = 0
  AnnotationAtts.databaseInfoFlag = 0
  AnnotationAtts.legendInfoFlag = 0
  AnnotationAtts.axesArray.visible = 0
  AnnotationAtts.backgroundColor = (0, 0, 0, 255)
  SetAnnotationAttributes(AnnotationAtts)

#set view angle
def setView():
  View3DAtts = View3DAttributes()
  View3DAtts.viewNormal = (-0.745356, -0.596285, 0.298142)
  View3DAtts.focus = (153.99998, 156.99997, 0)
  View3DAtts.viewUp = (0, 0, 1)
  View3DAtts.imagePan = (0, .03)
  View3DAtts.imageZoom = 4
  SetView3D(View3DAtts)

def saveFile(fileIndex):
  SaveWindowAtts = SaveWindowAttributes()
  SaveWindowAtts.outputToCurrentDirectory = 0
  SaveWindowAtts.outputDirectory = "/projects/joki9146/week_13/output/"
  SaveWindowAtts.fileName = "katrina"+fileIndex
  SaveWindowAtts.family = 0
  SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY
  SaveWindowAtts.width = 1024
  SaveWindowAtts.height = 1024
  SaveWindowAtts.compression = SaveWindowAtts.PackBits  # None, PackBits, Jpeg, Deflate
  SaveWindowAtts.forceMerge = 0
  SetSaveWindowAttributes(SaveWindowAtts)
  SaveWindow()

def readLatsLons(file):
  fPath = os.path.join(cwDir, file)
  df = pd.read_csv(fPath)
  lats = df['Lat'].values
  lons = df['Lon'].values
  lat=[]
  lon=[]

  for i in range(0,lats.size):
	  lat.append(lats[i]-lats[0])

  for i in range(0,lons.size):
	  lon.append(lons[i]-lons[0])
	
  lat=np.asarray(lat)
  lon=np.asarray(lon)
  return lat, lon

def readTimes(file):
  fPath = os.path.join(cwDir, file)
  df = pd.read_csv(fPath)
  time = df['Times'].values
  return time

def convertLat(lat):
  print lat
  factor = 27.43435
  coord = (lat) * factor
  print coord 
  return coord

def convertLon(lon):
  print lon
  factor = -24.07495
  coord = (lon) * factor
  print coord
  return coord

#main
print "started"
i = int(sys.argv[1])
print i

cwDir = "/projects/joki9146/week_13/Data_part2/"

lats, lons = readLatsLons("latslons.csv")
times = readTimes("Times.csv")

Launch()
loadBGImage(convertLat(lats[i]), convertLon(lons[i]))
openDB(str(i).zfill(3))
plotWind()
plotStreamtline()
addClouds()
addHotTowers()
addRainfall()
addLight()
annotation()
setView()
DrawPlots()
saveFile(str(i).zfill(3))
DeleteAllPlots()
closeDatabases(str(i).zfill(3))
Close()
