import colander
from deform import Form
from deform.exception import ValidationFailure
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from betahaus.viewcomponent import view_action
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_request
from voteit.core.models.schemas import button_cancel
from voteit.core import security
from voteit.core.models.interfaces import IMeeting

from sverok_rm import SverokMF as _

#XXX: Note that access system is up for refactoring.


PRE_ACCESS_TITLE = _(u"pre_access_request_label",
                     default = u"Special access permission for Sverok. All users will be given view, discussion and propose permissions INSTANTLY if they request it.")
@view_action('request_meeting_access', 'sverok_pre_rm_access', title = PRE_ACCESS_TITLE, interface = IMeeting)
def pre_meeting_access(context, request, va, **kw):
    if context.get_field_value('access_policy') != 'sverok_pre_rm_access':
        raise Exception("ViewAction for request meeting access public was called, but that access policy wasn't set for this meeting.")
    api = kw['api']
    if not api.userid:
        raise  Exception("Can't find userid")
    schema = colander.Schema()
    add_csrf_token(context, request, schema)
    form = Form(schema, buttons=(button_request, button_cancel,))
    response = {'api': api}
    post = request.POST
    if 'request' in post:
        controls = post.items()
        try:
            #For csrf, and possibly captcha later
            form.validate(controls)
        except ValidationFailure, e:
            response['form'] = e.render()
            return response
        context.add_groups(api.userid, [security.ROLE_VIEWER, security.ROLE_PROPOSE, security.ROLE_DISCUSS], event = True)
        api.flash_messages.add(_(u"You've been granted access. Welcome!"))
        url = resource_url(context, request)
        return HTTPFound(location=url)

    msg = _(u"pre_access_request_description",
            default = u"This meeting allows anyone to request access to it. You only need to click below to be allowed to view, discuss and add proposals in the meeting.")
    api.flash_messages.add(msg)
    #No action - Render form
    return form.render()


CLOSED_ACCESS_TITLE = _(u"closed_access_request_label",
                     default = u"Special access permission for Sverok. All users will be given view and discussion permissions INSTANTLY if they request it.")
@view_action('request_meeting_access', 'closed_rm_access', title = CLOSED_ACCESS_TITLE, interface = IMeeting)
def closed_prop_meeting_access(context, request, va, **kw):
    if context.get_field_value('access_policy') != 'closed_rm_access':
        raise Exception("ViewAction for request meeting access public was called, but that access policy wasn't set for this meeting.")
    api = kw['api']
    if not api.userid:
        raise  Exception("Can't find userid")
    schema = colander.Schema()
    add_csrf_token(context, request, schema)
    form = Form(schema, buttons=(button_request, button_cancel,))
    response = {'api': api}
    post = request.POST
    if 'request' in post:
        controls = post.items()
        try:
            #For csrf, and possibly captcha later
            form.validate(controls)
        except ValidationFailure, e:
            response['form'] = e.render()
            return response
        context.add_groups(api.userid, [security.ROLE_VIEWER, security.ROLE_DISCUSS], event = True)
        api.flash_messages.add(_(u"You've been granted access. Welcome!"))
        url = resource_url(context, request)
        return HTTPFound(location=url)

    msg = _(u"closed_prop_access_request_description",
            default = u"This meeting allows anyone to request access to it. You only need to click below to be allowed to view and discuss in the meeting.")
    api.flash_messages.add(msg)
    #No action - Render form
    return form.render()
