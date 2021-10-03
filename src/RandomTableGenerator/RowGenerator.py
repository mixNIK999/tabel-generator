from dataclasses import dataclass
from typing import Union, Dict, List, Any

from RandomTableGenerator.TableInfo import TableInfo, Condition, ColumnType

import pandas as pd


class RowGenerator:
    table_info: TableInfo
    condition: Condition

    column_constants: Dict[str, Union[int, str]]

    def __init__(self, table_info: TableInfo, condition: Condition) -> None:
        self.table_info = table_info
        self.condition = condition
        self.column_constants = {}

        for cl_cond in condition.column_conditions:
            assert cl_cond.name in table_info.columns_type
            cl_type = table_info.columns_type[cl_cond.name]
            if cl_cond.desired_value is not None:
                self.column_constants[cl_cond.name] = ColumnType.string_to_value(cl_type, cl_cond.desired_value)
            else:
                self.column_constants[cl_cond.name] = ColumnType.gen_random_value(cl_type)

    def _gen_value(self, cl_name, cl_type) -> Union[int, str]:
        val = self.column_constants.get(cl_name)
        if val is None:
            val = ColumnType.gen_random_value(cl_type)
        return val

    def fits(self, table: pd.DataFrame) -> pd.Series:
        mask = pd.Series([True] * table.shape[0])
        for cl_name, cl_const in self.column_constants.items():
            mask &= table[cl_name] == cl_const
        return mask

    def generate_row(self) -> List[Union[int, str]]:
        return [self._gen_value(cl_name, cl_type) for cl_name, cl_type in self.table_info.columns_type.items()]
