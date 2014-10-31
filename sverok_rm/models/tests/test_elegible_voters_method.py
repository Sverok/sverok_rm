import unittest

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from voteit.core.bootstrap import bootstrap_voteit
from voteit.core.security import ROLE_VOTER
from voteit.core.models.meeting import Meeting

from voteit.irl.models.interfaces import IElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.interfaces import IParticipantNumbers


class ElegibleVotersMethodTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(request = testing.DummyRequest())

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from sverok_rm.models.elegible_voters_method import SverokElegibleVotersMethod
        return SverokElegibleVotersMethod

    def _meeting_presence(self, context):
        return self.config.registry.getAdapter(context, IMeetingPresence)

    def _fixture(self):
        self.config.include('voteit.irl')

    def _add_delegate_numbers(self, meeting):
        pns = self.config.registry.getAdapter(meeting, IParticipantNumbers)
        pns.new_tickets('admin', 90, 110)
        for i in range(90, 110): #Reminder: that means 90-109
            ticket = pns.tickets[i]
            token = ticket.token
            pns.claim_ticket('user_%s' % i, token)

    def test_verify_class(self):
        self.failUnless(verifyClass(IElegibleVotersMethod, self._cut))

    def test_verify_object(self):
        self.failUnless(verifyObject(IElegibleVotersMethod, self._cut(Meeting())))

    def test_get_voters_nothing_done(self):
        self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(Meeting())
        self.assertEqual(obj.get_voters(request = request), set())
        
    def test_get_voters_with_delegate_numbers_no_present(self):
        self._fixture()
        request = testing.DummyRequest()
        meeting = Meeting()
        self._add_delegate_numbers(meeting)
        obj = self._cut(meeting)
        result = obj.get_voters(request = request, max_voters = 5)
        self.assertEqual(len(result), 0)

    def test_get_voters_with_delegate_numbers_all_present(self):
        self._fixture()
        request = testing.DummyRequest()
        meeting = Meeting()
        self._add_delegate_numbers(meeting)
        obj = self._cut(meeting)
        mp = self._meeting_presence(meeting)
        mp.start_check()
        for i in range(90, 110):
            mp.add('user_%s' % i)
        result = obj.get_voters(request = request, max_voters = 5)
        self.assertEqual(len(result), 5)
        expected = set(['user_%s' % i for i in range(101, 106)])
        self.assertEqual(result, expected)

    def test_get_voters_with_delegate_numbers_some_present(self):
        self._fixture()
        request = testing.DummyRequest()
        meeting = Meeting()
        self._add_delegate_numbers(meeting)
        obj = self._cut(meeting)
        mp = self._meeting_presence(meeting)
        mp.start_check()
        for i in (90, 101, 105, 109):
            mp.add('user_%s' % i)
        result = obj.get_voters(request = request, max_voters = 5)
        self.assertEqual(len(result), 3)
        expected = set(['user_%s' % i for i in (101, 105, 109,)])
        self.assertEqual(result, expected)

    def test_get_voters_with_delegate_numbers_some_present_but_without_delegate_number(self):
        self._fixture()
        request = testing.DummyRequest()
        meeting = Meeting()
        self._add_delegate_numbers(meeting)
        obj = self._cut(meeting)
        mp = self._meeting_presence(meeting)
        mp.start_check()
        for i in range(90, 115):
            mp.add('user_%s' % i)
        result = obj.get_voters(request = request, max_voters = 50)
        self.assertEqual(len(result), 9)
        expected = set(['user_%s' % i for i in range(101, 110)])
        self.assertEqual(result, expected)
