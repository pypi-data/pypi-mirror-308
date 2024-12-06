from typing import List
from json_schema_mapper.mapper_types import MappedType
from json_schema_mapper.type_mapper.interface_type_mapper import ITypeMapper


class BaseTypeMapper(ITypeMapper):
    """Base type mapper."""

    def __init__(self, mapped_type_stack: List[MappedType]):
        self.__mapped_type_stack = mapped_type_stack

    @property
    def _current_mapped_type(self) -> MappedType:
        stack_length = len(self.__mapped_type_stack)
        if not stack_length:
            raise KeyError("Mapped type stack is empty.")
        current_mapped_type = self.__mapped_type_stack[-1]
        return current_mapped_type

    def _pop_current_mapped_type(self):
        stack_length = len(self.__mapped_type_stack)
        if not stack_length:
            raise KeyError("No Mapped type entry to pop.")
        if stack_length > 1:
            self.__mapped_type_stack.pop()

    def _add_mapped_type_to_stack(self, mapped_type: MappedType):
        self.__mapped_type_stack.append(mapped_type)
