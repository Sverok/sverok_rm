import transaction

from voteit.core.scripts.worker import ScriptWorker
from voteit.core.security import ROLE_OWNER


def post_import(*args):
    #FIXME: This script shouldn't exist - it's already fixed in participants_import
    worker = ScriptWorker('post_import')
    
    print "Adjusting ownership for imported users"
    users = worker.root.users
    
    try:
        for (userid, obj) in users.items():
            obj.add_groups(userid, [ROLE_OWNER], event = True)
        print "Committing change"
        transaction.commit()
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
    worker.shutdown()
