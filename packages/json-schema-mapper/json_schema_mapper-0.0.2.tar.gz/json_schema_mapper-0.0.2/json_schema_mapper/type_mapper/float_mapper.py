from typing import List

from json_schema_mapper.mapper_types import MappedType
from json_schema_mapper.type_mapper.base_type_mapper import BaseTypeMapper


class FloatMapper(BaseTypeMapper):
    """Float open character Mapper."""

    def __init__(self, mapped_type_stack: List[MappedType]):
        super().__init__(mapped_type_stack)

    def perform_mapping_on_list(self, json_schema: str) -> str:
        has_colon = ':' in json_schema
        type_entry = "float"
        type_entry_index = json_schema.find(type_entry)

        new_json_schema = ''
        attr_name = None

        if has_colon:
            attr_name = json_schema.split(':')[0]
            new_json_schema = json_schema[type_entry_index +
                                          len(type_entry):]

        new_mapped_type = MappedType(
            attr_name=attr_name,
            attr_type=float
        )

        try:
            last_mapped_type = self._current_mapped_type
            last_mapped_type.add_to_mapped_children(new_mapped_type)
        except KeyError:
            self._add_mapped_type_to_stack(new_mapped_type)

        return new_json_schema
