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
from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface
from zope.interface import implements
from zope.formlib import form
from zope.schema import TextLine
from zope.schema import Text
from zope.schema import Choice
from zope.schema import getFieldNamesInOrder

from Products.CMFCore.utils import getToolByName

from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.contentrules.rule.interfaces import IExecutable

from collective.contentrules.mail import MessageFactory as _
from collective.contentrules.mail import LOG
from collective.contentrules.mail.browser.widget import ModelWidget
from collective.contentrules.mail.interfaces import IMailModel

from smtplib import SMTPException
from Products.MailHost.MailHost import MailHostError


class IMailAction(Interface):
    """Definition of the configuration available for a mail action
    """

    model = Choice(
        title=_(u"Mail model"),
        required=True,
        vocabulary="collective.contentrules.mail.vocabulary.model", )

    mimetype = Choice(
        title=_(u"Mail mimetype"),
        required=True,
        vocabulary="collective.contentrules.mail.vocabulary.mimetype", )

    subject = TextLine(
        title=_(u"Subject"),
        description=_(u"Subject of the message"),
        required=True)

    source = TextLine(
        title=_(u"Email source"),
        description=_("The email address that sends the email. If no email is" \
                      " provided here, it will use the portal from address."),
        required=False)

    recipients = TextLine(
        title=_(u"Email recipients"),
        description=_("The email where you want to send this message. To send" \
            " it to different email addresses, just separate them with commas."),
        required=True)

    cc = TextLine(
        title=_(u"CC recipients"),
        description=_("The email to receive a copy of this message. To send" \
            " it to different email addresses, just separate them with commas."),
        required=False)

    bcc = TextLine(
        title=_(u"BCC recipients"),
        description=_("The email to receive a blind copy of this message. To" \
     " send it to different email addresses, just separate them with commas."),
        required=False)

    message = Text(
        title=_(u"Message"),
        description=_(u"Type in here the message that you want to mail."),
        required=True)


class MailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IMailAction, IRuleElementData)

    model = ''
    mimetype = ''
    subject = ''
    source = ''
    recipients = ''
    cc = ''
    bcc = ''
    message = ''

    element = 'collective.contentrules.mail.actions.Mail'

    @property
    def summary(self):
        return _(u"Email report to ${recipients}",
                 mapping=dict(recipients=self.recipients))


class MailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        # Get event objet
        obj = self.event.object

        utool = getToolByName(aq_inner(self.context), "portal_url")
        portal = utool.getPortalObject()

        site_charset = 'utf-8'
        email_charset = portal.getProperty('email_charset')

        # Get replacer interface from model
        model = getUtility(IMailModel, self.element.model)
        replacer_interface = model.replacer_interface

        # Extract all variables from this replacer
        replacer = replacer_interface(obj, None)
        if replacer is None:
            LOG.debug(u"Could not send email. The replacer is not applicable for this type of object.")
            return False

        words = {}
        for word_id in getFieldNamesInOrder(replacer_interface):
            replacement_value = getattr(replacer, word_id)
            if isinstance(replacement_value, str):
                replacement_value = replacement_value.decode(site_charset)
            words[word_id] = replacement_value

        # Apply word substitution on every mail fields
        def substitute(text):
            if not text:
                return ""

            for word_id, replacement_value in words.items():
                text = text.replace(u"${%s}" % word_id, replacement_value)

            return text.encode(site_charset)

        source = self.element.source
        if source:
            source = substitute(self.element.source)
        recipients = substitute(self.element.recipients)
        cc = substitute(self.element.cc)
        bcc = substitute(self.element.bcc)
        subject = substitute(self.element.subject)
        message = substitute(self.element.message)

        def processRecipients(recipients=''):
            address_list = []
            for email in recipients.split(','):
                email = email.strip()
                if not email:
                    # Remove empty address
                    continue
                address_list.append(email)
            return address_list

        # Process recipients
        recipient_list = processRecipients(recipients)
        cc_list = [e for e in processRecipients(cc) if e not in recipients]
        bcc_list = [e for e in processRecipients(bcc) if e not in recipients]

        if not recipient_list:
            # Because there are no recipients, do not send email
            LOG.info(u"""Do not send email "%s": no recipients defined.""" %
                     model.title)
            return False

        recipients = ",".join(recipient_list)
        cc = ",".join(cc_list)
        bcc = ",".join(bcc_list)

        # Process source

        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')

            if not from_address:
                raise ValueError, "You must provide a source address for this\
action or enter an email in the portal properties"

            from_name = portal.getProperty('email_from_name')
            source = "%s <%s>" % (from_name, from_address)

        # Encode text using mail charset

        if email_charset != site_charset:
            source = source.decode(site_charset).encode(email_charset)
            recipients = recipients.decode(site_charset).encode(email_charset)
            cc = cc.decode(site_charset).encode(email_charset)
            bcc = bcc.decode(site_charset).encode(email_charset)
            subject = subject.decode(site_charset).encode(email_charset)
            message = message.decode(site_charset).encode(email_charset)

        # Send email
        mailhost = getToolByName(aq_inner(self.context), "MailHost")

        if not mailhost:
            raise ComponentLookupError, \
                "You must have a Mailhost utility to execute this action"

        mimetype = self.element.mimetype

        try:
            mailhost.secureSend(message, recipients, source,
                                subject=subject, subtype=mimetype,
                                mcc=cc, mbcc=bcc,
                                charset=email_charset, debug=False)
        except (MailHostError, SMTPException, ), e:
            LOG.exception(u"Failed to send mail")
            return False

        return True


class MailAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    form_fields['model'].custom_widget = ModelWidget
    label = _(u"Add Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = MailAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class MailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    form_fields['model'].custom_widget = ModelWidget
    label = _(u"Edit Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")
