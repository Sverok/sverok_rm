from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from pyramid.traversal import find_interface
from webhelpers.html.converters import nl2br

from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser

from sverok_rm.models.delegate_numbers import DelegateNumberStorage


@view_action('user_info', 'basic_profile', interface = IUser)
def user_basic_profile(context, request, va, **kw):
    api = kw['api']
    meeting = find_interface(api.context, IMeeting)
    if meeting:
        delegate_numbers = DelegateNumberStorage(meeting)
        delegate_number = delegate_numbers.get(context.__name__)
    else:
        delegate_number = None
                
    response = dict(
        about_me = nl2br(context.get_field_value('about_me')),
        api = api,
        context = context,
        delegate_number = delegate_number,
    )
    return render('../templates/snippets/user_basic_info.pt', response, request = request)