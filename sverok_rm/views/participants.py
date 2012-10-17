from pyramid.view import view_config

from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.participants import ParticipantsView
from voteit.core.fanstaticlib import voteit_participants


class ScoutParticipantsView(ParticipantsView):

    @view_config(name="participants", context=IMeeting, renderer="templates/participants.pt", permission=security.VIEW)
    def scout_participants_view(self):
        voteit_participants.need
        return super(ScoutParticipantsView, self).participants_view()

    @view_config(name = "_participants_data.json", context = IMeeting,
                 renderer = "json", permission=security.VIEW, xhr = True)
    def scout_participants_json_data(self):
        """ Return a json object with participant data.
            Will return json with this structure:
            
            .. code-block :: py
            
                {'userid':{'first_name': '<name>',
                           'last_name': '<name>',
                           'email': '<email>',
                           'extras: {'delegate_number': '<delegate_number>',},
                           'role_discuss': '<bool>', #<etc...>,
                          }
        """
        users = self.api.root.users
        results = {}
        #Find the users
        for userid in security.find_authorized_userids(self.context, (security.VIEW,)):
            user = users.get(userid, None)
            if user:
                results[userid] = dict(
                    first_name = user.get_field_value('first_name', u""),
                    last_name = user.get_field_value('last_name', u""),
                    email = user.get_field_value('email', u""),
                    extras = dict(delegate_number = user.get_field_value('delegate_number', u""),),
                    #Make sure context is meeting here!
                    roles = self.context.get_groups(userid)
                )
        return results
