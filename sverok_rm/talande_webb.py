# -*- coding: utf-8 -*-
""" Bindings for talande webb / browse aloud. Include manually to enable. This should be removed after the meeting,
    since it isn't open software.
"""
from pyramid.httpexceptions import HTTPFound
from voteit.core.models.interfaces import IFlashMessages
from . import SverokMF as _


def menu_toggle_ba(context, request, va, **kw):
    if request.cookies.get('ba_enabled', False):
        msg = u"Stäng av talande webb"
    else:
        msg = u"Aktivera talande webb"
    url = request.resource_url(context, '_toggle_ba')
    return u"""<li><a href="%s">%s</a></li>""" % (url, msg)

def menu_show_ba(context, request, va, **kw):
    if not request.cookies.get('ba_enabled', False):
        return u""
    return u"""<li><a href="javascript:toggleBar();">Visa talande webb</a></li>"""

def toggle_ba(context, request):
    fm = request.registry.getAdapter(request, IFlashMessages)
    response = HTTPFound(location = request.resource_url(context))
    if request.cookies.get('ba_enabled', False):
        response.delete_cookie('ba_enabled')
        fm.add(u"Talande webb avstängt")
    else:
        response.set_cookie('ba_enabled', '1')
        fm.add(u"Talande webb påslaget")
    return response

def is_ba_enabled(context, request, view):
    return request.cookies.get('ba_enabled', False)


def includeme(config):
    from voteit.core.models.interfaces import IFanstaticResources
    from voteit.core.fanstaticlib import jquery_deform
    from betahaus.viewcomponent.interfaces import IViewGroup
    from betahaus.viewcomponent.models import ViewAction
    from fanstatic import Resource

    from .fanstaticlib import sverok_lib

    #Add fanstatic resource
    ba_main = Resource(sverok_lib, 'ba.se.js', dont_bundle = True, bottom = False)
    ba_integration = Resource(sverok_lib, 'ba_integration.js', depends = (ba_main, jquery_deform, ), dont_bundle = True, bottom = False)
    util = config.registry.getUtility(IFanstaticResources)
    util.add('ba_integration', ba_integration, is_ba_enabled)

    #Add menu alternative
    va1 = ViewAction(menu_toggle_ba, 'menu_toggle_ba')
    va2 = ViewAction(menu_show_ba, 'menu_show_ba')
    vg = config.registry.getUtility(IViewGroup, name = 'help_action')
    vg.add(va1)
    vg.add(va2)

    #Add toggle view
    config.add_view(toggle_ba, name = '_toggle_ba')
