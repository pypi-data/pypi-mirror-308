from typing import List

from json_schema_mapper.mapper_types import MappedType
from json_schema_mapper.type_mapper.base_type_mapper import BaseTypeMapper


class SemiColonMapper(BaseTypeMapper):
    """Semi colon character Mapper."""

    def __init__(self, mapped_type_stack: List[MappedType]):
        super().__init__(mapped_type_stack)

    def perform_mapping_on_list(self, json_schema: str) -> str:
        semi_colon_index = json_schema.find(';')

        try:
            new_json_schema = json_schema[semi_colon_index + 1:]
        except IndexError:
            new_json_schema = ''

        return new_json_schema
