from betahaus.viewcomponent import view_action
from pyramid.traversal import find_interface

from voteit.core.models.interfaces import IMeeting

from sverok_rm import SverokMF as _
from sverok_rm.models.delegate_numbers import DelegateNumberStorage  


@view_action('main', 'creators_info')
def creators_info(context, request, va, **kw):
    """ Get discussions for a specific context """
    api = kw['api']
    creators = kw['creators']
    portrait = kw['portrait']
    if not creators:
        return ''
    output = '<span class="creators">'
    for userid in kw['creators']:
        user = api.get_user(userid)
        try:
            meeting = find_interface(api.context, IMeeting)
            delegate_numbers = DelegateNumberStorage(meeting)
            delegate_number = delegate_numbers.get(userid) 
            if delegate_number:
                delegate_number = " (%s)" % delegate_number
            else:
                delegate_number = ''
            output += """<a href="%(userinfo_url)s" class="inlineinfo">%(portrait_tag)s %(usertitle)s (%(userid)s)%(delegate_number)s</a>"""\
                % {'userinfo_url': api.get_userinfo_url(userid),
                   'portrait_tag': portrait and user.get_image_tag() or '',
                   'usertitle': user.title,
                   'userid':userid,
                   'delegate_number': delegate_number,}
        except AttributeError:
            #This is to avoid if-statements for things that will probably not happen.
            output += "(%s)" % userid
    output += '</span>'
    return output
