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

from zope.interface import implements
from zope.schema import getFieldsInOrder

from collective.contentrules.mail.interfaces import IMailModel
from collective.contentrules.mail.interfaces import IMailReplacer
from collective.contentrules.mail import MessageFactory as _


class MailModel(object):
    """A mail model described by interface.

    Create instances of this (as shown for DefaultMailModel below) and
    register these as unique named utilities providing IMailModel.
    """

    implements(IMailModel)

    def __init__(self, title, replacer_interface):
        self.title = title
        self.replacer_interface = replacer_interface

    @property
    def fields(self):
        fields = []

        # List of variables provided by replacer interface
        for name, field in getFieldsInOrder(self.replacer_interface):
            fields.append((name, field.title))

        return fields

# The default mail model, which uses the default mail replacer.
DefaultMailModel = MailModel(title=_(u"Standard model for plone content"),
                             replacer_interface=IMailReplacer)
