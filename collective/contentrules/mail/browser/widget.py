# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
from zope.component import getUtility
from zope.app.form.browser.itemswidgets import DropdownWidget
from zope.component.interfaces import ComponentLookupError

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from kss.core import KSSView

from collective.contentrules.mail.interfaces import IMailModel


class ModelKSSView(KSSView):
    help_template = ViewPageTemplateFile("templates/model.pt")

    def updateModelDescription(self, model_id=''):
        # Get model and display help
        try:
            model = getUtility(IMailModel, model_id)
        except ComponentLookupError:
            model = None

        help = ""

        if model is not None:
            help = self.help_template(fields=model.fields)

        core = self.getCommandSet('core')
        core.replaceInnerHTML('#mail-model .modelDescription', help)
        return self.render()


class ModelWidget(DropdownWidget):

    help_template = ViewPageTemplateFile("templates/model.pt")

    def __init__(self, field, request):
        """Initialize the widget."""
        super(ModelWidget, self).__init__(field,
            field.vocabulary, request)

    def __call__(self):
        """See IBrowserWidget."""
        value = self._getFormValue()
        contents = []
        contents.append(self._div('value', self.renderValue(value)))
        contents.append(self._emptyMarker())

        # Get model and display model description
        # If no model selected, get the first value of vocabulary
        help = ""

        if not value and len(self.vocabulary):
            value = self.vocabulary._terms[0].value

        # Get model
        if value:
            try:
                model = getUtility(IMailModel, value)
            except ComponentLookupError:
                model = None

            if model is not None:
                help = self.help_template(fields=model.fields)

        contents.append(self._div("modelDescription", help))
        return self._div(self.cssClass, "\n".join(contents), id="mail-model")
