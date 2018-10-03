# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import colander
import deform
from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import UserSchema
from arche.schemas import FinishRegistrationSchema
from voteit.core.schemas.meeting import EditMeetingSchema

"""
Plugin för att kunna skriva kön och pronomen
Eventuell patch för att visa det som byline, valbart.
MIGRERAD TILL VOTEIT DEFAULT PACKAGES. ANVÄND INTE DENNA!
"""


_PRONOMEN = (
    ('', '- Inget angett -'),
    ('den', 'Den'),
    ('han', 'Han'),
    ('hen', 'Hen'),
    ('hon', 'Hon'),
)
_PRONOMEN_TITLES = dict(_PRONOMEN)
del _PRONOMEN_TITLES['']


def add_pronomen_fields(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='pronomen',
            title="Pronomen",
            description="Kan visas i talarlistan om du anger det",
            missing="",
            widget=deform.widget.SelectWidget(values=_PRONOMEN),
        )
    )


def add_meeting_controls(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.Bool(),
            name='pronomen_on_sl',
            title="Visa pronomen i talarlista?",
            default=False,
            tab='advanced',
        )
    )


def get_pronomen(request, context):
    if getattr(request.meeting, 'pronomen_on_sl', False) == True:
        return _PRONOMEN_TITLES.get(getattr(context, 'pronomen', ''), '')


def includeme(config):
    config.add_subscriber(add_pronomen_fields, [UserSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_pronomen_fields, [FinishRegistrationSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_meeting_controls, [EditMeetingSchema, ISchemaCreatedEvent])

    #Add attributes
    from voteit.core.models.meeting import Meeting
    from voteit.core.models.user import User
    Meeting.pronomen_on_sl = False
    User.pronomen = ""

    #Override templates
    config.override_asset(to_override='voteit.debate:templates/',
                          override_with='sverok_rm:pronomen_overrides/')

    #Add request method
    config.add_request_method(get_pronomen)
