from marshmallow import Schema, fields, RAISE, post_load

from argrelay.api_ext.ConnectionConfig import ConnectionConfig
from argrelay.api_int.const_int import DEFAULT_IP_ADDRESS, DEFAULT_PORT_NUMBER
from argrelay.misc_helper.TypeDesc import TypeDesc


class ConnectionConfigSchema(Schema):
    class Meta:
        unknown = RAISE
        strict = True

    server_host_name = fields.String(
        default = DEFAULT_IP_ADDRESS,
    )
    server_port_number = fields.Integer(
        default = DEFAULT_PORT_NUMBER,
    )

    @post_load
    def make_object(self, input_dict, **kwargs):
        return ConnectionConfig(
            server_host_name = input_dict["server_host_name"],
            server_port_number = input_dict["server_port_number"],
        )


connection_config_desc = TypeDesc(
    object_schema = ConnectionConfigSchema(),
    ref_name = ConnectionConfigSchema.__name__,
    dict_example = {
        "server_host_name": DEFAULT_IP_ADDRESS,
        "server_port_number": DEFAULT_PORT_NUMBER,
    },
    default_file_path = "",
)
