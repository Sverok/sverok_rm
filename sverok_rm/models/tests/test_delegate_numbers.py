import unittest

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from sverok_rm.models.interfaces import IDelegateNumberStorage


class DelegateNumberStorageTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_zcml')
        self.config.load_zcml('sverok_rm:configure.zcml')

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from sverok_rm.models.delegate_numbers import DelegateNumberStorage
        return DelegateNumberStorage
    
    def _make_obj(self):
        return self._cut(self._make_meeting())
    
    def _make_meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting()

    def test_verify_class(self):
        self.assertTrue(verifyClass(IDelegateNumberStorage, self._cut))

    def test_verify_obj(self):
        self.assertTrue(verifyObject(IDelegateNumberStorage, self._make_obj()))
        
    def test_add(self):
        obj = self._make_obj()
        
        obj.add('dummy', 100)
        
        self.assertIn('dummy', obj.delegate_numbers)
        self.assertIs(100, obj.delegate_numbers['dummy'])
        
    def test_get(self):
        obj = self._make_obj()
        
        obj.add('dummy', 100)

        self.assertEqual(obj.get('dummy'), 100)

    def test_get_none(self):
        obj = self._make_obj()
        
        self.assertEqual(obj.get('dummy'), None)