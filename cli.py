import argparse

DEFAULT_FILE = "daily-stocks.parquet"


def get_args():
    parser = argparse.ArgumentParser(
        prog="polygon-py",
        description="",
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="commands")

    parser_get = subparsers.add_parser("get", help="get polygon data")
    parser_get.add_argument("year", help="year of date to get")
    parser_get.add_argument("month", help="month of date to get")
    parser_get.add_argument("day", help="day of date to get")
    parser_get.add_argument(
        "-i", "--input", type=str, default=DEFAULT_FILE, help="input file"
    )
    parser_get.add_argument(
        "-o", "--output", type=str, default=DEFAULT_FILE, help="output file"
    )

    parser_remove = subparsers.add_parser("remove", help="remove polygon data")
    parser_remove.add_argument("year", help="year of date to remove")
    parser_remove.add_argument("month", help="month of date to remove")
    parser_remove.add_argument("day", help="day of date to remove")
    parser_remove.add_argument(
        "-i", "--input", type=str, default=DEFAULT_FILE, help="input file"
    )
    parser_remove.add_argument(
        "-o", "--output", type=str, default=DEFAULT_FILE, help="output file"
    )

    parser_list = subparsers.add_parser("list", help="list polygon data")
    parser_list.add_argument(
        "file", help="file to list", type=str, default=DEFAULT_FILE
    )

    return parser.parse_args()
