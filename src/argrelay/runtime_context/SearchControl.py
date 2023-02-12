from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SearchControl:
    """
    FS_31_70_49_15:
    Object to specify what arg types will be used in search (and how they are mapped to named arg keys).
    """

    # TODO: In short, function plugin should populate envelope_class inside curr_assigned_types_to_values
    #       (probably with new ArgSource.MandatoryValue with highest priority).
    #       Move to `context_control` (out of this `search_control` here):
    #       Avoid special case when only some specific arg type `ReservedArgType.EnvelopeClass` is propagated
    #       this special mechanism and the rest of arg types are propagated via FS_46_96_59_05.
    envelope_class: str = field(default_factory = lambda: None)

    # A specs how to query `data_envelope` for this `EnvelopeContainer` (which arg types to use).
    # Direct list to preserve order:
    keys_to_types_list: list[dict[str, str]] = field(default_factory = lambda: [])

    # `keys_to_types_dict` is derived from `keys_to_types_list`:
    # Direct dict for quick lookup:
    keys_to_types_dict: dict[str, str] = field(init = False, default_factory = lambda: {})

    # `types_to_keys_dict` is derived from `keys_to_types_dict`:
    # Reverse lookup:
    types_to_keys_dict: dict[str, str] = field(init = False, default_factory = lambda: {})

    def __post_init__(self):
        self._init_derived_fields()

    def _init_derived_fields(self):
        self.keys_to_types_dict = self.convert_list_of_ordered_singular_dicts_to_unordered_dict(
            self.keys_to_types_list
        )

        # generate reverse:
        self.types_to_keys_dict = {
            v: k for k, v in
            self.keys_to_types_dict.items()
        }

    @staticmethod
    def convert_list_of_ordered_singular_dicts_to_unordered_dict(dict_list: list[dict]) -> dict:
        """
        Convert ordered list[dict] (with dict having single { key: value }) into unordered dict { keys: values }.
        """
        converted_dict = {}
        for key_to_value_dict in dict_list:
            curr_key = next(iter(key_to_value_dict))
            curr_value = key_to_value_dict[curr_key]
            converted_dict[curr_key] = curr_value

        return converted_dict
