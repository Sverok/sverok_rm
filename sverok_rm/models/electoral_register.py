import re

from BTrees.OOBTree import OOSet
from zope.interface import implements

from sverok_rm.models.interfaces import IElectoralRegister
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import ROLE_VOTER


class ElectoralRegister(object):
    __doc__ = IElectoralRegister.__doc__
    implements(IElectoralRegister)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context
        if not hasattr(self.context, '__register__'):
            self.context.__register__ = OOSet()
    
    @property
    def register(self):
        """ Acts as a storage.
        """
        return self.context.__register__
    
    def add(self, userid):
        if userid not in self.register:
            self.register.add(userid)

    def clear(self):
        self.closed = False
        self.context.__register__ = OOSet()
        
        userids_and_groups = []
        for permissions in self.context.get_security():
            groups = list(permissions['groups'])
            groups.remove(ROLE_VOTER)
            userids_and_groups.append({'userid':permissions['userid'], 'groups':groups})
        
        self.context.set_security(userids_and_groups)

    def close(self):
        self.closed = True
        
        #FIXME: set vote permissions the Sverok way
        for userid in self.register:
            self.context.add_groups(userid, (ROLE_VOTER, ))

def includeme(config):
    """ Include ElectoralRegister adapter in registry.
        Call this by running config.include('sverok_rm.models.electoral_register')
    """
    config.registry.registerAdapter(ElectoralRegister, (IMeeting,), IElectoralRegister)
