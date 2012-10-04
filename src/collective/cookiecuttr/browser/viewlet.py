from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.cookiecuttr.interfaces import ICookieCuttrSettings
from plone.app.layout.analytics.view import AnalyticsViewlet


class CookieCuttrViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(CookieCuttrViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        registry = getUtility(IRegistry)
        try:
            self.settings = registry.forInterface(ICookieCuttrSettings)
        except KeyError:
            self.settings = None

    def update(self):
        pass

    def available(self):
        return self.settings and self.settings.cookiecuttr_enabled

    def render(self):
        if self.available():
            snippet = safe_unicode(js_template % (self.settings.link,
                                                  self.settings.text,
                                                  self.settings.accept_button))
            return snippet
        return ""


class CookieCuttrAwareAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        if self.request.cookies.get('cc_cookie_accept', None):
            return super(CookieCuttrAwareAnalyticsViewlet, self).render()
        else:
            return ""


js_template = """
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            $.cookieCuttr({cookieAnalytics: false,
                           cookiePolicyLink: "%s",
                           cookieMessage: "%s",
                           cookieAcceptButtonText: "%s"
                           });
        })
    })(jQuery);
</script>

"""
