import argparse
import random

from RandomTableGenerator import generate_table, TableInfo
from RandomTableGenerator.TableInfo import ColumnType, ColumnInfo, ColumnCondition, Condition


def column_type(s: str) -> ColumnInfo:
    try:
        tokens = s.split(':')
        return ColumnInfo(tokens[0], ColumnType.resolve_type_from(tokens[1]))
    except Exception as ex:
        raise argparse.ArgumentTypeError("Columns must be name:type") from ex


def column_condition(s: str) -> ColumnCondition:
    try:
        tokens = s.split(':')
        value = None
        if len(tokens) > 1:
            value = tokens[1]
        return ColumnCondition(tokens[0], value)
    except Exception as ex:
        raise argparse.ArgumentTypeError("Columns must be name:value or just name") from ex


def create_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file', type=str,
                        help='file name for result')
    parser.add_argument('--seed', type=int, default=0,
                        help='random seed')
    parser.add_argument('--columns_info', type=column_type, nargs="+", required=True,
                        help='list of all columns name and type in format name:type')
    parser.add_argument('--conditions', type=column_condition, nargs="+", required=False,
                        help='generation condition as list of column names with optional constants')
    return parser


def main(args):
    random.seed(args.seed)
    table_info = TableInfo.create_by_list(args.columns_info)
    table, mask = generate_table(table_info, Condition(args.conditions), 1000, 0.2,
                                 args.seed)

    table_info.hex_columns(table)
    table.to_csv(args.file, index=False)
    table[mask].to_csv(f"{args.file}.ans", index=False)


if __name__ == '__main__':
    main(create_parser().parse_args())
