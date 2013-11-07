""" Fanstatic lib"""
from fanstatic import Library
from fanstatic import Resource


sverok_lib = Library('sverok_lib', 'static')
sverok_textspeech = Resource(sverok_lib, 'ba.se.js')


def includeme(config):
    from voteit.core.models.interfaces import IFanstaticResources
    util = config.registry.getUtility(IFanstaticResources)
    util.add('sverok_textspeech', sverok_textspeech)
