import unittest

from pyramid import testing
from zope.interface.verify import verifyObject

from voteit.core.security import ROLE_VOTER


ALL_TEST_USERS = set(('50', '150', '250', 'admin'))
VOTERS = set(('150', '250'))

class ElectoralRegisterMethodTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _make_adapted_obj(self):
        from sverok_rm.models.electoral_register_method import ElectoralRegisterMethod
        from voteit.core.models.meeting import Meeting
        self.meeting = Meeting()
        return ElectoralRegisterMethod(self.meeting)

    def test_interface(self):
        from voteit.irl.models.interfaces import IElectoralRegisterMethod
        obj = self._make_adapted_obj()
        self.assertTrue(verifyObject(IElectoralRegisterMethod, obj))

    def test_apply(self):
        obj = self._make_adapted_obj()

        for userid in ALL_TEST_USERS:
            self.meeting.add_groups(userid, (ROLE_VOTER, ), event=False)
        
        obj.apply(VOTERS)
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('150'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('250'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('50'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
    def test_sverok_all_delegates(self):
        obj = self._make_adapted_obj()
        
        userids = []
        
        userids.append('admin')
        
        # delegates
        for n in range(101, 202):
            userids.append("%s" % n)
        
        # reserves
        for n in range(202, 298):
            userids.append("%s" % n)
        
        # clerks
        for n in range(1, 54):
            userids.append("%s" % n)
            
        obj.apply(userids)
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('101'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('201'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('202'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('297'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('1'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('53'))
                
    def test_sverok_missing_delegates(self):
        obj = self._make_adapted_obj()
        
        userids = []
        
        userids.append('admin')
        
        # delegates
        for n in range(101, 200):
            userids.append("%s" % n)
        
        # reserves
        for n in range(202, 298):
            userids.append("%s" % n)
        
        # clerks
        for n in range(1, 54):
            userids.append("%s" % n)
        
        obj.apply(userids)
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('101'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('199'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('200'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('201'))
        
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('202'))
        self.assertIn(ROLE_VOTER, self.meeting.get_groups('203'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('204'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('297'))
        
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('1'))
        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('53'))