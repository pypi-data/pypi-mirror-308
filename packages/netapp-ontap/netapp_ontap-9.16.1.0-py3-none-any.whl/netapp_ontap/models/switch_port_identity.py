r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortIdentity", "SwitchPortIdentitySchema"]
__pdoc__ = {
    "SwitchPortIdentitySchema.resource": False,
    "SwitchPortIdentitySchema.opts": False,
    "SwitchPortIdentity": False,
}


class SwitchPortIdentitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortIdentity object"""

    index = Size(data_key="index", allow_none=True)
    r""" Interface Index. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Interface Name. """

    number = Size(data_key="number", allow_none=True)
    r""" Interface Number. """

    @property
    def resource(self):
        return SwitchPortIdentity

    gettable_fields = [
        "index",
        "name",
        "number",
    ]
    """index,name,number,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SwitchPortIdentity(Resource):

    _schema = SwitchPortIdentitySchema
