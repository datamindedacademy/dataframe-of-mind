# Basic Transforms: Project, Filter, Rename, Union, ...

Relational algebra forms the cornerstone of SQL, the de-facto standard for querying data of Relational Database Management Systems (RDBMS), in which the bulk of operational data is stored. 

Instead of re-inventing the wheel, analytical engines have largely adopted a SQL or SQL-like interace for querying data, making SQL the lingua franca of the analytics space. The DataFrame API is a higher level of abstraction, which similarly gets translated into a query plan optimized by the analytical engine.

In this exercise, we are going to use some of the basic relational operations to answer the following questions:

- Was there in 2022 an injured polar bear older than 15 (i.e. a senior polar bear)? Bonus question: can you answer the same question using Polars [categorical types](https://docs.pola.rs/user-guide/concepts/data-types/categoricals/#enum-vs-categorical)?
- How many times was Blizzard Bob's name capitalized in the batch measurements?
- Was Cubby Coldpaw ever sick with a temperature above 40 degrees? (tip: union + downfill)

First try to answer the questions with Polars' DataFrame API. Can you answer them as well using Polars' SQL dialect?
