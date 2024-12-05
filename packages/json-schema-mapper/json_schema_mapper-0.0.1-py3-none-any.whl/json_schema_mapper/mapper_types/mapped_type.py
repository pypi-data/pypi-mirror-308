from typing import Dict, Any, List, Optional

from json_schema_mapper.mapper_types.\
    mapping_properties import MappingProperties


class MappedType:

    def __init__(self,
                 attr_name: Optional[str] = None,
                 attr_type: Optional[Any] = None):
        self.__properties = MappingProperties()
        self.__mapped_type_children: List[MappedType] = []
        self.__attr_name = attr_name
        self.__attr_type = attr_type

    @property
    def mapped_children(self) -> Dict[str, Any]:
        return self.__mapped_type_children.copy()

    @property
    def properties(self) -> MappingProperties:
        return self.__properties

    @property
    def name(self) -> Optional[str]:
        return self.__attr_name

    @property
    def type(self) -> Any:
        return self.__attr_type

    def add_to_mapped_children(self, mapped_type: "MappedType"):
        self.__mapped_type_children.append(mapped_type)
