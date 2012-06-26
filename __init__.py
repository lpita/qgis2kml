def name():
  return "ogr2kml"

def description():
  return "This plugin convert a vector file loaded into QGIS to kml with style"

def version():
  return "Version 0.1"

def qgisMinimumVersion():
  return "1.8"

def authorName():
  return "Luca Delucchi"

def classFactory(iface):
  # load TestPlugin class from file testplugin.py
  from ogr2kml import OGR2KML
  return OGR2KML(iface)
