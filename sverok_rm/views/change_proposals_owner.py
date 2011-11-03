import colander
import deform
from voteit.core.views.base_edit import BaseEdit

from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from voteit.core import VoteITMF as vmf
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_OWNER
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.models.schemas import button_update
from voteit.core.models.schemas import button_cancel

from sverok_rm.schemas.change_proposals_owner import add_proposals_owner_nodes


class ChangeProposalsOwner(BaseEdit):

    def _appstruct(self, proposals):
        results = {}
        for prop in proposals:
            results[prop.__name__] = prop.creators[0]
        return results

    @view_config(name="proposals_owner", context = IAgendaItem, permission = MODERATE_MEETING,
                 renderer = 'voteit.core:views/templates/base_edit.pt')
    def edit_proposals_owners(self):
        """ Change proposal owners. """
        
        schema = colander.Schema()
        proposals = self.context.get_content(iface = IProposal, sort_on = 'created')
        add_proposals_owner_nodes(schema, proposals)
        schema = schema.bind(context = self.context, request = self.request)
        form = deform.Form(schema, buttons = (button_update, button_cancel,))
        self.api.register_form_resources(form)
        url = resource_url(self.context, self.request)

        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(vmf(u"Canceled"))
            return HTTPFound(location = url)
        
        if 'update' in self.request.POST:
            #Walk through all props and check data
            controls = self.request.POST.items()
            try:
                #appstruct is deforms convention. It will be the submitted data in a dict.
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response

            updated = set()
            for (prop_name, owner) in appstruct.items():
                proposal = self.context[prop_name]
                old_owner = proposal.creators[0]
                if owner == old_owner:
                    continue
                #Remove Owner group from old owner?
                groups = list(proposal.get_groups(old_owner))
                if ROLE_OWNER in groups:
                    groups.remove(ROLE_OWNER)
                    proposal.set_groups(old_owner, groups)
                
                #Add owner to new owner
                proposal.add_groups(owner, [ROLE_OWNER])

                #Set new owner in creators attr - this will also trigger reindex catalog event so keep it last!
                proposal.set_field_appstruct({'creators': (owner,)})
                
                updated.add(prop_name)

            if updated:
                self.api.flash_messages.add(vmf(u"Successfully updated"))
            else:
                self.api.flash_messages.add(vmf(u"Nothing updated"))

            return HTTPFound(location = url)
        
        appstruct = self._appstruct(proposals)
        self.response['form'] = form.render(appstruct)
        return self.response
