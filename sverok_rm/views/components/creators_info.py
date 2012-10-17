from betahaus.viewcomponent import view_action

from sverok_rm import SverokMF as _


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
            delegate_number = user.get_field_value('delegate_number', '')
            if delegate_number:
                delegate_number = " (%s)" % delegate_number
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
