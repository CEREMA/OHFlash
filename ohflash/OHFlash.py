# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OHFlash
                                 A QGIS plugin
 Ce plugin permet d'itérer sur tous les éléments d'une couche en zoomant dessus et en éditant une colonne de cette couche selon le choix de l'utilisateur. Initialement développé pour l'édition des ouvrages hydrauliques, ce plugin peut être utilisé pour toute autre couche.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-05-17
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Cerema
        email                : nassim.cheikh@cerema.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QTimer
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QMessageBox
from PyQt5.QtWidgets import QDialog, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit, QGridLayout, QLabel, QScrollArea, QWidget
from PyQt5 import QtWidgets, uic
from qgis.core import QgsProject, edit, QgsFeatureRequest, QgsExpression, QgsVectorLayer, QgsMapLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .OHFlash_dialog import OHFlashDialog
from .ohflash_dialog2 import Ui_OHFlashDialog2
from .ohflash_dialog3 import Ui_OHFlashDialog3
import os.path
import qgis.utils
from qgis.gui import QgsLayerTreeView

class OHFlash:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'OHFlash_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&OH Flash')

        
        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        # Initialize selected_only attribute
        self.selected_only = False
        
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('OHFlash', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/OHFlash/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'OHFlash'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

        

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&OH Flash'),
                action)
            self.iface.removeToolBarIcon(action)

    def populate_layers(self):
        self.dlg.layerComboBox.clear()
        layers = QgsProject.instance().mapLayers().values()
        
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                self.dlg.layerComboBox.addItem(layer.name(), layer)

    
    def handle_selected_only_change(self, state):
        if state == Qt.Checked:
            self.selected_only = True
        else:
            self.selected_only = False

    def handle_zoom_extent(self, checked):
        if checked:
            self.zoom_extent = True
        else:
            self.zoom_extent = False
        
    def populate_fields(self):
        self.dlg.fieldComboBox.clear()
        layer = self.dlg.layerComboBox.currentData()
        if layer:
            fields = layer.fields()
            for field in fields:
                if field.name() != "fid":
                    self.dlg.fieldComboBox.addItem(field.name())

    def get_selected_layer_and_field(self):
        layer = self.dlg.layerComboBox.currentData()
        field = self.dlg.fieldComboBox.currentText()
        return layer, field

    def on_layers_removed(self, layer_ids):
        self.populate_layers()
        
    def accept(self):
        
        # Close dialog
        self.dlg.close()
        
    def accept_okButton(self):
        """Accept and proceed to the next dialog"""
        self.dlg.close()
        self.open_second_dialog()

    def close_plugin(self):
        """Close the dialog and stop the plugin"""
        if self.whichDlg == 1:
            QTimer.singleShot(0, self.dlg.close)
        elif self.whichDlg == 2:
            QTimer.singleShot(0, self.dlg2.close)
        elif self.whichDlg == 3:
            QTimer.singleShot(0, self.variable_dialog.close)
        elif self.whichDlg == 4:
            QTimer.singleShot(0, self.dlg3.close)
            
        self.iface.messageBar().pushMessage("A bientôt sur OH Flash!", duration=3)
        
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = OHFlashDialog()
            # Connect populate_layers to QGIS
            # Connect signal to update layer combo box
            self.dlg.selectionBox.stateChanged.connect(self.handle_selected_only_change)
            QgsProject.instance().layersAdded.connect(self.populate_layers)
            QgsProject.instance().layersRemoved.connect(self.populate_layers)
            # Connect signal to quit plugin
            self.whichDlg = 1
            self.dlg.quitButton1.clicked.connect(self.close_plugin)
            # Connect signal for layer selection change
            self.dlg.layerComboBox.currentIndexChanged.connect(self.populate_fields)
            # Connect the OK button
            self.dlg.okButton.clicked.connect(self.accept_okButton)
            # Populate layers
            self.populate_layers()
            
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        

    def filtre(self, layer, field):
        filtre = self.ui2.optionsComboBox.currentText()
        # Determine the editing condition according to the user's choice
        if filtre == 'Tous les elements':
            # If selected_only is True, use only the selected features
            if self.selected_only:
                features = layer.selectedFeatures()
            else:
                features = layer.getFeatures()
        else:
            # If selected_only is True, filter the selected features
            if self.selected_only:
                features = [f for f in layer.selectedFeatures() if f[field] is None]
            else:
                # Create an expression to filter elements with an empty "AGARDER" column
                expression = QgsExpression(f'{field} IS NULL')
                features = layer.getFeatures(QgsFeatureRequest(expression))
        return features
    
    def handle_filter_change(self):
        layer, field = self.get_selected_layer_and_field()
        self.filtre(layer, field)
        
    def treatment_values(self):
        val1 = self.ui2.lineEditVal1.text()
        val2 = self.ui2.lineEditVal2.text()
        val3 = self.ui2.lineEditVal3.text()
        return val1, val2, val3

        
    def open_second_dialog(self):
        self.whichDlg = 2
        
        self.dlg2 = QtWidgets.QDialog()
        self.ui2 = Ui_OHFlashDialog2()
        self.ui2.setupUi(self.dlg2)
        self.ui2.optionsComboBox.clear()
        
        layer, field = self.get_selected_layer_and_field()
        self.ui2.optionsComboBox.addItem('Tous les elements')
        self.ui2.optionsComboBox.addItem(f'Uniquement ceux avec la colonne {field} vide')

        self.filtre(layer,field)  # Updates the filter after adding options
        
        self.ui2.optionsComboBox.currentIndexChanged.connect(self.handle_filter_change)
        self.zoom_extent = self.ui2.zoomExtent.isChecked()
        print("Etat Initial ", self.zoom_extent)
        self.ui2.zoomExtent.toggled.connect(self.handle_zoom_extent)
        self.ui2.okButtonOptions.clicked.connect(self.dlg2.accept)
        
        # Connect the OK button
        self.dlg2.show()
        result = self.dlg2.exec_()
        if result:
            self.layer, self.field = self.get_selected_layer_and_field()
            self.features = list(self.filtre(layer, field))
            nbFeatures = len(list(self.features))
            if nbFeatures == 0:
                self.dlg2.close()
                QMessageBox.information(None, "Info", f"Il n'y a aucun élément vide dans la colonne {field}.")
                self.iface.messageBar().pushMessage("A bientôt sur OH Flash!", duration=3)
            else:
                # Recovery of user-entered zoom
                if self.zoom_extent == True:
                    if self.ui2.dezoom.text() == "":
                        self.dezoom = 0.2
                    else:
                        self.dezoom = int(self.ui2.dezoom.text())/100
                else:
                    if self.ui2.zoomScale.text() == "":
                        self.zoom_scale = 500
                    else:
                        self.zoom_scale = int(self.ui2.zoomScale.text())
                self.NumValue = int(self.ui2.NumValue.text())
                self.open_variable_dialog()
            pass

    def open_variable_dialog(self):
        self.whichDlg = 3
        
        # Ouvrir une nouvelle boîte de dialogue pour définir les variables
        self.variable_dialog = QDialog(self.dlg)
        self.variable_dialog.setWindowTitle("Entrez les noms des variables")
        layout = QVBoxLayout(self.variable_dialog)

        # Add instruction label
        instruction_label = QLabel("Veuillez renseigner vos variables:")
        layout.addWidget(instruction_label)

        # Create a scroll area to hold the variable input fields
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QFormLayout(scroll_content)
    
        # Créer dynamiquement les QComboBox
        self.line_edits = []
        for i in range(self.NumValue):
            line_edit = QLineEdit(self.variable_dialog)
            line_edit.setPlaceholderText(f"Variable {i + 1}")
            layout.addWidget(line_edit)
            self.line_edits.append(line_edit)
            scroll_layout.addRow(line_edit)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Ajouter un bouton pour valider
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self.variable_dialog)
        cancel_button = QPushButton("Cancel", self.variable_dialog)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(self.variable_dialog.accept)
        cancel_button.clicked.connect(self.variable_dialog.accept)

        self.variable_dialog.setLayout(layout)
        self.variable_dialog.exec_()

        if self.variable_dialog.result() == QDialog.Accepted:
            self.process_line_edit_values()
            self.open_third_dialog()

    def process_line_edit_values(self):
        # Traitement des valeurs définies dans les QLineEdit
        self.values = []
        for index, line_edit in enumerate(self.line_edits):
            value = line_edit.text()
            self.values.append(value)
            

    def selection(self):
        self.layer.removeSelection()
        self.layer.select(self.feature.id())
        
    def open_third_dialog(self):
        self.whichDlg = 4
        
        self.dlg3 = QtWidgets.QDialog()
        self.ui3 = Ui_OHFlashDialog3()
        self.ui3.setupUi(self.dlg3)

        # Ajout d'un QScrollArea
        scroll_area = QtWidgets.QScrollArea(self.dlg3)
        scroll_area.setWidgetResizable(True)
        button_container_widget = QtWidgets.QWidget()
        scroll_area.setWidget(button_container_widget)
        
        # Initialisation des boutons dynamiques
        grid_layout = QGridLayout(button_container_widget)
        self.dynamic_buttons = []

        button_style = """
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #A0A0A0;
                border-style: inset;
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
        """
        
        for index, value in enumerate(self.values):
            button = QPushButton(value, self.dlg3)
            button.clicked.connect(self.show_next_feature)
            button.setStyleSheet(button_style)
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            button.setStyleSheet(button_style)

            # Calculer la position du bouton dans la grille
            row = index // 3
            col = index % 3
            # Ajouter le bouton au layout
            grid_layout.addWidget(button, row, col)
            self.dynamic_buttons.append(button)
        
        #A voir s'il ne faut pas indiquer juste le grand layout
        self.ui3.buttonContainer.addWidget(scroll_area)
    
##        self.ui3.yesButton.setText(val1)
##        self.ui3.noButton.setText(val2)
##        self.ui3.otherButton.setText(val3)

        self.nbFeatures = len(list(self.layer.getFeatures()))
        self.nbIteration = self.nbFeatures - len(self.features)
        
        self.ui3.quitButton.clicked.connect(self.close_plugin)
        self.ui3.prevButton.clicked.connect(self.prev_button_clicked)
        
        # Initialize iteration on layer elements
        self.current_feature_index = 0
        self.ui3.prevButton.setEnabled(False)
        self.feature = self.features[self.current_feature_index]
        
        if self.zoom_extent == True:
            self.fun_zoom_extent()
        else:
            self.zoom()

        self.selection()
        self.ui3.IDlabel.setText(f"Traitement de l'élément ID = {self.feature.id()}")

        # Initializing the progress bar
        self.ui3.progressBar.setMaximum(len(self.features))
        self.ui3.progressBar.setValue(self.current_feature_index)

        # Apply an advanced style to the progress bar
        self.ui3.progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                padding: 1px;
                background: #E0E0E0;
            }
            QProgressBar::chunk {
                background-color: #76c7c0;
                width: 1px; /* Définit la largeur des morceaux pour éviter plusieurs morceaux */
                margin: 0px; /* Enlève la marge entre les morceaux */
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #66FF66, stop: 1 #009900
                );
            }
        """)
        
        quit_button_style = """
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #A0A0A0;
                border-style: inset;
            }
            QPushButton:hover {
                background-color: #FFCCCC;
            }
        """

        prev_button_style = """
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #A0A0A0;
                border-style: inset;
            }
            QPushButton:hover {
                background-color: #FFDAB9;
            }
        """

        self.ui3.quitButton.setStyleSheet(quit_button_style)
        self.ui3.prevButton.setStyleSheet(prev_button_style)

        #self.dlg3.resize(800, 600)
        self.dlg3.show()
        result = self.dlg3.exec_()

        if result:
            pass
    
    def show_next_feature(self):
        # User-pressed button recovery
        choice = self.dlg3.sender()
        # Treatment of the layer
        self.field_treatment(choice)
        self.current_feature_index += 1
        
        self.ui3.prevButton.setEnabled(True)
            
        self.nbIteration += 1
        
        if self.current_feature_index < len(self.features):
            self.feature = self.features[self.current_feature_index]
            if self.zoom_extent == True:
                self.fun_zoom_extent()
            else:
                self.zoom()
            self.selection()
            self.ui3.IDlabel.setText(f"Traitement de l'élément ID = {self.feature.id()}")
            self.ui3.progressBar.setValue(self.current_feature_index)  # Mise à jour de la barre de progression
        else:
            self.layer.removeSelection()
            self.ui3.IDlabel.setText("Tous les éléments ont été traités")
            for button in self.dynamic_buttons:
                button.setEnabled(False)
            self.ui3.progressBar.setValue(self.current_feature_index)  # Mise à jour de la barre de progression
            self.dlg3.close()
            QMessageBox.information(None, "Info", "Tous les éléments ont été traités.")

    def prev_button_clicked(self):
        if self.current_feature_index > 0:
            self.current_feature_index -= 1
            self.feature = self.features[self.current_feature_index]
            if self.zoom_extent == True:
                self.fun_zoom_extent()
            else:
                self.zoom()
            self.selection()
            self.ui3.IDlabel.setText(f"Traitement de l'élément ID = {self.feature.id()}")
            self.ui3.progressBar.setValue(self.current_feature_index)
            if self.current_feature_index == 0:
                self.ui3.prevButton.setEnabled(False)
        
    def zoom(self):
        # Zoom on the element
        self.canvas = qgis.utils.iface.mapCanvas()
        self.canvas.setDestinationCrs(self.layer.crs())
        self.canvas.setExtent(self.feature.geometry().boundingBox())
        self.canvas.zoomScale(self.zoom_scale)

    def fun_zoom_extent(self):
        # Obtenir le canevas de la carte QGIS
        self.canvas = qgis.utils.iface.mapCanvas()
        
        # Définir le CRS de destination sur celui de la couche
        self.canvas.setDestinationCrs(self.layer.crs())
        
        # Obtenir l'étendue de l'élément
        bounding_box = self.feature.geometry().boundingBox()
        
        # Calculer la marge de 10%
        width_margin = bounding_box.width() * self.dezoom
        height_margin = bounding_box.height() * self.dezoom
        
        # Étendre la boîte englobante avec la marge
        expanded_bounding_box = bounding_box
        expanded_bounding_box.setXMinimum(bounding_box.xMinimum() - width_margin)
        expanded_bounding_box.setXMaximum(bounding_box.xMaximum() + width_margin)
        expanded_bounding_box.setYMinimum(bounding_box.yMinimum() - height_margin)
        expanded_bounding_box.setYMaximum(bounding_box.yMaximum() + height_margin)
        
        # Définir l'étendue du canevas sur celle de l'élément étendue
        self.canvas.setExtent(expanded_bounding_box)
        
        # Actualiser le canevas pour appliquer les changements
        self.canvas.refresh()

    def field_treatment(self, choice):
            
        values = self.values

        val = choice.text()

        if not self.layer.isEditable():
            
            with edit(self.layer):
                self.feature.setAttribute(self.field, val)
                self.layer.updateFeature(self.feature)
            
        else:
            
            field_index = self.layer.fields().indexFromName(self.field)
            self.layer.changeAttributeValue(self.feature.id(), field_index, val)
            
        if self.current_feature_index == len(self.features) - 1:
            self.layer.commitChanges()
       
