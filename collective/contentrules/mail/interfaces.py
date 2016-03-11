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
from zope.interface import Interface
from zope.schema import TextLine, Object, List, Tuple

from collective.contentrules.mail import MessageFactory as _


class IMailModel(Interface):
    """A named utility providing a mail model.

    The mail content rule will allow the user ot pick a mail model based on
    a vocabulary of all named utilities providing this interface. When the
    content rule action is executed, the object being acted upon will be
    adapted to the interface specified under `replacer_interface`.
    Substitutions will then be made based on variables matching field names
    (e.g. "${foobar}" matches the `foobar` field). The substituted values
    are obtained from the adapter.
    """

    title = TextLine(title=_(u"A friendly name for model", ))

    replacer_interface = Object(
        title=_(u"Mail replacer schema"),
        description=_(u"Interface providing word substitution in " \
                        "mail fields: source, recipients, subject, text"),
        schema=Interface)

    fields = List(
        title=_(u"Fields help text"),
        description=_(u"Exposes the variables provided by the replacer"),
        value_type=Tuple(title=_(u"Pair of (key, help text,)"),
                         value_type=TextLine(title=_(u"Name or help text"))))


class IMailReplacer(Interface):
    """Interface providing variables which can be used in mail fields:
    source, recipients, subject, text. This is the default implementation,
    which should work on any CMF content providing the IDublinCore interface.

    It is possible to extend this with other attributes and provide a new
    IMailModel utility with a different interface provided as the
    `replacer_interface`.
    """

    id = TextLine(title=_(u"Id of content", ))

    title = TextLine(title=_(u"Title of content", ))

    description = TextLine(title=_(u"Description of content", ))

    url = TextLine(title=_(u"URL to access content", ))

    relative_url = TextLine(
        title=_(u"Relative URL from portal to access content", ))

    portal_url = TextLine(title=_(u"URL of portal", ))

    owner_id = TextLine(title=_(u"Login of content ower", ))

    owner_fullname = TextLine(title=_(u"Full name of content owner", ))

    owner_emails = TextLine(
        title=_(u"Emails of users having Owner role on content", ))

    reader_emails = TextLine(
            title=_(u"Emails of users having Reader role on content", ))

    contributor_emails = TextLine(
            title=_(u"Emails of users having Contributor role on content", ))

    editor_emails = TextLine(
            title=_(u"Emails of users having Editor role on content", ))

    reviewer_emails = TextLine(
            title=_(u"Emails of users having Reviewer role on content", ))

    default_from_email = TextLine(title=_(u"Email address of default sender", ))

    default_from_name = TextLine(title=_(u"Full name of default sender", ))

    review_state = TextLine(title=_(u"State of content", ))
