from typing import Tuple

from RandomTableGenerator.RowGenerator import RowGenerator
from RandomTableGenerator.TableInfo import TableInfo, Condition
import pandas as pd


def generate_table(table_info: TableInfo, condition: Condition,
                   size: int, ratio: float, seed: int) -> Tuple[pd.DataFrame, pd.Series]:
    random_generator = RowGenerator(table_info, Condition.get_empty())
    generator_with_condition = RowGenerator(table_info, condition)

    assert 1 >= ratio >= 0
    target_num = int(size * ratio)
    table = table_info.create_df([])

    random_rows = [random_generator.generate_row() for _ in range(size - target_num)]
    table = table.append(table_info.create_df(random_rows))

    random_rows_with_condition = [generator_with_condition.generate_row() for _ in range(target_num)]
    table = table.append(table_info.create_df(random_rows_with_condition))

    table = table.sample(frac=1, random_state=seed).reset_index(drop=True)
    mask = generator_with_condition.fits(table)

    return table, mask
