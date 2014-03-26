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
        default=u'',
    )

    text = schema.Text(
        title=_(u"Text"),
        default=u"We use cookies."
                 " <a href='{{cookiePolicyLink}}' "
                 "title='read about our cookies'>"
                 "Read everything</a>"

    )


class ITextLinkSchema(Interface):

    language = schema.TextLine(
        title=_(u"Language"),
        description=_(u'Enter the language code. Ex.: en'),
        default=u'',
    )

    text = schema.Text(
        title=_(u"Link to page"),
        default=u"",

    )


class ITextAcceptSchema(Interface):

    language = schema.TextLine(
        title=_(u"Language"),
        description=_(u'Enter the language code. Ex.: en'),
        default=u'',
    )

    text = schema.Text(
        title=_(u"Text to show in the Accept button"),
        default=u"Accept cookies"

    )


class ICookieCuttrSettings(Interface):
    """Global CookieCuttr settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cookiecuttr_enabled = schema.Bool(title=_(u"Enable CookieCuttr"),
                                  description=_(u"help_cookiecuttr_enable",
                                  default=u"Toggle this to enable"
                                                " loading of the CookieCuttr"
                                                " plugin."),
                                  required=False,
                                  default=False,)

    text = schema.List(
        title=_(u"Text to show your visitor"),
        description=_(u"", default=u""),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextRowSchema
        )
    )
    widget(text=DataGridFieldFactory)

    link = schema.List(
        title=_(u"Link to page"),
        description=_(u"", default=u""),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextLinkSchema
        )
    )
    widget(link=DataGridFieldFactory)

    accept_button = schema.List(
        title=_(u"Text to show in the Accept button"),
        description=_(u"", default=u""),
        required=False,
        value_type=DictRow(
            title=u"Value",
            schema=ITextAcceptSchema
        )
    )
    widget(accept_button=DataGridFieldFactory)
