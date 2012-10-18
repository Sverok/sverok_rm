import colander
from unittest import TestCase

from pyramid import testing


class TicketValidatorTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    
    @property
    def _cut(self):
        from sverok_rm.schemas.delegate_ticket import TicketValidator
        return TicketValidator

    def _fixture(self):
        from voteit.core.models.meeting import Meeting
        from sverok_rm.models.delegate_ticket import DelegateTicket
        from sverok_rm.models.delegate_ticket import DelegateTicketStorage
        meeting = Meeting()
        tickets = DelegateTicketStorage(meeting)

        self.ticket = DelegateTicket(100)
        tickets.add(self.ticket)
        return meeting

    def _token_schema(self):
        from sverok_rm.schemas.delegate_ticket import ClaimTicketSchema
        return ClaimTicketSchema()

    def test_wrong_context(self):
        self.assertRaises(AssertionError, self._cut, testing.DummyModel())

    def test_nonexistent_ticket(self):
        meeting = self._fixture()
        obj = self._cut(meeting)
        node = self._token_schema()
        self.assertRaises(colander.Invalid, obj, node, 'dummy')

    def test_correct_token(self):
        meeting = self._fixture()
        obj = self._cut(meeting)
        node = self._token_schema()
        self.assertEqual(obj(node, self.ticket.token), None)