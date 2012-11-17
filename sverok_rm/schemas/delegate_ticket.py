import colander
from betahaus.pyracont.decorators import schema_factory
from pyramid.traversal import find_interface

from voteit.core.models.interfaces import IMeeting

from sverok_rm import SverokMF as _
from sverok_rm.models.delegate_ticket import DelegateTicketStorage


class TicketValidator(object):
    def __init__(self, context):
        assert IMeeting.providedBy(context)
        self.context = context

    def __call__(self, node, value):
        meeting = find_interface(self.context, IMeeting)
        tickets = DelegateTicketStorage(meeting)
        
        if value not in tickets.delegate_tickets:
            msg = _('no_ticket_with_that_token',
                    default=u"No ticket available with that number")
            raise colander.Invalid(node, msg)

@colander.deferred
def deferred_ticket_validator(node, kw):
    context = kw['context']
    return TicketValidator(context)

@schema_factory('ClaimDelegateTicketSchema')
class ClaimTicketSchema(colander.Schema):
    token = colander.SchemaNode(colander.String(),
                                title = _(u"claim_ticket_token_title",
                                          default = u"The ticket your received at the check-in."),
                                validator = deferred_ticket_validator,)
