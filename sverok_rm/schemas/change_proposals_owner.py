import colander

from voteit.core.validators import deferred_existing_userid_validator
from voteit.core.schemas.permissions import deferred_autocompleting_userid_widget

from betahaus.pyracont.decorators import schema_factory


@schema_factory('ProposalsOwnersSchema')
class ProposalsOwnersSchema(colander.Schema):
    proposals = colander.Schema() #Populated later


def add_proposals_owner_nodes(schema, proposals):
    for prop in proposals:
        name = prop.__name__
        schema.add(colander.SchemaNode(colander.String(),
                                       name = name,
                                       validator = deferred_existing_userid_validator,
                                       widget = deferred_autocompleting_userid_widget,))
