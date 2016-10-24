# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import colander
import deform
from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import UserSchema
from arche.schemas import FinishRegistrationSchema

"""
Patch för att kunna skriva kön.
"""


_GENDER = (
    ('', '- Inget angett -'),
    ('man', 'Man'),
    ('kvinna', 'Kvinna'),
    ('ickebinar', 'Icke-binär'),
    ('fritext', 'Annat (använd fritextfältet)'),
)


def add_gender_fields(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='gender_select',
            title="Kön",
            missing="",
            widget=deform.widget.SelectWidget(values=_GENDER),
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='gender_freetext',
            title="Om du angav kön annat, vad?",
            missing="",
        )
    )


def includeme(config):
    config.add_subscriber(add_gender_fields, [UserSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_gender_fields, [FinishRegistrationSchema, ISchemaCreatedEvent])

    #Add attributes
    from voteit.core.models.user import User
    User.gender_select = ""
    User.gender_freetext = ""
