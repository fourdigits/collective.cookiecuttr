# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.cookiecuttr.testing import\
    COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING
import unittest2 as unittest


class TestInstall(unittest.TestCase):

    layer = COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """Validate that our products GS profile has been run and the product
           installed
        """
        pid = 'collective.cookiecuttr'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')
