from pyramid.threadlocal import get_current_request

from voteit.core.models.interfaces import IMeeting
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence

from sverok_rm import SverokMF as _
from sverok_rm.models.interfaces import IDelegateNumberStorage


class SverokElegibleVotersMethod(ElegibleVotersMethod):
    name = 'sverok_voters_method'
    title = _(u"Sverok method")
    description = u""

    def get_voters(self, **kw):
        request = kw.get('request', get_current_request())
        max_voters = kw.get('max_voters', 101) #Good to be able to change it when testing :)
        delegate_numbers = request.registry.getAdapter(self.context, IDelegateNumberStorage)
        meeting_presence = request.registry.getAdapter(self.context, IMeetingPresence)
        potential_delegates = {}
        for userid in meeting_presence.present_userids:
            delegate_number = delegate_numbers.get(userid)
            try:
                #Might be None!
                delegate_number = int(delegate_number)
            except TypeError:
                #...which is handled here
                continue
            potential_delegates[delegate_number] = userid

        # loop through delegates starting from 101 and give the first 101 the voter role
        i = 0
        sorted_delegate_numbers = sorted([int(x) for x in potential_delegates.keys()])
        voting_userids = set()
        for delegate_number in sorted_delegate_numbers:
            if int(delegate_number) >= 101:
                #We found a match and will use up voting rights
                i += 1
                voting_userids.add(potential_delegates[delegate_number])
            if i >= max_voters:
                break;
        return voting_userids


def includeme(config):
    """ Include method (adapter) so it can be found by the system that sets voting rights. """
    config.registry.registerAdapter(SverokElegibleVotersMethod,
                                    (IMeeting,),
                                    name=SverokElegibleVotersMethod.name)
