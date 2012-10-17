from copy import deepcopy

from pyramid.traversal import find_interface
from zope.interface import implements

from voteit.core.security import ROLE_VOTER
from voteit.core.models.interfaces import IMeeting
from voteit.irl.models.interfaces import IElectoralRegisterMethod

from sverok_rm import SverokMF as _
from sverok_rm.models.delegate_numbers import DelegateNumberStorage


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
        
        # get delegate number for all users 
        meeting = find_interface(self.context, IMeeting)
        delegate_numbers = DelegateNumberStorage(meeting)
        delegates = {}
        for userid in userids:
            delegate_number = delegate_numbers.get(userid) 
            if delegate_number:
                # remove non numerical delegate numbers
                try:
                    delegate_number = int(delegate_number)
                    delegates[delegate_number] = userid
                except ValueError:
                    pass
        
        # loop through delegates starting from 101 and give the first 101 the voter role
        loops = 1
        for delegate_number in sorted(delegates.iterkeys()):
            if int(delegate_number) >= 101:
                userid = delegates[delegate_number]
                self.context.add_groups(userid, (ROLE_VOTER, ), event=False)
                loops += 1
            if loops > 101:
                break;
            
            
def includeme(config):
    """ Include ElectoralRegisterMethod adapter in registry.
        Call this by running config.include('sverok_rm.models.electoral_register_method')
    """
    config.registry.registerAdapter(ElectoralRegisterMethod, (IMeeting,), IElectoralRegisterMethod, name=ElectoralRegisterMethod.name)
