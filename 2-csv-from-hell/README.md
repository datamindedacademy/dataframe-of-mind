# Reading in data: the CSV from hell

An extremely common task is going to be _reading in data_. The most cross-compatible format for tabular data is CSV, but this can present its own challenges.

## Task

From the root folder, run `uv run python 2-csv-from-hell/generate_csv.py`. This command will generate 2 CSV files in the data directory: `measurements.csv` and `batch_measurements.csv`.

- Try to read in both csv files with Polars, see what you need to change in order to first succesfully read them in.
- Consider the data you are outputting, is everything as it should be? Take datatypes into consideration!
