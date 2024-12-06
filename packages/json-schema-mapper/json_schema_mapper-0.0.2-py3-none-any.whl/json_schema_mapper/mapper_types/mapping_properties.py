from typing import Optional


class MappingProperties:

    def __init__(self, *,
                 is_many: Optional[bool] = None,
                 is_optional: Optional[bool] = None):
        self.__is_many = is_many
        self.__is_optional = is_optional

    @property
    def is_many(self) -> bool:
        if not self.__is_many:
            return False
        return self.__is_many

    @is_many.setter
    def is_many(self, value: bool):
        if self.__is_many is not None:
            pass
            # raise ValueError("is_many has already been set.")
        self.__is_many = value

    @property
    def is_optional(self) -> bool:
        if not self.__is_optional:
            return False
        return self.__is_optional

    @is_optional.setter
    def is_optional(self, value: bool):
        if self.__is_many is not None:
            pass
            # raise ValueError("is_optional has already been set.")
        self.__is_many = value
