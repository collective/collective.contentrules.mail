from transaction import commit
import time

from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from plone.contentrules.engine.interfaces import IRuleStorage

from collective.contentrules.mail.tests.base import TestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.context import TarballExportContext

from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase

from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class TestGenericSetup(TestCase):

    def afterSetUp(self):
        self.storage = getUtility(IRuleStorage)

    def testRuleInstalled(self):
        self.failUnless('test1' in self.storage)

    def testRulesConfigured(self):
        rule1 = self.storage['test1']
        self.assertEquals("Test rule 1", rule1.title)
        self.assertEquals("A test rule", rule1.description)
        self.assertEquals(IObjectModifiedEvent, rule1.event)
        self.assertEquals(True, rule1.enabled)
        self.assertEquals(False, rule1.stop)

        self.assertEquals(2, len(rule1.conditions))
        self.assertEquals("plone.conditions.PortalType", rule1.conditions[0].element)
        self.assertEquals(["Document", "News Item"], list(rule1.conditions[0].check_types))
        self.assertEquals("plone.conditions.Role", rule1.conditions[1].element)
        self.assertEquals(["Manager"], list(rule1.conditions[1].role_names))

        self.assertEquals(1, len(rule1.actions))
        self.assertEquals("collective.contentrules.mail.actions.Mail", rule1.actions[0].element)
        self.assertEquals("collective.contentrules.mail.model.base", rule1.actions[0].model)
        self.assertEquals("html", rule1.actions[0].mimetype)
        self.assertEquals("${default_from_email}", rule1.actions[0].source)
        self.assertEquals("${owner_emails}", rule1.actions[0].recipients)
        self.assertEquals(u"Your content was modified", rule1.actions[0].subject)
        self.assertEquals(u"Your content ${title} was modified.", rule1.actions[0].message)

    def testRuleAssigned(self):
        assignable = IRuleAssignmentManager(self.portal.news)
        self.assertEquals(1, len(assignable))

        self.assertEquals(True, assignable['test1'].enabled)
        self.assertEquals(False, assignable['test1'].bubbles)

    def testAssignmentOrdering(self):
        assignable = IRuleAssignmentManager(self.portal.news)
        self.assertEquals([u'test1'], assignable.keys())

    def testImportTwice(self):
        portal_setup = self.portal.portal_setup
        time.sleep(1)  # avoid timestamp colission
        portal_setup.runAllImportStepsFromProfile('profile-collective.contentrules.mail:testing')

        # We should get the same results as before
        self.testRuleInstalled()
        self.testRulesConfigured()
        self.testRuleAssigned()

    def testExport(self):
        site = self.portal
        context = TarballExportContext(self.portal.portal_setup)
        exporter = getMultiAdapter((site, context), IBody, name=u'plone.contentrules')

        expected = """\
<?xml version="1.0"?>
<contentrules>
 <rule name="test1" title="Test rule 1" description="A test rule"
    enabled="True" event="zope.lifecycleevent.interfaces.IObjectModifiedEvent"
    stop-after="False">
  <conditions>
   <condition type="plone.conditions.PortalType">
    <property name="check_types">
     <element>Document</element>
     <element>News Item</element>
    </property>
   </condition>
   <condition type="plone.conditions.Role">
    <property name="role_names">
     <element>Manager</element>
    </property>
   </condition>
  </conditions>
  <actions>
   <action type="collective.contentrules.mail.actions.Mail">
    <property name="mimetype">html</property>
    <property name="recipients">${owner_emails}</property>
    <property name="cc"></property>
    <property name="bcc">${contributor_emails}</property>
    <property name="source">${default_from_email}</property>
    <property name="message">Your content ${title} was modified.</property>
    <property name="model">collective.contentrules.mail.model.base</property>
    <property name="subject">Your content was modified</property>
   </action>
  </actions>
 </rule>
 <assignment name="test1" bubbles="False" enabled="True" location="/news"/>
</contentrules>
"""

        body = exporter.body
        self.assertEquals(expected.strip(), body.strip(), body)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGenericSetup))
    return suite
