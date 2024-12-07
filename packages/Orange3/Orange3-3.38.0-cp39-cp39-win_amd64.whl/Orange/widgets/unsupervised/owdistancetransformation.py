from orangecanvas.utils.localization.si import plsi, plsi_sz, z_besedo
from orangecanvas.utils.localization import Translator  # pylint: disable=wrong-import-order
_tr = Translator("Orange", "biolab.si", "Orange")
del Translator
import numpy as np

from Orange.util import scale
from Orange.misc import DistMatrix
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import Input, Output


class OWDistanceTransformation(widget.OWWidget):
    name = _tr.m[2726, "Distance Transformation"]
    description = _tr.m[2727, "Transform distances according to selected criteria."]
    icon = "icons/DistancesTransformation.svg"
    keywords = _tr.m[2728, "distance transformation"]

    class Inputs:
        distances = Input(_tr.m[2729, "Distances"], DistMatrix)

    class Outputs:
        distances = Output(_tr.m[2730, "Distances"], DistMatrix, dynamic=False)

    want_main_area = False
    resizing_enabled = False

    normalization_method = settings.Setting(0)
    inversion_method = settings.Setting(0)
    autocommit = settings.Setting(True)

    normalization_options = (
        (_tr.m[2731, "No normalization"], lambda x: x),
        (_tr.m[2732, "To interval [0, 1]"], lambda x: scale(x, min=0, max=1)),
        (_tr.m[2733, "To interval [-1, 1]"], lambda x: scale(x, min=-1, max=1)),
        (_tr.m[2734, "Sigmoid function: 1/(1+exp(-X))"], lambda x: 1/(1+np.exp(-x))),
    )

    inversion_options = (
        (_tr.m[2735, "No inversion"], lambda x: x),
        ("-X", lambda x: -x),
        ("1 - X", lambda x: 1-x),
        ("max(X) - X", lambda x: np.max(x) - x),
        ("1/X", lambda x: 1/x),
    )

    def __init__(self):
        super().__init__()

        self.data = None

        gui.radioButtons(self.controlArea, self, "normalization_method",
                         box=_tr.m[2736, "Normalization"],
                         btnLabels=[x[0] for x in self.normalization_options],
                         callback=self._invalidate)

        gui.radioButtons(self.controlArea, self, "inversion_method",
                         box=_tr.m[2737, "Inversion"],
                         btnLabels=[x[0] for x in self.inversion_options],
                         callback=self._invalidate)

        gui.auto_apply(self.buttonsArea, self, "autocommit")

    @Inputs.distances
    def set_data(self, data):
        self.data = data
        self.commit.now()

    @gui.deferred
    def commit(self):
        distances = self.data
        if distances is not None:
            # normalize
            norm = self.normalization_options[self.normalization_method][1]
            distances = norm(distances)

            # invert
            inv = self.inversion_options[self.inversion_method][1]
            distances = inv(distances)
        self.Outputs.distances.send(distances)

    def send_report(self):
        norm, normopt = self.normalization_method, self.normalization_options
        inv, invopt = self.inversion_method, self.inversion_options
        parts = []
        if inv:
            parts.append(_tr.m[2738, 'inversion ({})'].format(invopt[inv][0]))
        if norm:
            parts.append(_tr.m[2739, 'normalization ({})'].format(normopt[norm][0]))
        self.report_items(
            _tr.m[2740, 'Model parameters'],
            {_tr.m[2741, 'Transformation']: ', '.join(parts).capitalize() or _tr.m[2742, 'None']})

    def _invalidate(self):
        self.commit.deferred()


if __name__ == "__main__":  # pragma: no cover
    import Orange.distance
    data = Orange.data.Table("iris")
    dist = Orange.distance.Euclidean(data)
    WidgetPreview(OWDistanceTransformation).run(dist)
