from pyramid.view import view_config

from voteit.core.views.base_view import BaseView
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IPoll
from voteit.core.security import MODERATE_MEETING


class ProjectorView(BaseView):

    @view_config(context=IAgendaItem, name="projector", renderer="templates/projector.pt", permission=MODERATE_MEETING)
    def view(self):
        """ """

        self.response['polls_ongoing'] = self.api.get_restricted_content(self.context, iface=IPoll, sort_on='created', states='ongoing')
        self.response['polls_upcoming'] = self.api.get_restricted_content(self.context, iface=IPoll, sort_on='created', states='upcoming')
        self.response['polls_closed'] = self.api.get_restricted_content(self.context, iface=IPoll, sort_on='created', states='closed')
        
        return self.response
