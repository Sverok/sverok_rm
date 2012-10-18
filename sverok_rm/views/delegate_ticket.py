import deform
from deform import Form
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createSchema
from betahaus.viewcomponent.decorators import view_action


from voteit.core.security import VIEW
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.schemas import button_add
from voteit.core.models.schemas import button_cancel
from voteit.core.views.base_view import BaseView

from sverok_rm import SverokMF as _
from sverok_rm.models.delegate_ticket import DelegateTicket
from sverok_rm.models.delegate_ticket import DelegateTicketStorage
from sverok_rm.models.delegate_numbers import DelegateNumberStorage


class ClaimTicketView(BaseView):
    
    @view_config(name="delegate_ticket", context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt", permission = VIEW)
    def claim_ticket(self):
        
        self.response['title'] = _(u"Claim delegate ticket")
        schema = createSchema('ClaimDelegateTicketSchema').bind(context=self.context, request=self.request)
        form = Form(schema, buttons=(button_add, button_cancel))
        self.api.register_form_resources(form)

        if 'add' in self.request.POST:
            controls = self.request.params.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            tickets = DelegateTicketStorage(self.context)
            
            ticket = tickets.delegate_tickets[appstruct['token']]
            ticket.claim(self.request)
            self.api.flash_messages.add(_(u"You've have been assigned delegate number ${number}", mapping={'number': ticket.delegate_number}))
            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)
        
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))
            url = resource_url(self.api.root, self.request)
            return HTTPFound(location=url)

        #No action - Render add form
        self.response['form'] = form.render()
        return self.response
    
    
@view_action('participants_menu', 'claim_delegate_number', title = _(u"Claim delegate number"),
             link = "delegate_ticket", permission=VIEW)
def electoral_register_moderator_menu_link(context, request, va, **kw):
    api = kw['api']

    delegate_numbers = DelegateNumberStorage(api.meeting)
    if delegate_numbers.get(api.userid):
        return ""
    
    url = request.resource_url(api.meeting, va.kwargs['link']) 
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))