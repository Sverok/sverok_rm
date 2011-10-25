from pyramid.config import Configurator
from sverok_rm.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('sverok_rm.views.my_view',
                    context='sverok_rm:resources.Root',
                    renderer='sverok_rm:templates/mytemplate.pt')
    config.add_static_view('static', 'sverok_rm:static', cache_max_age=3600)
    return config.make_wsgi_app()
