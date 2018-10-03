from arche import security
from pyramid.view import view_config
from voteit.core.models.interfaces import IMeeting
from voteit.debate.interfaces import ISpeakerLists
from voteit.irl.models.interfaces import IParticipantNumbers


@view_config(context = IMeeting,
             name = "active_list_speakers.json",
             permission = security.NO_PERMISSION_REQUIRED,
             renderer = "json")
def active_list_speakers(context, request):
    """ Returns a json structure with speakers in the current list
    """
    slists = request.speaker_lists
    active_list = slists.get(slists.get_active_list())
    root = context.__parent__
    data = {'active': None, 'queue': []}
    participant_numbers = request.registry.getAdapter(context, IParticipantNumbers)

    def get_user_data(pn):
        userid = participant_numbers.number_to_userid.get(pn, None)
        if userid:
            user = root.users[userid]
            img_plugin = user.get_image_plugin(request)
            img_url = ''
            if img_plugin:
                try:
                    img_url = img_plugin.url(300, request)
                except:
                    pass
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'userid': userid,
                'participant_number': pn,
                'pronoun': getattr(user, 'pronoun', ''),
                'profile_pic': img_url,
            }
        else:
            return {'participant_number': pn, 'profile_pic': ''}

    if active_list:
        if active_list.current != None:  # Note could be int 0!
            data['active'] = get_user_data(active_list.current)
        for num in active_list:
            data['queue'].append(get_user_data(num))
    return data


def includeme(config):
    config.scan(__name__)
