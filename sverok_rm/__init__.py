

def includeme(config):
    #FIXME: Do things with voteit :)
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('rm_static', 'voteit_rm:static', cache_max_age = cache_ttl_seconds)
    config.scan(__name__)
    config.include('sverok_rm.models.electoral_register')
