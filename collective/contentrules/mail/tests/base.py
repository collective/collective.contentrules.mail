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
"""" defines a test class and its Plone Site layer for plone tests
"""
from plone.app.testing.bbb import PloneTestCaseFixture, PloneTestCase
from plone.app import testing
from plone.app.testing import setRoles, TEST_USER_ID
from plone.testing import z2

# fake mailhost
from Products.MailHost import MailHost


class TestMailHost(MailHost.MailHost):

    def _send(self, mfrom, mto, messageText):
        """Fake sender"""
        print messageText


class CCMFixture(PloneTestCaseFixture):

    def setUpZope(self, app, configurationContext):
        super(PloneTestCaseFixture, self).setUpZope(app, configurationContext)
        import collective.contentrules.mail
        self.loadZCML(package=collective.contentrules.mail)
        z2.installProduct(app, 'collective.contentrules.mail')

    def setUpPloneSite(self, portal):
        super(PloneTestCaseFixture, self).setUpPloneSite(portal)

        # prepare structure
        if 'news' not in portal:
            setRoles(portal, TEST_USER_ID, ['Manager'])
            portal.invokeFactory('Folder', 'news', title='News Folder')
            setRoles(portal, TEST_USER_ID, ['Member'])

        # install product
        testing.applyProfile(portal, 'collective.contentrules.mail:default')

        # install testing profile
        from Products.GenericSetup import EXTENSION, profile_registry
        profile_registry.registerProfile('testing',
            "collective.contentrules.mail testing",
            'Used for testing only',
            'profiles/testing',
            'collective.contentrules.mail',
            EXTENSION)
        testing.applyProfile(portal, 'collective.contentrules.mail:testing')
        # patch mail host
        #portal._old = MailHost.MailHost
        #MailHost.MailHost = TestMailHost

        portal.manage_changeProperties(email_from_name='Site Administrator')

    def tearDownZope(self, app):
        super(PloneTestCaseFixture, self).tearDownZope(app)
        z2.uninstallProduct(app, 'collective.contentrules.mail')

PTC_FIXTURE = CCMFixture()
PTC_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(PTC_FIXTURE, ), name='PloneTestCase:Functional')


class TestCase(PloneTestCase):
    """ Base class used for test cases """

    layer = PTC_FUNCTIONAL_TESTING
