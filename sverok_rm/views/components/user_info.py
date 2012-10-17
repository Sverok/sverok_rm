from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from webhelpers.html.converters import nl2br

from voteit.core.models.interfaces import IUser


@view_action('user_info', 'basic_profile', interface = IUser)
def user_basic_profile(context, request, va, **kw):
    response = dict(
        about_me = nl2br(context.get_field_value('about_me')),
        api = kw['api'],
        context = context,
    )
    return render('../templates/snippets/user_basic_info.pt', response, request = request)