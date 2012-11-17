import transaction
import sys

from voteit.core.scripts.worker import ScriptWorker

from sverok_rm.models.delegate_ticket import DelegateTicketStorage
from sverok_rm.models.delegate_ticket import DelegateTicket


def delegate_numbers(*args):
    meetingname = sys.argv[2]
    worker = ScriptWorker('delegate_numbers')
    print "Delegate numbers"
    meeting = worker.root[meetingname]
    tickets = DelegateTicketStorage(meeting)
    
    try:
        for number in range(1, 300):
            ticket = DelegateTicket(number)
            tickets.add(ticket)
            print "%s;%s" % (number, ticket.token) 
        transaction.commit()
        print "Committed changes"
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
        print "There were errors, db commit was aborted. See log for details."
    
    worker.shutdown()
