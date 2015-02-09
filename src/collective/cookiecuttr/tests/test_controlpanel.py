# -*- coding: utf-8 -*-

from collective.cookiecuttr.interfaces import ICookieCuttrSettings
from collective.cookiecuttr.testing import \
    COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest

PROJECTNAME = 'collective.cookiecuttr'


class ControlPanelTestCase(unittest.TestCase):

    layer = COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    # def test_controlpanel_has_view(self):
    #     view = getMultiAdapter((self.portal, self.portal.REQUEST),
    #                            name='cookiecuttr-settings')
    #     view = view.__of__(self.portal)
    #     self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@cookiecuttr-settings',
        )

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('cookiecuttr' in actions,
                        'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('cookiecuttr' not in actions,
                        'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ICookieCuttrSettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_records_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'cookiecuttr_enabled'))
        self.assertTrue(hasattr(self.settings, 'implied_consent'))
        self.assertTrue(hasattr(self.settings, 'text'))
        self.assertTrue(hasattr(self.settings, 'link'))
        self.assertTrue(hasattr(self.settings, 'accept_button'))
        self.assertTrue(hasattr(self.settings, 'location_bottom'))
        # check default
        self.assertNotEqual(self.settings.accept_button, None)

    def test_records_value_types(self):
        text = getattr(self.settings, 'text')
        link = getattr(self.settings, 'link')
        accept_button = getattr(self.settings, 'accept_button')
        self.assertTrue(type(text), type([]))
        self.assertTrue(type(link), type([]))
        self.assertTrue(type(accept_button), type([]))

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.cover.controlpanel.ICookieCuttrSettings.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'cookiecuttr_enabled')
