.. contents::

Introduction
============
This is an integration package for the CookieCuttr javascript plugin <http://cookiecuttr.com/>


Installation
============
Add the package name ot the eggs part of your zope2 instance and rerun buildout, after a restart
you can install the package from the quickinstaller.

Setup
=====
Go to <http://yoursite/@@cookiecuttr-settings> to make some default settings, and turn on the package.

I use it to be able to decline cookies for Google Analytics; I do this by wrapping the
analytics code in <http://yoursite/@@site-controlpanel> in this javascript:

if (jQuery.cookie('cc_cookie_accept') == "cc_cookie_accept") {
    ...
    }



