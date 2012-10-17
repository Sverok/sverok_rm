from BTrees.OOBTree import OOBTree
from zope.interface import implements

from voteit.core.models.interfaces import IMeeting

from sverok_rm import SverokMF as _ 
from sverok_rm.models.interfaces import IDelegateNumberStorage


class DelegateNumberStorage(object):
    implements(IDelegateNumberStorage)

    def __init__(self, meeting):
        self.context = meeting
        
    @property
    def delegate_numbers(self):
        try:
            return self.context.__delegate_numbers__
        except AttributeError:
            self.context.__delegate_numbers__ = OOBTree()
            return self.context.__delegate_numbers__
        
    def add(self, userid, delegate_number):
    	self.delegate_numbers[userid] = delegate_number

    def get(self, userid):
        if userid in self.delegate_numbers:
            return self.delegate_numbers[userid]
        return None
    
    
def includeme(config):
    """ Include DelegateNumberStorage adapter in registry.
        Call this by running config.include('sverok_rm.models.delegate_numbers')
    """
    config.registry.registerAdapter(DelegateNumberStorage, (IMeeting,), IDelegateNumberStorage)