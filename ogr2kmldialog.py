from PyQt4 import QtCore, QtGui 
from ui_ogr2kml import Ui_ogr2kml

class ogr2kmlDialog(QtGui.QDialog): 
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_ogr2kml() 
        self.ui.setupUi(self)
