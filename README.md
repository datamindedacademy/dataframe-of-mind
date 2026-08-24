# DataFrame of Mind with Polars and PySpark

[![Dataminded Academy](https://raw.githubusercontent.com/datamindedacademy/branding/main/assets/badge.svg)](https://github.com/datamindedacademy)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/datamindedacademy/dataframe-of-mind)

A hands-on course about DataFrames and data processing with two analytics
engines: [Polars](https://pola.rs) and [PySpark](https://spark.apache.org/docs/latest/api/python/).
You write queries against a fake dataset of polar bear health measurements, and
along the way pick up lazy evaluation, query plans, relational operations,
window functions, joins and UDFs.

Each exercise folder has its own README with the goal and the questions to
answer. The notebooks next to them are where you work.

## Getting started in GitHub Codespaces

Click the badge above, or **Code → Codespaces → Create codespace on main** on
the repository page. The devcontainer builds Python 3.13, a JDK for Spark and
`uv`, then runs `uv sync --frozen`. First build takes a few minutes.

When it is done, open a notebook and pick the `.venv` kernel. Everything is
installed.

## Getting started locally

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a
JDK 17 or later (PySpark needs it). Then:

```bash
uv sync
```

Run anything through `uv run`, for example `uv run jupyter lab`, and select the
`.venv` kernel in the notebook.

## The exercises

Work through them in order. Exercise 2 and 3 generate the data files the later
ones use, so do not skip them.

| Folder | Topic |
| ------ | ----- |
| [`demo-reading-data`](demo-reading-data/) | Demo: what the lazy API saves you when reading from object storage |
| [`1-operational-vs-analytic`](1-operational-vs-analytic/) | Operational versus analytical data |
| [`2-csv-from-hell`](2-csv-from-hell/) | Reading CSV, and the ways it goes wrong |
| [`3-basic-transforms`](3-basic-transforms/) | Project, filter, rename, union |
| [`4-window-aggregations`](4-window-aggregations/) | Window functions and aggregations |
| [`5-joins`](5-joins/) | Joins |
| [`6-udf`](6-udf/) | User defined functions |

The data lands in `data/` and is gitignored. Regenerate it at any time:

```bash
uv run python 2-csv-from-hell/generate_csv.py
uv run python 3-basic-transforms/generate_parquet.py
```

## The slides

`docs/DataFrame-of-Mind.pdf` is the exported deck. To run it live:

```bash
cd docs
npm install
npm run dev
```

That serves the deck on http://localhost:3030, press `p` for presenter mode. In
a Codespace, the port is forwarded automatically. See
[`docs/README.md`](docs/README.md) for how the deck is put together.

## Reference

- [Polars documentation](https://docs.pola.rs/api/python/stable/reference/index.html)
- [PySpark documentation](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/index.html)
