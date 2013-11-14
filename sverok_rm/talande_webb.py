""" Bindings for talande webb. Include manually to enable. This should be removed after the meeting,
    since it isn't open software.
"""
from fanstatic import Resource


def activate_text_to_speech(context, request, va, **kw):
    return u"""<li><a href="javascript:toggleBar();">Talande Webb</a></li>"""


def includeme(config):
    from voteit.core.models.interfaces import IFanstaticResources
    from betahaus.viewcomponent.interfaces import IViewGroup
    from betahaus.viewcomponent.models import ViewAction
    from .fanstaticlib import sverok_lib

    #Add fanstatic resource
    sverok_textspeech = Resource(sverok_lib, 'ba.se.js')
    util = config.registry.getUtility(IFanstaticResources)
    util.add('sverok_textspeech', sverok_textspeech)

    #Add menu alternative
    va = ViewAction(activate_text_to_speech, 'talande_webb')
    vg = config.registry.getUtility(IViewGroup, name = 'help_action')
    vg.add(va)
