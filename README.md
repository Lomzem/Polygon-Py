# Polygon-Py

A simple python script to fetch data from [polygon.io](https://polygon.io) and add it to a cumulative parquet file.

### Commands
- `get`: Fetch a date from [polygon.io]("https://polygon.io") and add it to the parquet file.
- `remove`: Remove a date from the parquet file.
- `list`: List all dates in the parquet file and missing dates.

For more info on usage:
```bash
polygon-py -h
```

### Adding Polygon.io API Key
The script requires users to supply their own API key from [polygon.io]("https://polygon.io"). Provide this key as the environment variable `POLYGON_IO_KEY` before using the script.

For example, you can add this to your `.bashrc`:
```bash
export POLYGON_IO_KEY="<key here>"
```
