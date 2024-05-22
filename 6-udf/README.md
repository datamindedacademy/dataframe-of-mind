# User-Defined Functions (UDF)

User-defined functions are an escape-hatch: sometimes, the Polars Expression language just doesn't cut it, and a custom, Python function is needed. This is where UDFs come in.

UDFs in Polars come in three flavors:

- `map_rows`: a function that iterates over all rows, and returns a new DataFrame. This is the most flexible UDF, as it doesn't respect the schema: the output schema can be different from the input schema.
- `map_batches`: a function that iterates over one or multiple Series. The output must be a Series. In a `GroupBy` context, `map_batches` still consumes the entire Series, and not the different groups!
- `map_elements`: a function that iterates over the elements of a Series. The output must be a Series. In a `GroupBy` context, `map_elements` consumes the elements of the Series per group.

## Task

In this exercise, we want to figure out which non-weekend or holiday days attracted the most visitors. To do so, we'll write two user-defined functions:

- `is_weekend`: a function that determines whether a zoo opening date is a weekend day or not.
- `is_holiday`: a function that determines whether a zoo opening date is a holiday or not.

To determine whether a day is a holiday, have a look at the popular `holidays` python package: [https://pypi.org/project/holidays/](https://pypi.org/project/holidays/).
Are user-defined functions in this scenario the right tool for the job? Why (not)?
