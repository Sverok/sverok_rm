import unittest
from datetime import datetime

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid.exceptions import Forbidden

from voteit.core.models.interfaces import IMeeting

from sverok_rm.models.interfaces import IDelegateTicketStorage
from sverok_rm.models.interfaces import IDelegateTicket


class DelegateTicketStorageTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_zcml')
        self.config.load_zcml('sverok_rm:configure.zcml')

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from sverok_rm.models.delegate_ticket import DelegateTicketStorage
        return DelegateTicketStorage
    
    def _make_obj(self):
        return self._cut(self._make_meeting())
    
    def _make_meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting()

    def test_verify_class(self):
        self.assertTrue(verifyClass(IDelegateTicketStorage, self._cut))

    def test_verify_obj(self):
        self.assertTrue(verifyObject(IDelegateTicketStorage, self._make_obj()))
        
    def test_add(self):
        obj = self._make_obj()
        
        from sverok_rm.models.delegate_ticket import DelegateTicket
        ticket = DelegateTicket(100)
        
        obj.add(ticket)
        
        self.assertIn(ticket.token, obj.delegate_tickets)
        self.assertIs(ticket, obj.delegate_tickets[ticket.token])
        self.assertTrue(IMeeting.providedBy(ticket.__parent__))


class DelegateTicketTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_zcml')
        self.config.load_zcml('sverok_rm:configure.zcml')

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from sverok_rm.models.delegate_ticket import DelegateTicket
        return DelegateTicket
    
    def _make_obj(self):
        return self._cut(100)
    
    def _make_meeting(self):
        from voteit.core.models.meeting import Meeting
        meeting = Meeting()
        return meeting
    
    def _make_ticket_storage(self, meeting):
        from sverok_rm.models.delegate_ticket import DelegateTicketStorage
        return DelegateTicketStorage(meeting)
    
    def _make_number_storage(self, meeting):
        from sverok_rm.models.delegate_numbers import DelegateNumberStorage
        return DelegateNumberStorage(meeting)

    def test_verify_class(self):
        self.assertTrue(verifyClass(IDelegateTicket, self._cut))

    def test_verify_obj(self):
        self.assertTrue(verifyObject(IDelegateTicket, self._make_obj()))
        
    def test_claim_ticket(self):
        meeting = self._make_meeting()
        ticket_storage = self._make_ticket_storage(meeting)
        numbers_storage = self._make_number_storage(meeting)
        obj = self._make_obj()
        ticket_storage.add(obj)

        self.config.testing_securitypolicy(userid='some_user',
                                           permissive=True)

        request = testing.DummyRequest()
        ticket = ticket_storage.delegate_tickets[obj.token]
        ticket.claim(request)
        
        self.assertTrue(isinstance(ticket.closed, datetime))
        self.assertEqual(ticket.claimed_by, 'some_user')
        self.assertEqual(ticket.get_workflow_state(), 'closed')
        self.assertEqual(numbers_storage.get('some_user'), obj.delegate_number)

    def test_claim_closed(self):
        meeting = self._make_meeting()
        ticket_storage = self._make_ticket_storage(meeting)
        obj = self._make_obj()
        ticket_storage.add(obj)
    
        self.config.testing_securitypolicy(userid='some_user',
                                           permissive=True)
        
        request = testing.DummyRequest()
        ticket = ticket_storage.delegate_tickets[obj.token]
        
        #Set ticket to closed
        ticket.set_workflow_state(request, 'closed')
        
        self.assertRaises(Forbidden, ticket.claim, request)

    def test_claim_unathenticated(self):
        meeting = self._make_meeting()
        ticket_storage = self._make_ticket_storage(meeting)
        obj = self._make_obj()
        ticket_storage.add(obj)
        
        request = testing.DummyRequest()
        ticket = ticket_storage.delegate_tickets[obj.token]
        
        self.assertRaises(Forbidden, ticket.claim, request)
