from typing import List

from json_schema_mapper.mapper_types import MappedType
from json_schema_mapper.type_mapper.base_type_mapper import BaseTypeMapper


class DictCloseMapper(BaseTypeMapper):
    """Dict close character Mapper."""

    def __init__(self, mapped_type_stack: List[MappedType]):
        super().__init__(mapped_type_stack)

    def perform_mapping_on_list(self, json_schema: str) -> str:
        dict_close_index = json_schema.find('}')

        try:
            new_json_schema = json_schema[dict_close_index + 1:]
        except IndexError:
            new_json_schema = ''

        self._pop_current_mapped_type()

        return new_json_schema
