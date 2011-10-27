import re

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
            self.context.__register__ = []
        if not hasattr(self.context, '__register_closed__'):
            self.context.__register_closed__ = True
    
    @property
    def closed(self):
        return self.context.__register_closed__
    
    @property
    def register(self):
        """ Acts as a storage.
        """
        return self.context.__register__
    
    def add(self, userid):
        if self.closed:
            #FIXME: translations
            raise Exception(u"Electoral register is closed")

        if userid not in self.register:
            self.register.append(userid)

    def clear(self):
        self.context.__register_closed__ = False
        self.context.__register__ = []
        
        userids_and_groups = []
        for permissions in self.context.get_security():
            groups = list(permissions['groups'])
            if ROLE_VOTER in groups:
                groups.remove(ROLE_VOTER)
            userids_and_groups.append({'userid':permissions['userid'], 'groups':groups})
        
        self.context.set_security(userids_and_groups)

    def close(self, sverok=True):
        self.context.__register_closed__ = True
        
        if sverok:
            register = []
            # remove non numeric userids
            for userid in self.register:
                try:
                    int(userid)
                    register.append(userid)
                except Exception:
                    pass
            # sort register on userid
            register.sort(key=lambda x: int(x))
            # loop through register starting from 101 and give the first 101 the voter role
            loops = 1
            for userid in register:
                if int(userid) >= 101:
                    self.context.add_groups(userid, (ROLE_VOTER, ))
                    loops += 1
                if loops > 101:
                    break;
        else:
            for userid in self.register:
                self.context.add_groups(userid, (ROLE_VOTER, ))

def includeme(config):
    """ Include ElectoralRegister adapter in registry.
        Call this by running config.include('sverok_rm.models.electoral_register')
    """
    config.registry.registerAdapter(ElectoralRegister, (IMeeting,), IElectoralRegister)
