"""
Generate dummy parquet data for demonstrating Polars read_parquet vs scan_parquet
and Hive-partitioned vs non-partitioned data reading.

This script creates:
1. A single non-partitioned parquet file (data/sales.parquet)
2. Hive-partitioned parquet files (data/sales_partitioned/year=XXXX/month=XX/*.parquet)
"""

import shutil
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl
import pyarrow.parquet as pq
from faker import Faker

fake = Faker()
Faker.seed(42)
# Configuration
NUM_RECORDS = 100_000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)
OUTPUT_DIR = Path(__file__).parents[1] / "data"

PRODUCTS = [
    {
        "product_id": 1,
        "name": "Laptop",
        "category": "Electronics",
        "base_price": 999.99,
    },
    {
        "product_id": 2,
        "name": "Smartphone",
        "category": "Electronics",
        "base_price": 699.99,
    },
    {
        "product_id": 3,
        "name": "Headphones",
        "category": "Electronics",
        "base_price": 149.99,
    },
    {
        "product_id": 4,
        "name": "Coffee Maker",
        "category": "Appliances",
        "base_price": 89.99,
    },
    {"product_id": 5, "name": "Blender", "category": "Appliances", "base_price": 49.99},
    {
        "product_id": 6,
        "name": "Running Shoes",
        "category": "Sports",
        "base_price": 129.99,
    },
    {"product_id": 7, "name": "Yoga Mat", "category": "Sports", "base_price": 29.99},
    {
        "product_id": 8,
        "name": "Desk Chair",
        "category": "Furniture",
        "base_price": 299.99,
    },
    {
        "product_id": 9,
        "name": "Bookshelf",
        "category": "Furniture",
        "base_price": 199.99,
    },
    {
        "product_id": 10,
        "name": "Water Bottle",
        "category": "Sports",
        "base_price": 24.99,
    },
]

REGIONS = ["North", "South", "East", "West", "Central"]


def generate_sales_data(num_records: int) -> pl.DataFrame:
    records = []
    date_range_days = (END_DATE - START_DATE).days

    for i in range(num_records):
        random_days = fake.random_int(0, date_range_days)
        random_seconds = fake.random_int(0, 86399)  # seconds in a day
        timestamp = START_DATE + timedelta(days=random_days, seconds=random_seconds)

        product = fake.random_element(PRODUCTS)

        quantity = fake.random_int(1, 10)

        # Add some price variation (±10%)
        price_variation = 1 + fake.random.uniform(-0.1, 0.1)
        unit_price = round(product["base_price"] * price_variation, 2)

        records.append(
            {
                "sale_id": i + 1,
                "timestamp": timestamp,
                "product_id": product["product_id"],
                "product_name": product["name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "region": fake.random_element(REGIONS),
            }
        )

    df = pl.DataFrame(records)
    df = df.with_columns(
        [
            pl.col("timestamp").dt.year().alias("year"),
            pl.col("timestamp").dt.month().alias("month"),
        ]
    )

    return df


def write_non_partitioned(df: pl.DataFrame, output_path: Path) -> None:
    """
    Write the DataFrame as a single parquet file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  Created: {output_path} ({size_mb:.2f} MB)")


def write_hive_partitioned(df: pl.DataFrame, output_dir: Path) -> None:
    """
    Write the DataFrame as Hive-partitioned parquet files.

    Hive partitioning organizes data into a directory structure like:
        output_dir/year=2022/month=1/data.parquet
        output_dir/year=2022/month=2/data.parquet
        ...
    """

    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Convert to PyArrow table and use write_to_dataset for reliable Hive partitioning
    table = df.to_arrow()
    pq.write_to_dataset(
        table,
        root_path=str(output_dir),
        partition_cols=["year", "month"],
    )

    parquet_files = list(output_dir.rglob("*.parquet"))
    total_size = sum(f.stat().st_size for f in parquet_files)
    print(
        f"  Created: {len(parquet_files)} partition files ({total_size / (1024 * 1024):.2f} MB total)"
    )


if __name__ == "__main__":
    sales_df = generate_sales_data(NUM_RECORDS)

    write_non_partitioned(sales_df, OUTPUT_DIR / "sales.parquet")
    write_hive_partitioned(sales_df, OUTPUT_DIR / "sales_partitioned")
