import unittest

from pyramid import testing
from zope.interface.verify import verifyObject

from voteit.core.bootstrap import bootstrap_voteit
from voteit.core.security import ROLE_VOTER


class ElectoralRegisterMethodTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _make_adapted_obj(self):
        from sverok_rm.models.electoral_register_method import ElectoralRegisterMethod
        return ElectoralRegisterMethod(self.meeting)
    
    def _fixures(self):
        self.config.scan('betahaus.pyracont.fields.password')
        self.config.scan('voteit.core.models.site')
        self.config.scan('voteit.core.models.agenda_template')
        self.config.scan('voteit.core.models.agenda_templates')
        self.config.scan('voteit.core.models.user')
        self.config.scan('voteit.core.models.users')
        from voteit.core.models.meeting import Meeting
        self.root = bootstrap_voteit(echo=False)
        self.meeting = Meeting()
        self.root['meeting'] = self.meeting

    def test_interface(self):
        from voteit.irl.models.interfaces import IElectoralRegisterMethod
        self._fixures()
        obj = self._make_adapted_obj()
        self.assertTrue(verifyObject(IElectoralRegisterMethod, obj))

    def test_apply(self):
        self._fixures()
        obj = self._make_adapted_obj()

        from voteit.core.models.user import User
        for delegate_number in ('50', '150', '250', 'admin'):
            userid = "user_%s" % delegate_number
            self.root.users[userid] = User(creators = [userid], 
                                           delegate_number = delegate_number)
            self.meeting.add_groups(userid, (ROLE_VOTER, ), event=False)
        
        obj.apply(('user_150', 'user_250'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_150'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_250'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_50'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
    def test_sverok_all_delegates(self):
        self._fixures()
        obj = self._make_adapted_obj()
        
        delegate_numbers = []
        
        # delegates
        for n in range(101, 202):
            delegate_numbers.append("%s" % n)
        
        # reserves
        for n in range(202, 298):
            delegate_numbers.append("%s" % n)
        
        # clerks
        for n in range(1, 54):
            delegate_numbers.append("%s" % n)
            
        # add users
        userids = []
        from voteit.core.models.user import User
        for delegate_number in delegate_numbers:
            userid = "user_%s" % delegate_number
            self.root.users[userid] = User(creators = [userid], 
                                           delegate_number = delegate_number)
            userids.append(userid)
        
        userids.append('admin')
        
        obj.apply(userids)
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_101'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_201'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_202'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_297'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_1'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_53'))
                
    def test_sverok_missing_delegates(self):
        self._fixures()
        obj = self._make_adapted_obj()
        
        delegate_numbers = []
        
        # delegates
        for n in range(101, 200):
            delegate_numbers.append("%s" % n)
        
        # reserves
        for n in range(202, 298):
            delegate_numbers.append("%s" % n)
        
        # clerks
        for n in range(1, 54):
            delegate_numbers.append("%s" % n)
            
        # add users
        userids = []
        from voteit.core.models.user import User
        for delegate_number in delegate_numbers:
            userid = "user_%s" % delegate_number
            self.root.users[userid] = User(creators = [userid], 
                                           delegate_number = delegate_number)
            userids.append(userid)
        
        userids.append('admin')
        
        obj.apply(userids)
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_101'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_199'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_200'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_201'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_202'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('user_203'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_204'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_297'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_1'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('user_53'))