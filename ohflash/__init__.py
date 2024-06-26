# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OHFlash
                                 A QGIS plugin
 Ce plugin permet d'itérer sur tous les éléments d'une couche en zoomant dessus et en éditant une colonne de cette couche selon le choix de l'utilisateur. Initialement développé pour l'édition des ouvrages hydrauliques, ce plugin peut être utilisé pour toute autre couche.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-05-17
        copyright            : (C) 2024 by Cerema
        email                : nassim.cheikh@cerema.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OHFlash class from file OHFlash.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .OHFlash import OHFlash
    return OHFlash(iface)
