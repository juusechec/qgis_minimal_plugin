from PyQt5 import uic

import os
from qgis.core import QgsVectorLayer, QgsProject

from PyQt5.QtWidgets import *

DialogBase, DialogType = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'geometry_operation_dialog_base.ui'))

class GeometryOperationDialog (DialogType, DialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.bufferButton.clicked.connect(self.buttonBufferClicked)
        self.centroidButton.clicked.connect(self.buttonCentroidClicked)

    def loadLayers(self):
        self.layerComboBox.clear()
        for layer in QgsProject.instance().mapLayers().values():
            self.layerComboBox.addItem(layer.name(), layer)

    def buffer(self):
        layer = self.layerComboBox.currentData()
        uri = 'Polygon?crs={authid}&index=yes'.format(authid=layer.crs().authid())
        new_layer = QgsVectorLayer(uri, 'buffer', 'memory')
        QgsProject.instance().addMapLayer(new_layer)
        # segunda parte
        buffer_size = self.spinBox.value()
        new_layer.startEditing()

        for field in layer.fields():
            new_layer.addAttribute(field)

        for feature in layer.getFeatures():
            geom = feature.geometry().buffer(buffer_size, 5)

            feature.setGeometry(geom)
            new_layer.addFeature(feature)

        new_layer.commitChanges()

    def buttonBufferClicked(self):
        QMessageBox.information(None, u'Minimal plugin', u'Lo voy a hacer!')
        self.buffer()

    def centroid(self):
        layer = self.layerComboBox.currentData()
        uri = 'Point?crs={authid}&index=yes'.format(authid=layer.crs().authid())
        new_layer = QgsVectorLayer(uri, 'centroid', 'memory')
        QgsProject.instance().addMapLayer(new_layer)
        # segunda parte
        new_layer.startEditing()

        for field in layer.fields():
            new_layer.addAttribute(field)

        for feature in layer.getFeatures():
            geom = feature.geometry().centroid()

            feature.setGeometry(geom)
            new_layer.addFeature(feature)

        new_layer.commitChanges()

    def buttonCentroidClicked(self):
        QMessageBox.information(None, u'Minimal plugin', u'Lo voy a hacer :D')
        self.centroid()
