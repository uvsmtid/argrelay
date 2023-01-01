from __future__ import annotations

from copy import deepcopy
from unittest import TestCase

import mongomock

from argrelay.data_schema.MongoConfigSchema import mongo_config_desc, database_name_
from argrelay.interp_plugin.AbstractInterp import AbstractInterp
from argrelay.interp_plugin.FirstArgInterpFactory import FirstArgInterpFactory
from argrelay.relay_demo.ServiceInterpFactory import ServiceInterpFactory, service_interp_config_desc
from argrelay.runtime_context.InterpContext import InterpContext
from misc_helper import parse_line_and_cpos, default_test_parsed_context
from relay_demo.test_relay_demo import relay_demo_static_data_object


# noinspection PyMethodMayBeStatic
class ThisTestCase(TestCase):

    def run_test(self, test_line):
        (command_line, cursor_cpos) = parse_line_and_cpos(test_line)
        parsed_ctx = default_test_parsed_context(command_line, cursor_cpos)
        first_arg_vals_to_next_interp_factory_ids = {
            "known_command1": ServiceInterpFactory.__name__,
            "known_command2": FirstArgInterpFactory.__name__,
        }
        config_dict = {
            "first_arg_vals_to_next_interp_factory_ids": first_arg_vals_to_next_interp_factory_ids,
        }
        interp_factories = {
            FirstArgInterpFactory.__name__: FirstArgInterpFactory(
                config_dict = config_dict,
            ),
            ServiceInterpFactory.__name__: ServiceInterpFactory(
                config_dict = service_interp_config_desc.dict_example,
            ),
        }
        mongo_db = mongomock.MongoClient()[mongo_config_desc.dict_example[database_name_]]
        interp_ctx = InterpContext(parsed_ctx, deepcopy(relay_demo_static_data_object), interp_factories, mongo_db)
        line_interp = interp_factories[FirstArgInterpFactory.__name__].create_interp(interp_ctx)
        line_interp.consume_key_args()
        line_interp.consume_pos_args()
        curr_interp: AbstractInterp = line_interp.next_interp()
        self.assertEqual([0], interp_ctx.consumed_tokens)
        first_token_value = interp_ctx.parsed_ctx.all_tokens[0]
        self.assertTrue(first_token_value in first_arg_vals_to_next_interp_factory_ids.keys())
        interp_factory_id = first_arg_vals_to_next_interp_factory_ids[first_token_value]
        interp_factory_instance = interp_factories[interp_factory_id]
        self.assertTrue(
            curr_interp.__class__.__name__ in interp_factory_instance.__class__.__name__,
            "factory class name contains instance class name (true in this case)",
        )

    def test_consume_pos_args_unknown(self):
        test_line = "unknown_command prod|"
        with self.assertRaises(KeyError):
            self.run_test(test_line)

    def test_consume_pos_args_known(self):
        test_line = "known_command1 prod|"
        self.run_test(test_line)
        test_line = "known_command2 prod|"
        self.run_test(test_line)

    def test_consume_pos_args_with_no_args(self):
        test_line = "  | "
        with self.assertRaises(IndexError):
            self.run_test(test_line)
