import os
import logging
import pandas as pd
import requests

from cli import DEFAULT_FILE


def handle_get(args, polygon_key):
    if os.path.splitext(args.input)[-1] != ".parquet":
        logging.error(f'Provided input file "{args.input}" is not a parquet file')
        return

    old_df = pd.DataFrame()
    if os.path.exists(args.input):
        logging.info(f'Reading existing data from "{args.input}"')
        old_df = pd.read_parquet(args.input)
    else:
        logging.info("Using default file as input")

    if not os.path.exists(args.input) and args.input != DEFAULT_FILE:
        logging.warning(f'Provided input file "{args.input}" does not exist. Skipping.')

    logging.info(f"Fetching polygon data for {args.year}-{args.month}-{args.day}")
    resp = requests.get(
        f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{args.year}-{args.month:>02}-{args.day:>02}/?apiKey={polygon_key}"
    )

    new_df = pd.DataFrame(resp.json()["results"])

    logging.info("Adding date column")
    new_df = new_df.assign(
        date=pd.to_datetime(args.year + "-" + args.month + "-" + args.day)
    )

    logging.info("Removing t column")
    new_df.drop(columns=["t"], inplace=True)

    logging.info("Removing null rows")
    new_df.dropna(subset=["n", "vw", "v"], inplace=True)

    logging.info("Setting column datatypes")
    new_df = new_df.astype(
        {
            "T": "str",
            "date": "datetime64[ns]",
            "o": "float32",
            "h": "float32",
            "l": "float32",
            "c": "float32",
            "v": "float32",
            "vw": "float32",
            "n": "int32",
        }
    )

    logging.info("Merging old data with new data")
    merged_df = pd.concat([old_df, new_df], ignore_index=True)

    if os.path.exists(args.output):
        logging.info(f'Output file "{args.output}" already exists. Overwriting.')

    merged_df.to_parquet(args.output)


def handle_remove(args):
    if os.path.splitext(args.input)[-1] != ".parquet":
        logging.error(f'Provided input file "{args.input}" is not a parquet file')
        return

    df = pd.DataFrame()
    if os.path.exists(args.input):
        logging.info(f'Reading existing data from "{args.input}"')
        df = pd.read_parquet(args.input)
    else:
        logging.info("Using default file as input")

    if not os.path.exists(args.input) and args.input != DEFAULT_FILE:
        logging.warning(f'Provided input file "{args.input}" does not exist. Skipping.')

    logging.info(f"Removing {args.year}-{args.month}-{args.day}")
    df = df[df["date"] != pd.to_datetime(args.year + "-" + args.month + "-" + args.day)]

    if os.path.exists(args.output):
        logging.info(f'Output file "{args.output}" already exists. Overwriting.')

    df.to_parquet(args.output)


def handle_list(args):
    if os.path.splitext(args.input)[-1] != ".parquet":
        logging.error(f'Provided input file "{args.input}" is not a parquet file')
        return

    if not os.path.exists(args.input):
        logging.error(f'Provided input file "{args.input}" does not exist')
        return

    df = pd.read_parquet(args.input)

    print("Your input file has the date range:")
    print(df["date"].min().date(), "to", df["date"].max().date())
    full_range = pd.date_range(start=df["date"].min(), end=df["date"].max())
    missing_date = full_range.difference(df["date"])

    print("\nHowever are you missing these dates:")
    for date in missing_date:
        if date.weekday() >= 5:
            continue

        print(date.date())
