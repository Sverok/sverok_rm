from copy import deepcopy

from zope.interface import implements

from voteit.core.security import ROLE_VOTER
from voteit.core.models.interfaces import IMeeting
from voteit.irl.models.interfaces import IElectoralRegisterMethod

from sverok_rm import SverokMF as _


class ElectoralRegisterMethod(object):
    name = 'sverok_electoral_register_method'
    title = _(u"sverok_electoral_register_method_title", default=u"Sverok method")
    description = _(u"standard_electoral_register_method_description",
                    default = u"")
    implements(IElectoralRegisterMethod)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    def apply(self, userids):        
        # removing ROLE_VOTER from all users
        userids_and_groups = []
        for permissions in self.context.get_security():
            groups = list(permissions['groups'])
            if ROLE_VOTER in groups:
                groups.remove(ROLE_VOTER)
            userids_and_groups.append({'userid':permissions['userid'], 'groups':groups})
        
        self.context.set_security(userids_and_groups, event=False)
        
        # set ROLE_VOTER on all users in userids
        register = []
        # remove non numeric userids
        for userid in userids:
            try:
                int(userid)
                register.append(userid)
            except ValueError:
                pass
        # sort register on userid
        register.sort(key=lambda x: int(x))
        # loop through register starting from 101 and give the first 101 the voter role
        loops = 1
        for userid in register:
            if int(userid) >= 101:
                self.context.add_groups(userid, (ROLE_VOTER, ), event=False)
                loops += 1
            if loops > 101:
                break;
            
            
def includeme(config):
    """ Include ElectoralRegisterMethod adapter in registry.
        Call this by running config.include('sverok_rm.models.electoral_register_method')
    """
    config.registry.registerAdapter(ElectoralRegisterMethod, (IMeeting,), IElectoralRegisterMethod, name=ElectoralRegisterMethod.name)
