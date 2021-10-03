import random
import string
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional, Union, Any

from pandas import DataFrame


class ColumnType(Enum):
    STR = auto()
    INT = auto()
    HEX = auto()

    @staticmethod
    def resolve_type_from(s: str) -> 'ColumnType':
        if s == "str":
            return ColumnType.STR
        elif s == "int":
            return ColumnType.INT
        elif s == "hex":
            return ColumnType.HEX
        raise RuntimeError(f"Unsupported column type: {s}")

    @staticmethod
    def gen_random_value(some_type: 'ColumnType') -> Union[int, str]:
        return ColumnType.random_generator[some_type]()

    @staticmethod
    def string_to_value(some_type: 'ColumnType', st: string) -> Union[int, str]:
        return ColumnType.from_string[some_type](st)


ColumnType.from_string = {
    ColumnType.STR: lambda s: s,
    ColumnType.INT: lambda s: int(s),
    ColumnType.HEX: lambda s: int(s, base=16)
}

ColumnType.random_generator = {
    ColumnType.STR: lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
    ColumnType.INT: lambda: random.randint(-10 ** 5, 10 ** 5),
    ColumnType.HEX: lambda: random.randint(-10 ** 5, 10 ** 5)
}


@dataclass(frozen=True)
class ColumnInfo:
    name: str
    type: ColumnType


@dataclass(frozen=True)
class TableInfo:
    columns_type: Dict[str, ColumnType]

    def create_df(self, data: List[List[Any]]) -> DataFrame:
        return DataFrame(columns=self.columns_type.keys(), data=data)

    def hex_columns(self, table: DataFrame) -> None:
        for cl_name, cl_type in self.columns_type.items():
            if cl_type == ColumnType.HEX:
                table[cl_name] = table[cl_name].apply(hex)

    @staticmethod
    def create_by_list(list_of_columns: List[ColumnInfo]) -> 'TableInfo':
        column_type = {cl_info.name: cl_info.type for cl_info in list_of_columns}
        return TableInfo(column_type)


@dataclass(frozen=True)
class ColumnCondition:
    name: str
    desired_value: Optional[str]


@dataclass(frozen=True)
class Condition:
    column_conditions: List[ColumnCondition]

    @staticmethod
    def get_empty() -> 'Condition':
        return Condition([])
