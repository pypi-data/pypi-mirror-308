from abc import ABC, abstractmethod


class ITypeMapper(ABC):

    @abstractmethod
    def perform_mapping_on_list(self, json_schema: str) -> str:
        """Perform mapping on a list of MappedTypes"""
        pass
