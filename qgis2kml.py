from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis2kmldialog import qgis2kmlDialog
from qgis2kmlStyle import qgis2kmlClassStyle
from qgis2funz import *
# initialize Qt resources from file resouces.py
import resources_rc
import os
import sys
import zipfile
import shutil

currentPath = os.path.dirname( __file__ )
sys.path.append( os.path.abspath(currentPath))
import simplekml

class QGIS2KML:
    MSG_BOX_TITLE = "qgis2kml Plugin Warning"
    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/qgis2kml/icon.png"), "qgis2kml", self.iface.mainWindow())
        self.action.setWhatsThis("Configuration for qgis2kml plugin")
        #self.action.setStatusTip("This is status tip")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&qgis2kml", self.action)

        # connect to signal renderComplete which is emitted when canvas rendering is done
        #QObject.connect(self.iface.mapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderTest)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&qgis2kml",self.action)
        self.iface.removeToolBarIcon(self.action)
        
        # disconnect form signal of the canvas
        #QObject.disconnect(self.iface.MapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderTest)
        
    def run(self):
        # create and show a configuration dialog or something similar
        self.dlg = qgis2kmlDialog()
        #select directory where save files
        QObject.connect(self.dlg.ui.browseButton, SIGNAL("clicked()"), self.SelectKmlDir)
        #load layer
        layers =  self.iface.activeLayer()
        #OGR layers
        self.layers = {}        
        #Checks for loaded layers, do not load if no layers
        if layers == None:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("No active layer found\n" "Please make one or more OGR layer "\
            "active\n" "Beware of layers sizes for export"), QMessageBox.Ok, 
            QMessageBox.Ok)
            return
        #load qgis mapCanvas
        self.mapCanvas = self.iface.mapCanvas()
        #set number of row in the table
        self.dlg.ui.tablelayers.setColumnCount(3)
        self.dlg.ui.tablelayers.setRowCount(self.mapCanvas.layerCount())
        #add header
        item = QTableWidgetItem('Source')
        self.dlg.ui.tablelayers.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem('Name field')
        self.dlg.ui.tablelayers.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem('Desc field')
        self.dlg.ui.tablelayers.setHorizontalHeaderItem(2, item)
        #number of layer
        n_layer = 0
        #Checks vector type and populates the layer list view in opposite 
        #order for the correct visualization on OL
        for i in range(self.mapCanvas.layerCount()-1,-1,-1):
            # define actual layer
            layer = self.mapCanvas.layer(i)
            #check if is a vector (TODO remove when support also other type)
            if layer.type() == layer.VectorLayer:
                nameFields = fieldsName(layer)
                self.layers[layer] = nameFields
                #this is for remove "layerid=*" when use "Unique Value" symbology
                source=layer.source()
                source.remove(QRegExp('\|layerid=[\d]+$'))
                #create and add item of the source to table layer list
                item = QTableWidgetItem(source)
                self.dlg.ui.tablelayers.setItem(n_layer,0, item)
                #
                nameTableItem = QComboBox()
                nameTableItem.addItem('No Name field')
                descTableItem = QComboBox()
                descTableItem.addItem('No Desc field')
                for f in nameFields:
                    nameTableItem.addItem(f)
                    descTableItem.addItem(f)
                self.dlg.ui.tablelayers.setCellWidget(n_layer,1, nameTableItem)
                self.dlg.ui.tablelayers.setCellWidget(n_layer,2, descTableItem)
                n_layer += 1
        self.dlg.ui.tablelayers.resizeColumnsToContents()
        #button for start the plugin
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.WriteKML)
        #button for close the plugin after create openlayers file
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("rejected()"), self.dlg.close)
        #Set up the default map extent
        Extent = self.mapCanvas.extent()
        if len(self.layers) == 0:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("No active point layer found\n" "Please make one or more OGR layer "\
            "active\n" "Beware of layers sizes for export"), QMessageBox.Ok, 
            QMessageBox.Ok)
            return
        #set the directory where save the files
        global mydir
        mydir=""
        self.dlg.show()

    def SelectKmlDir(self):
        #set up the output dir for new vector files
        global mydir
        mydir = QFileDialog.getExistingDirectory( None,QString("Choose the GML"\
        " files destination folder"),"")
        if not mydir:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("You have to choose a folder"), QMessageBox.Ok, 
            QMessageBox.Ok)
        elif os.access(mydir, os.W_OK):
            self.dlg.ui.kmldirpath.setText(mydir)
            return
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("It is not possible to write into folder '%s'" % mydir), QMessageBox.Ok, 
            QMessageBox.Ok)

    def kmlStyle(self,st,fe,geot,at=None):
        """Create the style of feature"""
        if st.output['type'] == 'singleSymbol':
            fe.style = st.output['style']
        if st.output['type'] == 'categorizedSymbol':
            attr = unicode(at)
            fe.style = st.output[attr]['style']
        if st.output['type'] == 'graduatedSymbol':
            attr = float(unicode(at))
            for i in range(len(st.ranges)):
                nl = 'symb%i' % i
                if attr <= st.output[nl]['max'] and attr >= st.output[nl]['min']:
                    fe.style = st.output[nl]['style']
                    break
        if not self.icon:
            fe.style.iconstyle.icon = None
            
    def WriteKML(self):
        nrow = 0
        outPath = str(self.dlg.ui.kmldirpath.text())  
        if self.dlg.ui.checkBox.isChecked():
            self.icon = True
        else:
            self.icon = False
        for layer, fields in self.layers.iteritems():
            outFormat = self.dlg.ui.outputFormCombo.currentIndex()            
            if layer.geometryType() > QGis.WKBPolygon:
                QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
                ("Layer %s: format not yet supported" % layer.name()), QMessageBox.Ok, QMessageBox.Ok)
            source = layer.source()
            source.remove(QRegExp('\|layerid=[\d]+$'))
            if source != self.dlg.ui.tablelayers.item(nrow,0).text():
                QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
                ("An error occur with vector: %s" % layer.name()), QMessageBox.Ok, QMessageBox.Ok)
            # create kml for layer
            kml = simplekml.Kml(name=layer.name())
            folder = kml.newfolder(name=layer.name())
            # create style
            if layer.geometryType() != 0:
                self.icon = False
            if self.icon:
                outFormat = 1
            style = qgis2kmlClassStyle(layer,self.icon,outPath)
            provider = layer.dataProvider()
            #set coordinate system of my first vector
            SrsSrc = provider.crs()
            #set wgs84 coordinate system
            SrsDest = QgsCoordinateReferenceSystem(4326)
            #trasform
            SrsTrasform = QgsCoordinateTransform(SrsSrc, SrsDest)
            qgisFeat = QgsFeature()
            allAttrs = provider.attributeIndexes()
            provider.select(allAttrs)
            if style.output['type'] != 'singleSymbol':
                idf = idField(layer,style.nameField)
            while provider.nextFeature(qgisFeat):
                geom = qgisFeat.geometry()
                attrs = qgisFeat.attributeMap()
                if geom.wkbType() == QGis.WKBPoint:
                    feat = folder.newpoint()
                    new_geom = SrsTrasform.transform(geom.asPoint())
                    x = float(new_geom.x())
                    y = float(new_geom.y())
                    feat.coords = [(x, y)]
                    if style.output['type'] != 'singleSymbol':
                        self.kmlStyle(style,feat,geom.wkbType(),attrs[idf].toString())
                    else:
                        self.kmlStyle(style,feat,geom.wkbType())
                elif geom.wkbType() == QGis.WKBLineString:
                    feat = folder.newlinestring()
                    line = []
                    for g in qgisFeat.geometry().asPolyline():
                        line.append(SrsTrasform.transform(g))
                    feat.coords = line
                    if style.output['type'] != 'singleSymbol':
                        self.kmlStyle(style,feat,geom.wkbType(),attrs[idf].toString())
                    else:
                        self.kmlStyle(style,feat,geom.wkbType())
                elif geom.wkbType() == QGis.WKBPolygon:
                    feat = folder.newpolygon()
                    polys = []
                    for g in qgisFeat.geometry().asPolygon():
                        poly = []
                        for p in g:
                            poly.append(SrsTrasform.transform(p))
                        polys.append(poly)
                    feat.innerboundaryis = polys
                    #feat.outerboundaryis = polys
                    if style.output['type'] != 'singleSymbol':
                        self.kmlStyle(style,feat,geom.wkbType(),attrs[idf].toString())
                    else:
                        self.kmlStyle(style,feat,geom.wkbType())
                else:
                    continue
                #elif geom.wkbType() == QGis.WKBMultiPolygon:
                    #feat = kml.newlinestring()
                    #inpoly = []
                    #outpoly = []
                    #wkbgeom = qgisFeat.geometry().asMultiPolygon()[0]
                    #for pol in wkbgeom:
                        #QgsGeometry.fromPoint(
                        #outpoly.append(SrsTrasform.transform(g))
                    #for g in wkbgeom[0][1]:
                        #inpoly.append(SrsTrasform.transform(g))                        
                    #feat.outerboundaryis = outpoly
                    #feat.innerboundaryis = inpoly
                    #if style.output['type'] != 'singleSymbol':
                        #self.kmlStyle(style,feat,layer.geometryType(),attrs[idf].toString())
                    #else:
                        #self.kmlStyle(style,feat,layer.geometryType())
                    
                #if self.dlg.ui.nameTableItem.currentIndex() != 0:
                nid = self.dlg.ui.tablelayers.cellWidget(nrow,1).currentIndex()
                if nid != 0:
                    n = attrs[nid-1].toString()
                    if n:
                        feat.name = n
                did = self.dlg.ui.tablelayers.cellWidget(nrow,2).currentIndex()
                if did != 0:
                    d = attrs[did-1].toString()
                    if d:
                        feat.description = d

            if outFormat == 0:
                kml.save(os.path.join(outPath,
                        '%s.kml' % layer.name()))
            elif outFormat == 1:
                outName = os.path.join(outPath, '%s.kmz' % layer.name())
                kml.savekmz(outName)
                if self.icon:
                    zf = zipfile.ZipFile(outName,mode='a')
                    for f in os.listdir(style.path): 
                        oldF = os.path.join(style.path,f)
                        newF = os.path.join('symbols_%s' % layer.name(),f)
                        zf.write(oldF,newF)
                    zf.close()
                    #shutil.rmtree(style.path)
                    
            nrow += 1