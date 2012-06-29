# -*- coding: utf-8 -*-
#############################################
#       OGR2Layers Plugin (c)  for Quantum GIS
#       (c) Copyright Luca Delucchi 2010
#       Authors: Luca DELUCCHI
#       Email: lucadelucchi_at_gmail_dot_com
#
#############################################
#       OGR2Layers Plugin is licensed under the terms of GNU GPL 2              #
#       This program is free software; you can redistribute it and/or modify    #
#       it under the terms of the GNU General Public License as published by    #
#       the Free Software Foundation; either version 2 of the License, or       #
#       (at your option) any later version.                                     #
#       This program is distributed in the hope that it will be useful,         #
#       but WITHOUT ANY WARRANTY; without even implied warranty of              #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    # 
#       See the GNU General Public License for more details.                    #
#############################################


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import os, sys
import os2emxpath
import shutil

currentPath = os.path.dirname( __file__ )
sys.path.append( os.path.abspath(currentPath))

import simplekml

from qgis2funz import *

class qgis2kmlClassStyle:
    """A class to create style of layer and the relative code"""
    def __init__(self,
                  layer,
                  icon,
                  path
                ):
        #qgis layer
        self.layer = layer
        #set icon variable
        self.icon = icon
        self.path = os.path.join(path,'symbols_%s' % self.layer.name())
        if self.icon:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
            os.mkdir(self.path)
        # layer geometry type
        self.typeGeom = self.layer.geometryType()
        #layer name
        self.name = self.layer.name()
        # layer renderer
        if self.layer.renderer() != None:
            raise Exception, "Old symbology doen't support\n"
        elif self.layer.rendererV2() != None:
            self.renderer = self.layer.rendererV2()
            #type of rendering
            self.typeRend = str(self.renderer.type())
            if self.typeRend != 'singleSymbol':
                self.nameField = str(self.renderer.classAttribute())
            return self.typeV2()
        else:
            raise Exception, "There are some problem with the rendering\n"
        # data provider
        self.provider = self.layer.dataProvider()

    def typeV2(self):
        self.output = {}
        if self.typeRend == 'graduatedSymbol':
            self.output['type'] = 'graduatedSymbol'
            return self.gradSymbol2()
        #if Single Symbol
        elif self.typeRend == 'singleSymbol':
            self.output['type'] = 'singleSymbol'
            return self.singleSymbol2()
        #if Unique Value
        elif self.typeRend == 'categorizedSymbol':
            self.output['type'] = 'categorizedSymbol'
            return self.uniqueVal2()
        else:
            raise Exception, "There are some problem with the rendering\n"

    def singleSymbol2(self):
        """Return the javascript code for single symbology"""
        symbol = self.renderer.symbol()
        if self.icon:
            image = symbol.bigSymbolPreviewImage()
            imageName = os.path.join(self.path,'symbol.png')
            image.save(imageName,'png')
        self.checkSymbol2(symbol)
        style = dictV2(symbol.symbolLayer(0).properties())
        #set fill color
        color = self.rgb_to_hex(style['color'].split(','))
        #javascript code
        self.output['style'] = simplekml.Style()        
        #if is point geometry add the point size
        if self.typeGeom == 0:
            if self.icon:
                kmlIcon = simplekml.Icon()
                kmlIcon.href = os.path.join('.','symbols_%s' % self.layer.name(),
                                            'symbol.png')
                self.output['style'].iconstyle.icon = kmlIcon
            else:
                self.output['style'].iconstyle.color = color
                self.output['style'].iconstyle.scale = style['size']               
        elif self.typeGeom == 1:
            self.output['style'].linestyle.color = color
            self.output['style'].linestyle.width = style['width']
        elif self.typeGeom == 2:
            #set stroke color
            self.output['style'].polystyle.color = color
            self.output['style'].polystyle.outline = style['width_border']
            

    def uniqueVal2(self):
        """Return the javascript code for unique values symbology"""
        styleMap = self.renderer.categories()
        for cat in styleMap:
            # TODO fix for non UTF8 character
            #z = str(cat.value().toString().toUtf8())
            z = unicode(cat.value().toString())
            self.output[z] = {}
            self.output[z]['style'] = simplekml.Style()
            symbol = cat.symbol()
            if self.icon:
                image = symbol.bigSymbolPreviewImage()
                imageName = os.path.join(self.path,'%s.png' % z)
                image.save(imageName,'png')
            self.checkSymbol2(symbol)
            style = dictV2(symbol.symbolLayer(0).properties())
            color = self.rgb_to_hex(style['color'].split(','))            
            if self.typeGeom == 0:
                if self.icon:
                    kmlIcon = simplekml.Icon()
                    kmlIcon.href = os.path.join('.','symbols_%s' % self.layer.name(),
                                                '%s.png' % z)
                    self.output[z]['style'].iconstyle.icon = kmlIcon
                else:
                    self.output[z]['style'].iconstyle.color = color
                    self.output[z]['style'].iconstyle.scale = style['size']
            elif self.typeGeom == 1:
                self.output[z]['style'].linestyle.color = color
                self.output[z]['style'].linestyle.width = style['width']
            elif self.typeGeom == 2:
                self.output[z]['style'].polystyle.outline = style['width_border']
                self.output[z]['style'].polystyle.color = color

    def gradSymbol2(self):
        """Return the javascript code for graduated symbology"""
        symbolsGrad = self.renderer.symbols()
        self.ranges = self.renderer.ranges()
        value = 0
        # the higher number od styleMap
        for i in range(len(symbolsGrad)):
            symbol = symbolsGrad[i]
            nl = 'symb%i' % i
            self.output[nl] = {}
            self.output[nl]['min'] = self.ranges[i].lowerValue()
            self.output[nl]['max'] = self.ranges[i].upperValue()
            self.output[nl]['style'] = simplekml.Style()
            if self.icon:
                image = symbol.bigSymbolPreviewImage()
                imageName = os.path.join(self.path,'%s.png' % nl)
                image.save(imageName,'png')
            self.checkSymbol2(symbol)
            style = dictV2(symbol.symbolLayer(0).properties())
            color = self.rgb_to_hex(style['color'].split(','))
            if self.typeGeom == 0:
                if self.icon:
                    kmlIcon = simplekml.Icon()
                    kmlIcon.href = os.path.join('.','symbols_%s' % self.layer.name(),
                                                '%s.png' % nl)
                    self.output[nl]['style'].iconstyle.icon = kmlIcon
                else:
                    self.output[nl]['style'].iconstyle.color = color
                    self.output[nl]['style'].iconstyle.scale = style['size']
            elif self.typeGeom == 1:
                self.output[nl]['style'].linestyle.color = color
                self.output[nl]['style'].linestyle.width = style['width']
            elif self.typeGeom == 2:
                self.output[nl]['style'].polystyle.outline = style['width_border']
                self.output[nl]['style'].polystyle.color = color

    def checkSymbol2(self,symbol):
        """Check if a symbol has some problem for OpenLayers style"""
        #check how many symbols there are in a symbolset
        if symbol.symbolLayerCount() != 1:
            self.log += "WARNING: qgis2kml support only a layer of the new symbology. "
            self.log += "         On vector <b>%s</b>, style type %s, first symbol is used <br />" % (
                        self.name, self.typeRend)

    def rgb_to_hex(self,rgb):
        new_rgb = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
        return '#%02x%02x%02x' % new_rgb
