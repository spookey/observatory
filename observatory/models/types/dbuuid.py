from uuid import UUID

from sqlalchemy.types import BINARY, TypeDecorator

# pylint: disable=abstract-method


class DBuuid(TypeDecorator):
    impl = BINARY

    @staticmethod
    def load_dialect(dialect):
        return dialect.type_descriptor(BINARY(16))

    @staticmethod
    def process_bind_param(value, _):
        if value is None:
            return None
        if isinstance(value, UUID):
            return value.bytes
        if isinstance(value, bytes):
            return UUID(bytes=value).bytes
        if isinstance(value, int):
            return UUID(int=value).bytes
        if isinstance(value, str):
            return UUID(hex=value).bytes

        raise ValueError(f'value {value} is not a valid uuid')

    @staticmethod
    def process_result_value(value, _):
        if value is None:
            return None
        if not isinstance(value, UUID):
            return UUID(bytes=value)
        return value
