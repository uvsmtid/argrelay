from marshmallow import Schema, fields, validates_schema, INCLUDE

from argrelay.enum_desc.ReservedEnvelopeClass import ReservedEnvelopeClass
from argrelay.misc_helper.TypeDesc import TypeDesc
from argrelay.schema_config_interp.FunctionEnvelopeInstanceDataSchema import function_envelope_instance_data_desc

envelope_id_ = "envelope_id"
"""
Not required (yet) field within `envelope_metadata` with unique id for `data_envelope`.
If provided, it is given to MongoDB as `id_` (otherwise, if not provided, MongoDB auto-generates one).
"""

envelope_class_ = "envelope_class"
"""
Required field within `envelope_metadata` with unique id for `envelope_class` which defines schema for `instance_data`.
"""

instance_data_ = "instance_data"
"""
Data specific to `envelope_class`.
Unlike `envelope_payload` `argrelay` does not inspect, `instance_data` can be inspected
(if not inspected by `argrelay`, but by its plugins) and this data has schema implied or defined somewhere.
"""

envelope_payload_ = "envelope_payload"
"""
Data `argrelay` does not inspect.
"""

context_control_ = "context_control"

class DataEnvelopeSchema(Schema):
    """
    Schema for all :class:`StaticDataSchema.data_envelopes`

    Note that this schema definition (unlike many others) is not used to `Schema.dump` `dict` instances
    because `data_envelope`-s contain arbitrary top-level keys used as (search) metadata.
    Because these top-level keys are arbitrary, they cannot be defined in this schema.
    Because they are missing in the schema, they do not survive `Schema.dump`.
    This is a known issue/limitation of `marshmallow` - the `Meta.unknown` field is only used on `Schema.load`
    to allow extra keys in, but `Schema.dump` simply do not serialize them.
    """

    class Meta:
        # All other fields of data envelope becomes its metadata available for search queries.
        # Note that it does not work for `Schema.dump`:
        unknown = INCLUDE
        strict = True

    envelope_id = fields.String(
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    envelope_class = fields.String(
        required = True,
    )

    """
    Data specific to `envelope_class`.
    Each envelope class may define its own schema for that data.
    For example, `ReservedEnvelopeClass.ClassFunction` defines `FunctionEnvelopeInstanceDataSchema`.
    """
    instance_data = fields.Dict(
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    """
    Arbitrary schemaless data (payload) wrapped by `DataEnvelopeSchema`.
    It is not inspected by `argrelay`.
    """
    envelope_payload = fields.Dict(
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    """
    List of arg types to be pushed to the next `args_context` to query next `data_envelope`-s.
    """
    context_control = fields.List(
        fields.String(),
        # TODO: make it required for predictability - isn't it required?
        required = False,
    )

    @validates_schema
    def validate_known(self, input_dict, **kwargs):
        if input_dict[envelope_class_] == ReservedEnvelopeClass.ClassFunction.name:
            function_envelope_instance_data_desc.validate_dict(input_dict[instance_data_])


data_envelope_desc = TypeDesc(
    dict_schema = DataEnvelopeSchema(),
    ref_name = DataEnvelopeSchema.__name__,
    dict_example = {
        envelope_id_: "some_unique_id",
        envelope_class_: ReservedEnvelopeClass.ClassFunction.name,
        instance_data_: function_envelope_instance_data_desc.dict_example,
        envelope_payload_: {},
        context_control_: [
            "SomeTypeB",
        ],
        "SomeTypeA": "A_value_1",
        "SomeTypeB": "B_value_1",
        "SomeTypeC": "C_value_1",
    },
    default_file_path = "",
)
