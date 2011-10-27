from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.response import Response
from pyramid.url import resource_url
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import find_root

from sverok_rm.models.interfaces import IElectoralRegister
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import VIEW
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_VOTER

#FIXME: translations

class ElectoralRegisterView(object):
    """ 
    """
    
    def __init__(self, request):
        from voteit.core.views.api import APIView
        self.api = APIView(request.context, request)
    
        self.userid = authenticated_userid(request)
        if not self.userid:
            raise Forbidden("You're not allowed to access this view.")
        
        self.request = request
        self.register = self.request.registry.getAdapter(self.request.context, IElectoralRegister)

    @view_config(name="clear_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def clear(self):
        """ 
        """
        self.register.clear()
        
        self.api.flash_messages.add(u"Electoral register is cleared.")
        return HTTPFound(location=resource_url(self.request.context, self.request))
        
    @view_config(name="add_electoral_register", context=IMeeting, permission=VIEW)
    def add(self):
        """ 
        """
        self.register.add(self.userid)
        
        self.api.flash_messages.add(u"Thanks, you have registered your attendance.")
        return HTTPFound(location=resource_url(self.request.context, self.request))
        
    @view_config(name="close_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def close(self):
        """ 
        """
        self.register.close()
        
        return HTTPFound(location=resource_url(self.request.context, self.request)+'view_electoral_register')
        
    @view_config(name="view_electoral_register", context=IMeeting, renderer="templates/electoral_register.pt", permission=MODERATE_MEETING)
    def view(self):
        root = find_root(self.request.context)
        
        def _get_user(userid):
            return root['users'][userid]

        def _is_voter(userid):
            groups = self.request.context.get_groups(userid)
            if ROLE_VOTER in groups:
                return u"Yes"
            
            return u"No"
        
        response = {}
        response['api'] = self.api
        #FIXME: sort them according to the Sverok way
        response['register'] = self.register.register
        response['get_user'] = _get_user
        response['is_voter'] = _is_voter
        
        return response
