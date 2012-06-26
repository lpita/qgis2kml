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

from qgis2funz import *

class qgis2kmlClassStyle:
    """A class to create style of layer and the relative code"""
    def __init__(self,
                  layer
                ):
        #qgis layer
        self.layer = layer
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
        self.checkSymbol2(symbol)
        style = dictV2(symbol.symbolLayer(0).properties())
        #set fill color
        fillColor = style['color']
        self.output['fillcolor'] = self.rgb_to_hex(fillColor.split(','))
        #javascript code
        #if is point geometry add the point size
        if self.typeGeom == 0:
            self.output['size'] = style['size']
        elif self.typeGeom == 1:
            self.output['lineWidth'] = style['width']
        elif self.typeGeom == 2:
            #set stroke color
            self.output['lineWidth'] = style['width_border']
        self.output

    def uniqueVal2(self):
        """Return the javascript code for unique values symbology"""
        styleMap = self.renderer.categories()
        for cat in styleMap:
            z = unicode(cat.value().toString())
            self.output[z] = {}
            symbol = cat.symbol()
            self.checkSymbol2(symbol)
            style = dictV2(symbol.symbolLayer(0).properties())
            if self.typeGeom == 0:
                self.output[z]['size'] = style['size']
            elif self.typeGeom == 1:
                self.output[z]['lineWidth'] = style['width']
            elif self.typeGeom == 2:
                #set stroke color
                self.output[z]['lineWidth'] = style['width_border']
            fillColor = style['color']
            self.output[z]['fillcolor'] = self.rgb_to_hex(fillColor.split(','))

    def gradSymbol2(self):
        """Return the javascript code for graduated symbology"""
        symbolsGrad = self.renderer.symbols()
        self.ranges = self.renderer.ranges()
        value = 0
        # the higher number od styleMap
        for i in range(len(symbolsGrad)):
            nl = 'symb%i' % i
            self.output[nl] = {}
            self.output[nl]['min'] = self.ranges[i].lowerValue()
            self.output[nl]['max'] = self.ranges[i].upperValue()
            self.checkSymbol2(symbolsGrad[i])
            style = dictV2(symbolsGrad[i].symbolLayer(0).properties())
            fillColor = style['color']
            self.output[nl]['fillcolor'] = self.rgb_to_hex(fillColor.split(','))
            if self.typeGeom == 0:
                self.output[nl]['size'] = style['size']
            elif self.typeGeom == 1:
                self.output[nl]['lineWidth'] = style['width']
            elif self.typeGeom == 2:
                #set stroke color
                self.output[nl]['lineWidth'] = style['width_border']

    def checkSymbol2(self,symbol):
        """Check if a symbol has some problem for OpenLayers style"""
        #check how many symbols there are in a symbolset
        if symbol.symbolLayerCount() != 1:
            self.log += "WARNING: OGR2Layers support only a layer of the new symbology. "
            self.log += "         On vector <b>%s</b>, style type %s, first symbol is used <br />" % (
                        self.name, self.typeRend)

    def rgb_to_hex(self,rgb):
        new_rgb = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
        return '#%02x%02x%02x' % new_rgb
