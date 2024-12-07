from dictstruct._main import DictStruct


class LazyDictStruct(DictStruct, frozen=True):  # type: ignore [call-arg,misc]
    """
    A subclass of DictStruct that supports JIT decoding of field values.

    It exists to optimize performance and memory usage by storing field values in a raw, undecoded format and decoding them only when accessed.

    This class is frozen, meaning its fields cannot be modified after creation.

    Example:
        >>> import msgspec
        >>> from functools import cached_property
        >>> class MyStruct(LazyDictStruct):
        ...     _myField: msgspec.Raw = msgspec.field(name='myField')
        ...     @cached_property
        ...     def myField(self) -> str:
        ...         '''Decode the raw JSON data into a python object when accessed.'''
        ...         return msgspec.json.decode(self._myField, type=str)
        ...
        >>> raw_data = msgspec.json.encode({"myField": "some value"})
        >>> my_struct = MyStruct(_myField=raw_data)
        >>> print(my_struct.myField)
        "some value"
    """

    def __init_subclass__(cls, *args, **kwargs):
        """
        Initialize a subclass of LazyDictStruct.

        Resolve any lazy field names (prefixed with an underscore) and overwrite
        `cls.__struct_fields__` so it contains the names of the materialized properties
        you defined on your subclass.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        See Also:
            :class:`DictStruct` for the base class implementation.
        """
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ == "StructMeta":
            return

        try:
            struct_fields = cls.__struct_fields__
        except AttributeError:
            # TODO: debug this
            # raise TypeError(cls, dir(cls), issubclass(cls, Struct))
            return

        resolved_fields = tuple(
            field[1:] if field[0] == "_" else field for field in struct_fields
        )
        cls.__struct_fields__ = resolved_fields
