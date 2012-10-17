from zope.interface import Attribute
from zope.interface import Interface

from betahaus.pyracont.interfaces import IBaseFolder


class IDelegateTicketStorage(Interface):
    """ Adapts meeting to add ability to store delegate tickets
    """
    delegate_tickets = Attribute("Storage for delegate tickets.")

    def __init__(meeting):
        """ meeting to adapt. """
        
    def add(ticket):
        """ add ticket to meeting """


class IDelegateTicket(Interface):
    """ Delegate ticket - these track delegates to meetings. """
    delegate_number = Attribute("Delegate number that the user who claimed it gets")
    created = Attribute("Creation date")
    closed = Attribute("Close date (When the ticket was used)")
    token = Attribute("Security token.")
    claimed_by = Attribute("The userid of the user who claimed (used) this ticket.")

    def claim(request):
        """ Handle claim of this ticket. Set delegate number on user and 
            set the ticket as closed.

            Called by ticket form - see:
            :func:`sverok_rm.views.delegate_ticket.DelegateTicketView.claim_ticket`
        """


class IDelegateNumberStorage(Interface):
    """ Adapts meeting to add ability to store delege numbers
    """
    
    delegate_numbers = Attribute("Storage for delegate numbers.")

    def __init__(meeting):
        """ meeting to adapt. """
        
    def add(userid, delegate_number):
        """ add delegate number to userid in meeting """
        
    def get(userid):
        """ get delegate number for userid in meeting """
        