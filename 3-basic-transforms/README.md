# Basic Transforms: Project, Filter, Rename, Union

Relational algebra forms the cornerstone of SQL, the de-facto standard for querying data of Relational Database Management Systems (RDBMS), in which the bulk of operational data is stored.

Instead of re-inventing the wheel, analytical engines have largely adopted a SQL or SQL-like interace for querying data, making SQL the lingua franca of the analytics space. The DataFrame API is a higher level of abstraction, which similarly gets translated into a query plan optimized by the analytical engine.

## Task

As you have seen in the previous exercise, we will be working with a (fake) dataset concerning the health and wellbeing of polar bears in a zoo. We have two types of measurements: batch measurements, performed by veterinarians every few days, and "real time" measurements sent out by wireless sensors.

Run `uv run python 3-basic-transforms/generate_parquet.py` in order to generate the required parquet files for this and the following exercises.

In this exercise, we are going to use some of the basic relational operations to answer the following questions:

- Was there in 2022 an injured polar bear older than 15 (i.e. a senior polar bear)? Bonus question: can you answer the same question using Polars [categorical types](https://docs.pola.rs/user-guide/expressions/categorical-data-and-enums/#data-type-categorical)?
- How many times was Blizzard Bob's name capitalized in the batch measurements?
- Was Chilly Willy ever sick with a temperature above 40 degrees? (Hint: you might need to perform some data wrangling by performing a union and downfill.)

First try to answer the questions with Polars' DataFrame API. Can you answer them as well using Polars' SQL dialect?
