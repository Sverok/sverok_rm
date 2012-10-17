import sys

import transaction
from voteit.core.scripts.worker import ScriptWorker
from voteit.core.security import ROLE_PROPOSE
from voteit.core.security import ROLE_OWNER
from voteit.core.security import ROLE_ADMIN
from voteit.core.security import ROLE_MODERATOR
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal


def proposal_stop(*args):
    meetingname = sys.argv[1]
    
    worker = ScriptWorker('proposal_stop')
    
    print "Disabling proposals in meeting '%s'" % meetingname
    users = worker.root.users
    meeting = worker.root[meetingname]

    try:
        for userid in users.keys():
            meeting.del_groups(userid, [ROLE_PROPOSE], event = True)

        for ai in meeting.get_content(iface = IAgendaItem):
            for prop in ai.get_content(iface = IProposal):
                userids_and_groups = prop.get_security()
                for userid_group in userids_and_groups:
                    groups = userid_group['groups']
                    userid = userid_group['userid']

                    if ROLE_OWNER in groups and not (ROLE_ADMIN in groups or ROLE_MODERATOR in groups):
                        prop.del_groups(userid, [ROLE_OWNER], event = True)

        print "Committing changes"
        transaction.commit()
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
    
    worker.shutdown()