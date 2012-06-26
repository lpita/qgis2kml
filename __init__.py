def name():
  return "qgis2kml"

def description():
  return "This plugin convert a vector file loaded into QGIS to kml with style"

def version():
  return "Version 0.2"

def qgisMinimumVersion():
  return "1.8"

def authorName():
  return "Luca Delucchi"

def classFactory(iface):
  # load TestPlugin class from file testplugin.py
  from qgis2kml import QGIS2KML
  return QGIS2KML(iface)
