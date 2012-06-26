from plone.app.registry.browser import controlpanel

from collective.cookiecuttr.interfaces import ICookieCuttrSettings, _


class CookieCuttrSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ICookieCuttrSettings
    label = _(u"CookieCuttr settings")
    description = _(u"""""")

    def updateFields(self):
        super(CookieCuttrSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(CookieCuttrSettingsEditForm, self).updateWidgets()


class CookieCuttrSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CookieCuttrSettingsEditForm
