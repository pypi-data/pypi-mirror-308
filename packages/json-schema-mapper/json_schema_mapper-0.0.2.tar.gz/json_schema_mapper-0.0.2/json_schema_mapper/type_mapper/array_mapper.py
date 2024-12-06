from typing import List

from json_schema_mapper.mapper_types import MappedType
from json_schema_mapper.type_mapper.base_type_mapper import BaseTypeMapper


class ArrayMapper(BaseTypeMapper):
    """Array character Mapper."""

    def __init__(self, mapped_type_stack: List[MappedType]):
        super().__init__(mapped_type_stack)

    def perform_mapping_on_list(self, json_schema: str) -> str:
        array_index = json_schema.find('[]')

        new_json_schema = ''

        try:
            if array_index != -1:
                new_json_schema = json_schema[array_index + 1:]
        except IndexError:
            pass

        current_map_type = self._current_mapped_type
        current_map_type.properties.is_many = True

        return new_json_schema
