import csv
import transaction

from voteit.core.scripts.worker import ScriptWorker
from voteit.core.models.user import User
from voteit.core import security


def participants_import(*args):
    args = list(args)
    meetingname = args[0][0]
    filename = args[0][1]
    
    worker = ScriptWorker('participants_import')
    
    print "Importing participants"
    root = worker.root
    users = worker.root.users
    meeting = worker.root[meetingname]

    reader = csv.reader(open(filename, "rb"), delimiter=';', quotechar='"')
    
    try:
        # skip first line
        reader.next()
        for participant in reader:
            userid = participant[0]
            firstname = unicode(participant[2], 'utf-8')
            lastname = unicode(participant[3], 'utf-8')
            email = participant[4]
            password = unicode(participant[5], 'utf-8')
            
            print "\timporting: %s - %s %s" % (userid, firstname, lastname)
            
            user = User()
            user.set_field_value('first_name', firstname)
            user.set_field_value('last_name', lastname)
            user.set_field_value('email', email)
            user.set_password(password)
            
            users[userid] = user
            
            meeting.add_groups(userid, (security.ROLE_PROPOSE, ))
            
        transaction.commit()
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
    
    worker.shutdown()
