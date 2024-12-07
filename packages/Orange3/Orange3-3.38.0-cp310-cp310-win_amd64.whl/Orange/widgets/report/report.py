from orangecanvas.utils.localization.si import plsi, plsi_sz, z_besedo
from orangecanvas.utils.localization import Translator  # pylint: disable=wrong-import-order
_tr = Translator("Orange", "biolab.si", "Orange")
del Translator
from collections import OrderedDict

from orangewidget.report.report import *
from orangewidget.report import report as __report

from Orange.data.sql.table import SqlTable

__all__ = __report.__all__ + [
    "DataReport", "describe_data", "describe_data_brief",
    "describe_domain", "describe_domain_brief",
]

del __report


class DataReport(Report):
    """
    A report subclass that adds data related methods to the Report.
    """

    def report_data(self, name, data=None):
        """
        Add description of data table to the report.

        See :obj:`describe_data` for details.

        The first argument, `name` can be omitted.

        :param name: report section name (can be omitted)
        :type name: str or tuple or OrderedDict
        :param data: data whose description is added to the report
        :type data: Orange.data.Table
        """

        name, data = self._fix_args(name, data)
        self.report_items(name, describe_data(data))

    def report_domain(self, name, domain=None):
        """
        Add description of domain to the report.

        See :obj:`describe_domain` for details.

        The first argument, `name` can be omitted.

        :param name: report section name (can be omitted)
        :type name: str or tuple or OrderedDict
        :param domain: domain whose description is added to the report
        :type domain: Orange.data.Domain
        """
        name, domain = self._fix_args(name, domain)
        self.report_items(name, describe_domain(domain))

    def report_data_brief(self, name, data=None):
        """
        Add description of data table to the report.

        See :obj:`describe_data_brief` for details.

        The first argument, `name` can be omitted.

        :param name: report section name (can be omitted)
        :type name: str or tuple or OrderedDict
        :param data: data whose description is added to the report
        :type data: Orange.data.Table
        """
        name, data = self._fix_args(name, data)
        self.report_items(name, describe_data_brief(data))


# For backwards compatibility Report shadows the one from the base
Report = DataReport


def describe_domain(domain):
    """
    Return an :obj:`OrderedDict` describing a domain

    Description contains keys "Features", "Meta attributes" and "Targets"
    with the corresponding clipped lists of names. If the domain contains no
    meta attributes or targets, the value is `False`, which prevents it from
    being rendered by :obj:`~Orange.widgets.report.render_items`.

    :param domain: domain
    :type domain: Orange.data.Domain
    :rtype: OrderedDict
    """

    def clip_attrs(items, desc):
        s = clipped_list([a.name for a in items], 1000)
        nitems = len(items)
        if nitems >= 10:
            s += _tr.e(_tr.c(2537, f" (total: {nitems} {desc})"))
        return s

    return OrderedDict(
        [(_tr.m[2538, "Features"], clip_attrs(domain.attributes, _tr.e(_tr.c(2539, "features")))),
         (_tr.m[2540, "Meta attributes"], bool(domain.metas) and
          clip_attrs(domain.metas, _tr.e(_tr.c(2541, "meta attributes")))),
         (_tr.m[2542, "Target"], bool(domain.class_vars) and
          clip_attrs(domain.class_vars, _tr.m[2543, "target variables"]))])


def describe_data(data):
    """
    Return an :obj:`OrderedDict` describing the data

    Description contains keys "Data instances" (with the number of instances)
    and "Features", "Meta attributes" and "Targets" with the corresponding
    clipped lists of names. If the domain contains no meta attributes or
    targets, the value is `False`, which prevents it from being rendered.

    :param data: data
    :type data: Orange.data.Table
    :rtype: OrderedDict
    """
    items = OrderedDict()
    if data is None:
        return items
    if isinstance(data, SqlTable):
        items[_tr.m[2544, "Data instances"]] = data.approx_len()
    else:
        items[_tr.m[2545, "Data instances"]] = len(data)
    items.update(describe_domain(data.domain))
    return items


def describe_domain_brief(domain):
    """
    Return an :obj:`OrderedDict` with the number of features, metas and classes

    Description contains "Features" and "Meta attributes" with the number of
    featuers, and "Targets" that contains either a name, if there is a single
    target, or the number of targets if there are multiple.

    :param domain: data
    :type domain: Orange.data.Domain
    :rtype: OrderedDict
    """
    items = OrderedDict()
    if domain is None:
        return items
    items[_tr.m[2546, "Features"]] = len(domain.attributes) or _tr.m[2547, "None"]
    items[_tr.m[2548, "Meta attributes"]] = len(domain.metas) or _tr.m[2549, "None"]
    if domain.has_discrete_class:
        items[_tr.m[2550, "Target"]] = _tr.m[2551, "Class '{}'"].format(domain.class_var.name)
    elif domain.has_continuous_class:
        items[_tr.m[2552, "Target"]] = _tr.m[2553, "Numeric variable '{}'"]. \
            format(domain.class_var.name)
    elif domain.class_vars:
        items[_tr.m[2554, "Targets"]] = len(domain.class_vars)
    else:
        items[_tr.m[2555, "Targets"]] = False
    return items


def describe_data_brief(data):
    """
    Return an :obj:`OrderedDict` with a brief description of data.

    Description contains keys "Data instances" with the number of instances,
    "Features" and "Meta attributes" with the corresponding numbers, and
    "Targets", which contains a name, if there is a single target, or the
    number of targets if there are multiple.

    :param data: data
    :type data: Orange.data.Table
    :rtype: OrderedDict
    """
    items = OrderedDict()
    if data is None:
        return items
    if isinstance(data, SqlTable):
        items[_tr.m[2556, "Data instances"]] = data.approx_len()
    else:
        items[_tr.m[2557, "Data instances"]] = len(data)
    items.update(describe_domain_brief(data.domain))
    return items
