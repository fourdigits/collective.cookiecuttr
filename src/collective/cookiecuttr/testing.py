# -*- coding: utf-8 -*-

from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig


class CollectiveCookiecuttr(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.cookiecuttr
        xmlconfig.file('configure.zcml',
                       collective.cookiecuttr,
                       context=configurationContext)
        xmlconfig.file('overrides.zcml',
                       collective.cookiecuttr,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.cookiecuttr:default')


COLLECTIVE_COOKIECUTTR_FIXTURE = CollectiveCookiecuttr()
COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_COOKIECUTTR_FIXTURE, ),
                       name="CollectiveCookiecuttr:Integration")
