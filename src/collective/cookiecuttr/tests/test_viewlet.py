import unittest2 as unittest

from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView as View

# this time, we need to add an interface to the request
from zope.interface import alsoProvides

# The browserlayer
from collective.cookiecuttr.interfaces import ICookieCuttr
from collective.cookiecuttr.testing import\
    COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING


class CookieCuttrViewletTestCase(unittest.TestCase):
    """ test demonstrates that zcml registration variables worked properly
    """
    layer = COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.webstats_js = "analytics test"
        pprops = getToolByName(self.portal, 'portal_properties')
        pprops.site_properties.webstats_js = self.webstats_js

    def test_viewlet_is_not_installed(self):
        """ looking up and updating the manager should not list our viewlet
            when our browserlayer is not applied, eq. when our product is not
            installed.
        """
        request = self.app.REQUEST
        context = self.portal

        view = View(context, request)

        manager_name = 'plone.htmlhead'
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        manager.update()

        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 0)

        # The analytics viewlet should be there and show its normal contents.
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.assertEqual(analytics, self.webstats_js)

    def get_analytics_viewlet_contents(self, context, request, view):
        # Get the contents of the analytics viewlet or return a string
        # explaining what went wrong..
        manager_name = 'plone.portalfooter'
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)
        if manager is None:
            return 'No viewlet manager %s found.' % manager_name
        manager.update()
        analytics_viewlet = [v for v in manager.viewlets
                             if v.__name__ == 'plone.analytics']
        if len(analytics_viewlet) != 1:
            return 'Not 1 but %d analytics viewlets found.' % len(
                analytics_viewlet)
        return analytics_viewlet[0].render()

    def test_viewlet_is_present(self):
        """ looking up and updating the manager should list our viewlet
        """
        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal

        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)

        # The analytics viewlet should be there and show its normal contents.
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.assertEqual(analytics, self.webstats_js)

    def test_viewlet_cookiecuttr_disabled(self):
        """ looking up and updating the manager should list our viewlet

        But when disabled it should be empty.
        """
        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal
        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)
        self.failUnlessEqual(my_viewlet[0].render(), '')

        # The analytics viewlet should be there and show its normal contents.
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.assertEqual(analytics, self.webstats_js)

    def test_viewlet_cookiecuttr_enabled(self):
        """ looking up and updating the manager should list our viewlet

        It is enabled so it should be filled.
        """
        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal
        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)

        my_viewlet[0].settings.cookiecuttr_enabled = True

        self.failUnlessEqual(my_viewlet[0].render(), u'\n<script type="text/javascript">\n\n    (function($) {\n        $(document).ready(function () {\n            if($.cookieCuttr) {\n                $.cookieCuttr({cookieAnalytics: false,\n                               cookiePolicyLink: " ",\n                               cookieMessage: "We use cookies. <a href=\'{{cookiePolicyLink}}\' title=\'read about our cookies\'>Read everything</a>",\n                               cookieAcceptButtonText: "Accept cookies",\n                               cookieNotificationLocationBottom: false\n                               });\n                }\n        })\n    })(jQuery);\n</script>\n\n')

        # The analytics viewlet should be there and show nothing.
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.assertEqual(analytics, '')

    def test_viewlet_analytics(self):
        """ looking up and updating the manager should list our viewlet
        """
        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal
        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)

        my_viewlet[0].settings.cookiecuttr_enabled = True
        self.failUnlessEqual(my_viewlet[0].render(), u'\n<script type="text/javascript">\n\n    (function($) {\n        $(document).ready(function () {\n            if($.cookieCuttr) {\n                $.cookieCuttr({cookieAnalytics: false,\n                               cookiePolicyLink: " ",\n                               cookieMessage: "We use cookies. <a href=\'{{cookiePolicyLink}}\' title=\'read about our cookies\'>Read everything</a>",\n                               cookieAcceptButtonText: "Accept cookies",\n                               cookieNotificationLocationBottom: false\n                               });\n                }\n        })\n    })(jQuery);\n</script>\n\n')

        # The analytics viewlet should be there and be empty.
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.assertEqual(analytics, '')

        # CookieCuttr disabled, user hasn't set cookie
        my_viewlet[0].settings.cookiecuttr_enabled = False
        request.cookies['cc_cookie_accept'] = False
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.failUnlessEqual(analytics, self.webstats_js)

        # CookieCuttr enabled, user hasn't set cookie
        my_viewlet[0].settings.cookiecuttr_enabled = True
        request.cookies['cc_cookie_accept'] = False
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.failUnlessEqual(analytics, '')

        # CookieCuttr disabled, user has set cookie
        my_viewlet[0].settings.cookiecuttr_enabled = False
        request.cookies['cc_cookie_accept'] = True
        analytics = self.get_analytics_viewlet_contents(context, request, view)
        self.failUnlessEqual(analytics, self.webstats_js)

        # CookieCuttr enabled, user has set cookie
        my_viewlet[0].settings.cookiecuttr_enabled = True
        request.cookies['cc_cookie_accept'] = 'cc_cookie_accept'
        self.failUnlessEqual(analytics, self.webstats_js)

    def test_viewlet_implied_consent(self):
        """ check the implied consent setting
        """
        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal
        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)

        my_viewlet[0].settings.cookiecuttr_enabled = True
        self.failUnlessEqual(my_viewlet[0].render(), u'\n<script type="text/javascript">\n\n    (function($) {\n        $(document).ready(function () {\n            if($.cookieCuttr) {\n                $.cookieCuttr({cookieAnalytics: false,\n                               cookiePolicyLink: " ",\n                               cookieMessage: "We use cookies. <a href=\'{{cookiePolicyLink}}\' title=\'read about our cookies\'>Read everything</a>",\n                               cookieAcceptButtonText: "Accept cookies",\n                               cookieNotificationLocationBottom: false\n                               });\n                }\n        })\n    })(jQuery);\n</script>\n\n')

        footer_manager = queryMultiAdapter((context, request, view),
                                           IViewletManager,
                                           'plone.portalfooter',
                                           default=None)

        footer_manager.update()

        analytics_viewlet = [v for v in footer_manager.viewlets if v.__name__ == 'plone.analytics'][0]

        # Set something for the analytics viewlet
        self.portal.portal_properties.site_properties.webstats_js = "analytics test"

        # CookieCuttr enabled, implied_consent enabled, user has no cookie,
        # analytics viewlet is rendered
        my_viewlet[0].settings.cookiecuttr_enabled = True
        my_viewlet[0].settings.implied_consent = True
        request.cookies['cc_cookie_accept'] = False
        self.failUnlessEqual(analytics_viewlet.render(), "analytics test")
        analytics = self.get_analytics_viewlet_contents(context, request, view)

    def test_viewlet_location_bottom(self):
        """Check the location_bottom setting."""

        # our viewlet is registered for a browser layer.  Browser layers
        # are applied to the request during traversal in the publisher.  We
        # need to do the same thing manually here
        request = self.app.REQUEST
        context = self.portal
        alsoProvides(request, ICookieCuttr)

        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.htmlhead'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter(
            (context, request, view),
            IViewletManager,
            manager_name,
            default=None,
        )

        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets
                      if v.__name__ == 'collective.cookiecuttr']

        self.failUnlessEqual(len(my_viewlet), 1)

        my_viewlet[0].settings.cookiecuttr_enabled = True
        expected = u"""
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            if($.cookieCuttr) {
                $.cookieCuttr({cookieAnalytics: false,
                               cookiePolicyLink: " ",
                               cookieMessage: "We use cookies. <a href=\'{{cookiePolicyLink}}\' title=\'read about our cookies\'>Read everything</a>",
                               cookieAcceptButtonText: "Accept cookies",
                               cookieNotificationLocationBottom: false
                               });
                }
        })
    })(jQuery);
</script>

"""
        self.failUnlessEqual(my_viewlet[0].render(), expected)
        my_viewlet[0].settings.location_bottom = True

        expected = u"""
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            if($.cookieCuttr) {
                $.cookieCuttr({cookieAnalytics: false,
                               cookiePolicyLink: " ",
                               cookieMessage: "We use cookies. <a href=\'{{cookiePolicyLink}}\' title=\'read about our cookies\'>Read everything</a>",
                               cookieAcceptButtonText: "Accept cookies",
                               cookieNotificationLocationBottom: true
                               });
                }
        })
    })(jQuery);
</script>

"""
        self.failUnlessEqual(my_viewlet[0].render(), expected)
