from PyQt4 import QtCore, QtGui 
from ui_qgis2kml import Ui_qgis2kml

class qgis2kmlDialog(QtGui.QDialog): 
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_qgis2kml() 
        self.ui.setupUi(self)
