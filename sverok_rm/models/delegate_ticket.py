import string

from BTrees.OOBTree import OOBTree
from betahaus.pyracont.decorators import content_factory
from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid
from pyramid.traversal import find_interface 
from random import choice
from repoze.folder import Folder
from uuid import uuid4
from zope.interface import implements

from voteit.core.models.date_time_util import utcnow
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.workflow_aware import WorkflowAware

from sverok_rm import SverokMF as _ 
from sverok_rm.models.interfaces import IDelegateTicketStorage
from sverok_rm.models.interfaces import IDelegateTicket
from sverok_rm.models.delegate_numbers import DelegateNumberStorage


class DelegateTicketStorage(object):
    implements(IDelegateTicketStorage)
    
    def __init__(self, meeting):
        self.context = meeting
    
    @property
    def delegate_tickets(self):
        try:
            return self.context.__delegate_tickets__
        except AttributeError:
            self.context.__delegate_tickets__ = OOBTree()
            return self.context.__delegate_tickets__
        
    def add(self, ticket):
        ticket.__parent__ = self.context
        self.delegate_tickets[ticket.token] = ticket


@content_factory('DelegateTicket', title=_(u"Delegate ticket"))
class DelegateTicket(Folder, WorkflowAware):
    """ Delegate ticket. Give the token to users to claim a 
        delegate number.
        See :mod:`sverok_rm.models.interfaces.IDelegateTicket`.
        All methods are documented in the interface of this class.
    """
    implements(IDelegateTicket)
    content_type = 'DelegateTicket'
    allowed_contexts = () #Not addable through regular forms
    #No schemas
    
    def __init__(self, delegate_number):
        self.delegate_number = "%s" % delegate_number
        self.created = utcnow()
        self.closed = None
        self.claimed_by = None
        self.token = ''.join([choice(string.letters + string.digits) for x in range(30)])
        self.uid = unicode(uuid4())
        super(DelegateTicket, self).__init__()

    def claim(self, request):
        #Is the ticket open?
        if self.get_workflow_state() != 'open':
            raise Forbidden("This ticket has already been claimed")
        #Find required resources and do some basic validation
        meeting = find_interface(self, IMeeting)
        assert meeting
        
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden("You can't claim a ticket unless you're authenticated.")
        
        # get delegate number adapter and add userid and delegaste number
        delegate_numbers = DelegateNumberStorage(meeting)
        delegate_numbers.add(userid, self.delegate_number)

        self.claimed_by = userid

        self.set_workflow_state(request, 'closed')
        
        self.closed = utcnow()


def includeme(config):
    """ Include DelegateTicketStorage adapter in registry.
        Call this by running config.include('sverok_rm.models.delegate_ticket')
    """
    config.registry.registerAdapter(DelegateTicketStorage, (IMeeting,), IDelegateTicketStorage)