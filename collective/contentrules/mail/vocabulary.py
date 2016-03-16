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
from collective.contentrules.mail.interfaces import IMailModel
from collective.contentrules.mail import MessageFactory as _
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class ModelVocabulary(object):
    """Vocabulary factory listing all mail models
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = [SimpleTerm(name, title=utility.title)
                 for name, utility in getUtilitiesFor(IMailModel)]
        return SimpleVocabulary(terms)


ModelVocabularyFactory = ModelVocabulary()


class MimetypeVocabulary(object):
    """Vocabulary factory listing mail mimetypes
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = (
            SimpleTerm(
                u"plain",
                title=_(u"text/plain", )),
            SimpleTerm(
                u"html",
                title=_(u"text/html", )),
            )

        return SimpleVocabulary(terms)


MimetypeVocabularyFactory = MimetypeVocabulary()
