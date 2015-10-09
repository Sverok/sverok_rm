# -*- coding: utf-8 -*-
from pyramid.i18n import TranslationStringFactory


SverokMF = TranslationStringFactory('sverok_rm')


def includeme(config):
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('rm_static', 'voteit_rm:static', cache_max_age = cache_ttl_seconds)
    config.scan('sverok_rm')
    config.include('sverok_rm.models.elegible_voters_method')
    config.add_translation_dirs('sverok_rm:locale/')
    #config.include(patch_localisation)

def patch_localisation(config):
    from betahaus.pyracont.interfaces import ISchemaFactory
    to_patch = ('AddUserSchema', 'RegisterUserSchema', 'EditUserSchema')
    for name in to_patch:
        factory = config.registry.getUtility(ISchemaFactory, name = name)
        cls = factory._callable
        node = getattr(cls, 'last_name')
        node.description = u"Här kan du också lägga till ditt pronomen (hon/han/hen) om du vill."
        node = getattr(cls, 'about_me', None)
        if node:
            node.description = """Här kan du fylla i mer information om dig som kan vara intressant för andra att veta.
                Det kan vara vilken förening du tillhör, vilket pronomen du föredrar (han/hon/hen)
                eller om du har någon särskild hjärtefråga i Sverok.
                Vänligen notera att det du skriver här blir synligt för alla användare som
                är deltagare i samma möte som du."""
