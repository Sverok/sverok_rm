from betahaus.viewcomponent import view_action
from pyramid.traversal import find_resource
from voteit.core.security import VIEW

from sverok_rm import SverokMF as _


@view_action('meta_data_listing', 'proposal_number', permission=VIEW)
def meta_proposal_number(context, request, va, **kw):
    api = kw['api']
    brain = kw['brain']
    
    if not brain['content_type'] == 'Proposal':
        return ''
    
    obj = find_resource(api.root, brain['path'])
    proposal_number = obj.get_field_value('proposal_number')
    
    if not proposal_number:
        return ''

    return '<strong>%s</strong>' % proposal_number
