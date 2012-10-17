from pyramid.i18n import TranslationStringFactory


SverokMF = TranslationStringFactory('sverok_rm')


def includeme(config):
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('rm_static', 'voteit_rm:static', cache_max_age = cache_ttl_seconds)
    config.scan('sverok_rm')
    config.include('sverok_rm.models.electoral_register_method')
    config.include('sverok_rm.models.delegate_ticket')
    config.include('sverok_rm.models.delegate_numbers')
    config.add_translation_dirs('sverok_rm:locale/')
    
    #Remove like-action from voteit.core
    from betahaus.viewcomponent.interfaces import IViewGroup
    vg = config.registry.queryUtility(IViewGroup, name = 'user_tags')
    if vg and 'like' in vg:
        del vg['like']
