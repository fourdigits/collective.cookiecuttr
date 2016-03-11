# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

import logging

PROFILE_ID = 'profile-collective.cookiecuttr:default'
UNINSTALL = 'profile-collective.cookiecuttr:uninstall'
DEPENDENCY = 'profile-collective.z3cform.datagridfield:default'


def upgrade_to_0002(context, logger=None):
    """ Install dependencies and modify saved information
    """

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.cookiecuttr')

    # Get the existing values
    registry = queryUtility(IRegistry)
    text = registry.get(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.text',
        u' '
    )
    link = registry.get(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.link',
        u' '
    )
    accept = registry.get(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.accept_button',
        u' '
    )

    if not text:
        text = u' '

    if not link:
        link = u' '

    if not accept:
        accept = u' '

    # re-import profile
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    # save preexisting data in a dict
    lt = getToolByName(context, 'portal_languages')
    lang = safe_unicode(lt.getDefaultLanguage())
    registry['collective.cookiecuttr.interfaces.ICookieCuttrSettings.text'] = [dict(language=lang, text=text)]
    registry['collective.cookiecuttr.interfaces.ICookieCuttrSettings.link'] = [dict(language=lang, text=link)]
    registry['collective.cookiecuttr.interfaces.ICookieCuttrSettings.accept_button'] = [dict(language=lang, text=accept)]

    # install datagridfield
    portal_setup.runAllImportStepsFromProfile(DEPENDENCY)

    logger.info('Done')


def upgrade_from_0002_to_0003(context, logger=None):
    """Add option to move cookie message to the bottom to the control panel."""

    if logger is None:
        logger = logging.getLogger('collective.cookiecuttr')

    # Re-import plone.app.registry
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    logger.info('Successfully upgraded from 0002 to 0003')
