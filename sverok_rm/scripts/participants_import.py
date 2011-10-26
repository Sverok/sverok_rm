import csv
import transaction

from voteit.core.scripts.worker import ScriptWorker
from voteit.core.models.user import User
from voteit.core import security


def participants_import(*args):
    worker = ScriptWorker('participants_import')
    
    print "Importing participants"
    root = worker.root
    users = worker.root.users
    #FIXME: take meeting name from args
    meeting = worker.root['meetings']['meeting']

    #FIXME: take file name from args
    reader = csv.reader(open("import.csv", "rb"), delimiter=',', quotechar='"')
    
    try:
        for participant in reader:
            firstname = participant[0]
            lastname = participant[1]
            email = participant[2]
            userid = participant[3]
            reserve = participant[4]
            #FIXME: get password from file
            
            print "\timporting: %s" % userid

            user = User()
            user.set_field_value('first_name', firstname)
            user.set_field_value('last_name', lastname)
            user.set_field_value('email', email)
            #FIXME: get password from file
            user.set_password('dummy')
            
            users[userid] = user
            
            meeting.add_groups(userid, (security.ROLE_DISCUSS, security.ROLE_PROPOSE, ))
            
        transaction.commit()
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
    
    worker.shutdown()
