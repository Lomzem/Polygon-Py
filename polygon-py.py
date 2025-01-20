import cli
from commands import handle_get, handle_remove, handle_list

import os
import logging

POLYGON_API_KEY = "POLYGON_IO_KEY"


logging.basicConfig(level=logging.INFO)


def main():
    try:
        polygon_key = os.environ[POLYGON_API_KEY]
    except KeyError:
        print(f'Error: Missing environment variable: "{POLYGON_API_KEY}"')
        return

    args = cli.get_args()

    if args.command == "get":
        handle_get(args, polygon_key)

    elif args.command == "remove":
        handle_remove(args)

    elif args.command == "list":
        handle_list(args)


if __name__ == "__main__":
    main()
