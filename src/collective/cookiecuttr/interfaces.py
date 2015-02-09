# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform.directives import widget
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('collective.cookiecuttr')


class ICookieCuttr(Interface):
    """This interface is registered in profiles/default/browserlayer.xml,
    and is referenced in the 'layer' option of various browser resources.
    When the product is installed, this marker interface will be applied
    to every request, allowing layer-specific customisation.
    """


class ITextRowSchema(Interface):

    language = schema.TextLine(
        title=_(u"Language"),
        description=_(u'Enter the language code. Ex.: en'),
    )

    text = schema.Text(
        title=_(u"Text"),
    )


class ITextLinkSchema(Interface):

    language = schema.TextLine(
        title=_(u"Language"),
        description=_(u'Enter the language code. Ex.: en'),
    )

    text = schema.Text(
        title=_(u"Link to page"),
    )


class ITextAcceptSchema(Interface):

    language = schema.TextLine(
        title=_(u"Language"),
        description=_(u'Enter the language code. Ex.: en'),
    )

    text = schema.Text(
        title=_(u"Text to show in the Accept button"),
    )


class ICookieCuttrSettings(Interface):
    """Global CookieCuttr settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cookiecuttr_enabled = schema.Bool(
        title=_(u"Enable CookieCuttr"),
        description=_(
            u"help_cookiecuttr_enable",
            default=u"Toggle this to enable loading of the CookieCuttr plugin."
        ),
        required=False,
        default=False,
    )

    implied_consent = schema.Bool(
        title=_(u"Implied consent"),
        description=_(
            u"help_cookiecuttr_inplied",
            default=u"If enabled, the analytics viewlet will be rendered even "
                     "when the message is not accepted"
        ),
        required=False,
        default=False,
    )

    location_bottom = schema.Bool(
        title=_(u"Show cookiecuttr at the bottom"),
        description=_(
            u"help_cookiecuttr_location_bottom",
            default=u"If checked, the cookie message will be rendered at the "
                     "bottom"
            ),
        required=False,
        default=False,
    )

    text = schema.List(
        title=_(u"Text to show your visitor"),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextRowSchema
        ),
        default=[dict(
            language=u'en',
            text=u"We use cookies. <a href='{{cookiePolicyLink}}' "
                 "title='read about our cookies'>Read everything</a>"
         )],
    )
    widget(text=DataGridFieldFactory)

    link = schema.List(
        title=_(u"Link to page"),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextLinkSchema
        ),
        default=[dict(language=u"en", text=u" ")],
    )
    widget(link=DataGridFieldFactory)

    accept_button = schema.List(
        title=_(u"Text to show in the Accept button"),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextAcceptSchema
        ),
        default=[dict(language=u"en", text=u"Accept cookies")],
    )
    widget(accept_button=DataGridFieldFactory)
