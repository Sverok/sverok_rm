# -*- coding: utf-8 -*-


def includeme(config):
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('rm_static', 'voteit_rm:static', cache_max_age = cache_ttl_seconds)
    # No longer used in Sverok
    # config.include('sverok_rm.models.elegible_voters_method')
