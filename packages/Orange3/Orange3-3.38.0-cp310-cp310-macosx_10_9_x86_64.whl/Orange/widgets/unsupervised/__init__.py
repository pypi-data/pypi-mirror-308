"""
============
Unsupervised
============

Unsupervised learning.

"""
from orangecanvas.utils.localization.si import plsi, plsi_sz, z_besedo
from orangecanvas.utils.localization import Translator  # pylint: disable=wrong-import-order
_tr = Translator("Orange", "biolab.si", "Orange")
del Translator

NAME = _tr.m[2558, "Unsupervised"]

ID = "orange.widgets.unsupervised"

DESCRIPTION = _tr.m[2559, "Unsupervised learning."]

BACKGROUND = "#CAE1EF"

ICON = "icons/Category-Unsupervised.svg"

PRIORITY = 6
