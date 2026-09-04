---
theme: dataminded
title: DataFrame of Mind
info: Data pipelines with Polars and PySpark. Data Minded Academy.
fonts:
  serif: El Messiri
  sans: DM Sans
transition: slide-left
layout: cover
subtitle: Data pipelines with Polars and PySpark · Data Minded Academy
---

# DataFrame of <span class="dm-accent">Mind</span>

---
layout: agenda
label: Contents
---

# Contents

1. Data and schemas
2. The engines: pandas, DuckDB, Polars
3. Expressing a query
4. How the engine executes it
5. Choosing an engine
6. PySpark

---
layout: section
---

# Data and <span class="dm-accent">schemas</span>

---
layout: default
label: 1 · Data and schemas
---

# Operational vs. <span class="dm-accent">Analytical</span> Data

<div class="ova">
<div class="ova-side">

<div class="ova-pill ova-pill--navy">Operational ⚡</div>

- Detailed events
- Fast and complete (ACID)
- Reads and writes **one record**, all of its fields

</div>

<div class="ova-bits">
  <img src="/img/bits.png" alt="A block of ones and zeros" />
  <div class="ova-row" v-click="1" />
  <div class="ova-col" v-click="2" />
  <svg class="ova-loop" viewBox="0 0 340 340" v-click="3">
    <path d="M 120.4 33.7 A 145 145 0 1 0 214 36"
          fill="none" stroke="var(--dm-connecting)" stroke-width="12" />
    <polygon points="0,-13 26,0 0,13" transform="translate(219.6, 33.7) rotate(200)"
             fill="var(--dm-connecting)" />
  </svg>
</div>

<div class="ova-side">

<div class="ova-pill ova-pill--violet">Analytical 🔍</div>

- Descriptive and predictive
- Slow and selective
- Reads **one field** across every record

</div>
</div>

<p class="ova-caption" v-click="3">Operations capture reality event by event, analytics finds the
patterns, and the patterns change how the next event is served.</p>

<!--
It is all the same bits in the end, ones and zeros. What differs is the shape of the access. An
operational system grabs a whole record: this customer, this order, right now. An analytical system
grabs one field over millions of records: every order value of the past year. That single difference
drives everything downstream, from the file format to the engine.

Third click: during operations we capture the richness of reality, details of every event, so the
business keeps running and customers are served well. Afterwards we understand the patterns hidden
in the chaos, and leverage them to serve customers better, which keeps the business alive.
-->

---
layout: default
label: 1 · Data and schemas
---

# <span class="dm-accent">Rows</span> group records; <span class="dm-accent">columns</span> group fields

<div class="storage-compare">
  <div class="storage-format storage-format--rows">
    <div class="storage-format-head">
      <strong>Row-oriented</strong>
      <span>one line per record</span>
    </div>
    <div class="storage-file" aria-label="The same data stored one record per line">
      <div class="storage-line storage-line--header">id,name,weight_kg,age,heart_rate,country</div>
      <div class="storage-line">8,Ana,210,4,76,CA</div>
      <div class="storage-line">1042,Nanook,480,15,54,NO</div>
      <div class="storage-line">73,Pipaluk,320,9,68,GL</div>
      <div class="storage-line storage-record-run">615,Siku,405,12,61,CA</div>
      <div class="storage-line">204,Nuka,260,6,72,US</div>
      <div class="storage-line">981,Tala,505,18,52,RU</div>
    </div>
    <p class="storage-question">Give me record <b>615</b></p>
  </div>

  <div class="storage-divider"><span>same data</span></div>

  <div class="storage-format storage-format--columns">
    <div class="storage-format-head">
      <strong>Column-oriented</strong>
      <span>one line per field</span>
    </div>
    <div class="storage-file" aria-label="The same data stored one field per line">
      <div class="storage-line storage-line--header">field,value1,value2,value3,value4,value5,value6</div>
      <div class="storage-line">id,8,1042,73,615,204,981</div>
      <div class="storage-line">name,Ana,Nanook,Pipaluk,Siku,Nuka,Tala</div>
      <div class="storage-line">weight_kg,210,480,320,405,260,505</div>
      <div class="storage-line storage-field-run">age,4,15,9,12,6,18</div>
      <div class="storage-line">heart_rate,76,54,68,61,72,52</div>
      <div class="storage-line">country,CA,NO,GL,CA,US,RU</div>
    </div>
    <p class="storage-question">Give me the highest <b>age</b></p>
  </div>
</div>

<p class="storage-punch" v-click="2">Same values, different order on disk, different work to retrieve them.</p>

<!--
This is the same tiny dataset written in two different orders. In the row-oriented version, put
your finger at the start of Nanook's line and move right: the whole record arrives in one sweep.
But to read every age, your finger has to jump to each line and count past several numeric fields.
A column-oriented format transposes the physical layout. Now every age is adjacent, while
reconstructing one bear means jumping between fields. Storage layout makes an access pattern cheap
by keeping the values it needs together.
-->

---
layout: statement
title: Exercise - operational vs analytical data
---

# Exercise time: operational vs. analytical data

<p class="mt-6 text-lg opacity-80"><code>1-operational-vs-analytic/</code></p>

---
layout: default
label: 1 · Data and schemas
---

# A schema gives values <span class="dm-accent">meaning</span>

<div class="meaning-flow">
  <div class="meaning-raw">
    <span>A record without context</span>
    <code>1042, Nanook, 480, 15, 54, NO</code>
  </div>

  <div class="meaning-arrow" v-click="1"><b>↓</b> add names and types</div>

  <div class="meaning-fields" v-click="1">
    <div><span>id</span><strong>1042</strong><small>Int64</small></div>
    <div><span>name</span><strong>Nanook</strong><small>String</small></div>
    <div><span>weight_kg</span><strong>480</strong><small>Int64</small></div>
    <div><span>age</span><strong>15</strong><small>Int64</small></div>
    <div><span>heart_rate</span><strong>54</strong><small>Int64</small></div>
    <div><span>country</span><strong>NO</strong><small>String</small></div>
  </div>
</div>

<p class="meaning-punch" v-click="2"><b>Layout</b> tells us where values are.
<b>Schema</b> tells us what they are.</p>

<!--
The exercise changed where the values were stored. A schema solves a different problem: it gives
those values names and types. Without a schema, 15 is just a number. With one, it is an age. Layout
is about location; schema is about interpretation.
-->

---
layout: default
label: 1 · Data and schemas
---

# File formats combine <span class="dm-accent">layout</span> and <span class="dm-accent">schema</span>

<div class="format-slide-body">
<DmColumns class="mt-6">
<DmColumn header="Record-oriented" tone="navy">

- **CSV / TSV**: text; schema supplied or inferred
- **Avro**: binary; writer schema stored with the data

<div class="fmt-logos fmt-logos--center">
  <img src="/img/logo-csv.png" alt="CSV" />
  <img src="/img/logo-avro.png" alt="Avro" />
</div>

</DmColumn>
<DmColumn header="Column-oriented" tone="violet" divider>

- **Parquet / ORC**: binary; schema and statistics stored in the file
- **Arrow IPC / Feather**: columnar interchange between tools

<div class="fmt-logos fmt-logos--center">
  <img src="/img/logo-parquet.png" alt="Parquet" />
  <img src="/img/logo-orc.png" alt="Apache ORC" />
  <img src="/img/logo-arrow.png" alt="Apache Arrow" />
</div>

</DmColumn>
</DmColumns>

<p class="format-punch">The format changes the physical representation, not what the data means.</p>
</div>

<!--
A file format answers both questions we have introduced: where are the values placed, and how does
the reader know what they mean? CSV keeps records as text and relies on outside knowledge for types.
Avro keeps records together and carries its writer schema. Parquet and ORC group data by column and
carry their schema and statistics. Arrow IPC is designed to exchange columnar data between tools.

Databases and table formats sit at another layer. Postgres and DuckDB manage data through an engine;
Delta and Iceberg organize data files into tables. They are useful examples later, but they are not
the same kind of thing as CSV, Avro or Parquet.

[Sources]
- https://avro.apache.org/docs/1.11.3/
- https://parquet.apache.org/
- https://orc.apache.org/docs/
- https://arrow.apache.org/docs/format/Columnar.html
-->

---
layout: default
label: 1 · Data and schemas
---

# Different formats, one <span class="dm-accent">DataFrame</span> abstraction

<div class="dataframe-figure">
  <div class="dataframe-example">
    <div class="dataframe-head">id<small>Int64</small></div>
    <div class="dataframe-head">name<small>String</small></div>
    <div class="dataframe-head">weight_kg<small>Int64</small></div>
    <div class="dataframe-head">age<small>Int64</small></div>
    <div class="dataframe-head">heart_rate<small>Int64</small></div>
    <div class="dataframe-head">country<small>String</small></div>
    <div>8</div>
    <div>Ana</div>
    <div>210</div>
    <div>4</div>
    <div>76</div>
    <div>CA</div>
    <div class="dataframe-row-hit">1042</div>
    <div class="dataframe-row-hit">Nanook</div>
    <div class="dataframe-row-hit">480</div>
    <div class="dataframe-row-hit">15</div>
    <div class="dataframe-row-hit">54</div>
    <div class="dataframe-row-hit">NO</div>
    <div>73</div>
    <div>Pipaluk</div>
    <div>320</div>
    <div>9</div>
    <div>68</div>
    <div>GL</div>
    <div>615</div>
    <div>Siku</div>
    <div>405</div>
    <div>12</div>
    <div>61</div>
    <div>CA</div>
  </div>
  <div class="dataframe-legend">
    <span class="dataframe-row-key"><b>Row</b> · one complete record</span>
    <span class="dataframe-column-key"><b>Column</b> · one typed field across records</span>
  </div>
</div>

<p class="dataframe-punch">Libraries let us work with rows and typed columns, independent of the source format.</p>

<!--
Put tabular data and its schema together and you have the mental model of a DataFrame. Rows are
records; columns are named, typed fields. The source format can change without changing that logical
model. The engines differ in how they execute operations, but they all let us work with this same
abstraction. That is the bridge to the libraries we compare next.
-->

---
layout: section
---

# Bring in the <span class="dm-accent">Animals</span> 🐼 🦆 🐻‍❄️

---
layout: default
label: 2 · The engines
---

# An engine turns a query into <span class="dm-accent">actual work</span>

<div class="flex justify-center mt-2">
  <img src="/img/etl-engine.png" alt="Sources feeding a processing engine that serves analytics" style="height: 268px" />
</div>

<p class="engine-punch">A <b>query engine</b> reads bytes in whatever layout they arrive, applies the
operations you asked for, and writes the result back out.</p>

<!--
Section 1 ended on the DataFrame: rows, typed columns, one logical model regardless of the file
format. That model does not execute itself. Something has to open the file, decide which bytes it
actually needs, run the work across cores, and hand back a result. That something is the query
engine, and it is what sits in the middle of every pipeline you will build.

The T in ETL is the engine's job. Extract and load are mostly I/O; the transform is where the
engine earns its keep. For the rest of the course we ask three questions about it, one per section:
how do you express what you want (section 3), how does the engine decide to run it (section 4), and
which engine should you pick (section 5).

The three we compare are pandas, DuckDB and Polars. They all give you the same DataFrame model, so
the interesting differences are underneath it.
-->

---
layout: default
label: 2 · The engines
---

# Three engines, one <span class="dm-accent">DataFrame</span>

<DmComparison
  class="engine-cmp mt-4"
  :rows="['Born 🐣', 'What it is 📖', 'You write 📝', 'Loved by ❤️']"
  :cols="['🐼 pandas', '🦆 DuckDB', '🐻‍❄️ Polars']"
>
  <template #r0c0>2008 🇺🇸</template>
  <template #r0c1>2019 🇳🇱</template>
  <template #r0c2>2020 🇳🇱</template>

  <template #r1c0>The original Python DataFrame library, and still the most widely taught.</template>
  <template #r1c1>A small analytics database that runs inside your Python process.</template>
  <template #r1c2>A newer DataFrame library, built for speed from the start.</template>

  <template #r2c0>Python</template>
  <template #r2c1>SQL</template>
  <template #r2c2>Python</template>

  <template #r3c0>Data scientists 👩‍🔬</template>
  <template #r3c1>Data analysts 👨‍💼</template>
  <template #r3c2>Data engineers 👷</template>
</DmComparison>

<p class="engine-punch">All three hand you the same DataFrame. What differs is how you
<b>ask</b> for it.</p>

<!--
Keep this slide short. It exists so nobody is lost when the next slide shows three snippets, not to
settle the choice.

The "loved by" row is the one to talk around, because it is a real pattern and not a rule. Data
scientists inherited pandas from the notebooks and courses they learned in, analysts reach for
DuckDB because it lets them stay in SQL, and engineers pick Polars when a pipeline has to be fast
and predictable. Ask the room which of the three they already use, it tells you who you are talking
to for the rest of the day.

Notice the dates. pandas had roughly a decade on its own, and then two engines arrived within a
year of each other. That is not a coincidence: it is what happens when one machine gets big enough
to do work that used to need a cluster. Section 5 has the graph.

If someone asks "so which one should I use", say that it depends on the size of the job and who
maintains it, and that there is a decision diagram waiting in section 5. Do not settle it here.
They cannot weigh the trade-offs before they know what the differences cost.

Deliberately not on this slide: GitHub stars, which change monthly and have never decided an
architecture, and the execution details. If an experienced room pushes: pandas is eager and
single-core with a row index inherited from NumPy; DuckDB is a vectorised SQL engine that can spill
to disk; Polars is Arrow-backed, has no index, plans the whole query before running it, and uses
every core. Every one of those terms gets taught later, so do not lead with them.
-->

---
layout: default
label: 2 · The engines
---

# The same question in <span class="dm-accent">three dialects</span>

<p class="engine-question">Average heart rate per bear, adults only.</p>

<DmColumns class="mt-3" :gap="16">
<DmColumn header="🐼 pandas" tone="navy">

```py
df = pd.read_parquet(path)
adults = df[df["age"] >= 4]
(adults
  .groupby("name")["heart_rate"]
  .mean())
```

</DmColumn>
<DmColumn header="🦆 DuckDB" tone="navy" divider>

```sql
SELECT name, avg(heart_rate)
FROM 'measurements.parquet'
WHERE age >= 4
GROUP BY name
```

</DmColumn>
<DmColumn header="🐻‍❄️ Polars" tone="violet" divider>

```py
(pl.scan_parquet(path)
  .filter(pl.col("age") >= 4)
  .group_by("name")
  .agg(
    pl.col("heart_rate").mean()
  )
  .collect())
```

</DmColumn>
</DmColumns>

<!--
Same question, same answer, three styles. Ask the room which one they would rather debug at
half past five on a Friday, and let them argue for a minute.

Three things to point at. pandas mutates and re-binds: `adults` is a new object, and the boolean
mask is a separate expression from the column it filters. DuckDB is pure SQL over a file, with no
Python object in sight. Polars reads as one pipeline, and `pl.col("age")` is not a value but a
description of a column that the engine will resolve later.

Note `scan_parquet` and `collect` in the Polars version. Nothing happens until `collect` is called.
Do not explain why yet, just plant it: that is section 4.

These styles have names, and they are the subject of section 3.
-->

---
layout: default
label: 2 · The engines
---

# Polars is a side project that got <span class="dm-accent">out of hand</span> 🤷‍♂️

<DmColumns class="mt-6">
<DmColumn>

- Main author: Ritchie Vink 🇳🇱, a structural engineer by education
- Started during the COVID-19 pandemic 😷, as an exercise in learning Rust
- No database career behind it, so no inherited assumptions: no index, expressions everywhere, Arrow from day one
- Full-time on Polars since July 2023, when he founded Polars Inc. to fund the work
- The company sells enterprise support and Polars Cloud

</DmColumn>
<DmColumn divider>

<div class="flex justify-center">
  <img src="/img/ritchie-vink.png" alt="Ritchie Vink" style="height: 240px; border-radius: 12px" />
</div>

</DmColumn>
</DmColumns>

<!--
This is a short human beat, not a biography. The one bullet that matters is the third: the API you
are about to use looks the way it does because it was not designed by someone carrying thirty years
of RDBMS habits. Dropping the index was a choice, and every expression you write for the rest of
the day is downstream of it.

Worth saying out loud: this is a young project with a company attached, and it moves fast. Pin your
version, and read release notes before upgrading.
-->

---
layout: default
label: 2 · The engines
---

# How to read a CSV with <span class="dm-accent">polars</span>

```py
pl.read_csv(
    source: str | Path | IO[str] | IO[bytes] | bytes,
    *,
    has_header: bool = True,
    columns: Sequence[int] | Sequence[str] | None = None,
    new_columns: Sequence[str] | None = None,
    separator: str = ',',
    comment_prefix: str | None = None,
    skip_rows: int = 0,
    skip_lines: int = 0,
    schema: SchemaDict | None = None,
    schema_overrides: Mapping[str, PolarsDataType] | Sequence[PolarsDataType] | None = None,
    null_values: str | Sequence[str] | dict[str, str] | None = None,
    empty_string_is_null: bool = True,
    infer_schema: bool = True,
    infer_schema_length: int | None = 100,
    ..., # there are many more arguments you can pass
) -> DataFrame
```


A CSV may name its columns, never their <span class="dm-accent">types</span>. Since Polars works with DataFrames, you will need to help it understanding the schema.

<!--
Reconcile this with the formats slide from section 1, because someone always asks. That slide said
CSV is "text; schema supplied or inferred", and this is the same claim from the reader's side. A
header row can carry column *names*, which is why `has_header` exists. Nothing in the file carries
*types*, which is why every other argument on this slide exists.

Look at the defaults, they are the whole story. `has_header=True` assumes a header. `separator=','`
assumes commas. `try_parse_dates=False` means dates arrive as strings unless you ask. Each default
is a guess about a file the library has never seen, and `schema` or `schema_overrides` is how you
replace a guess with a decision.

The failure mode to name out loud: a wrong guess does not raise. The read succeeds, the column is a
String instead of a date or a number, and nobody notices until a join returns nothing. So the habit
is to look at `df.schema` before you look at the data.

Do not walk through a worked example. They should discover which arguments their two files need,
and the error messages on the way are worth more than a solution on a slide.
-->

---
layout: statement
title: Demo - reading a dirty csv
---

# Demo time: a dirty, dirty CSV

<p class="mt-6 text-lg opacity-80"><code>demo-reading-data/</code> and <code>2-csv-from-hell/</code></p>

<!--
Two files, both deliberately awful, and no README hand-holding: they have the arguments from the
previous slide and the docs, and that is the point. Let them hit the error messages. Polars error
messages are unusually good, and reading one properly is a skill worth ten minutes of frustration.

The checkpoint question when they say they are done: "is every column the type you want?" Most
people stop at "it read without an error" and leave numbers and timestamps sitting as strings.

Note for the instructor: `demo-reading-data/` is about scan versus read against object storage,
which is lazy evaluation and I/O pushdown. That is section 4 material and it lands better next to
the hive partitioning demo. Consider running only `2-csv-from-hell/` here.
-->

---
layout: section
---

# Querying and <span class="dm-accent">Transforming</span> Data

---
layout: default
label: 3 · Expressing a query
---

# Imperative, declarative and <span class="dm-accent">functional</span> styles

<DmColumns class="mt-4" :gap="16">
<DmColumn header="Imperative" tone="navy">

```py
affordable_cars = []
for car in cars:
  if car.price <= 30_000:
    affordable_cars.append(car)
```

Step by step, like a recipe.

</DmColumn>
<DmColumn header="Declarative" tone="navy" divider>

```sql
SELECT brand, price FROM cars
WHERE price <= 30000
```

Describe what you want, let an optimised engine work out how.

</DmColumn>
<DmColumn header="Functional" tone="violet" divider>

```py
cars = pl.read_csv("cars.csv")
affordable = cars.filter(
  pl.col("price") <= 30_000
)
```

Chain functions into a pipeline, no duplication, no mutation.

</DmColumn>
</DmColumns>

<!--
Exercise: split into three groups, write the same transformation logic in each style, compare the
results and discuss readability.
-->

---
layout: default
label: 3 · Expressing a query
---

# Relational algebra, the cornerstone of <span class="dm-accent">RDBMS</span>

<div class="flex justify-center mt-6">
  <img src="/img/relational-algebra.png" alt="Relational algebra operators" style="height: 300px" />
</div>

<p class="text-center mt-4 opacity-80">Projection, selection, rename, set operations and the whole family of joins.</p>

<!--
Voilà, summarised in a single slide.
-->

---
layout: default
label: 3 · Expressing a query
---

# Project, filter, rename, union, <span class="dm-accent">join</span>

<DmColumns class="mt-4">
<DmColumn header="SQL" tone="navy">

```sql
SELECT
    price as car_price
FROM
    (
        SELECT * FROM old_cars
        UNION
        SELECT * FROM new_cars
    )
WHERE car_price > 30000
```

</DmColumn>
<DmColumn header="Polars" tone="violet" divider>

```py
import polars as pl

df = (
  pl.concat(
    pl.read_csv("old_cars.csv"),
    pl.read_csv("new_cars.csv"),
  )
  .select(
    pl.col("price").alias("car_price")
  )
  .filter(pl.col("car_price") > 30_000)
)
```

</DmColumn>
</DmColumns>

---
layout: default
label: 3 · Expressing a query
---

# To SQL or not to <span class="dm-accent">SQL</span>?

<DmColumns class="mt-4">
<DmColumn header="SQL wins on" tone="navy">

- Readability
- Getting stuff done
- Easy to learn, everyone speaks it

<img src="/img/logo-dbt.png" alt="dbt" style="height: 36px; margin-top: 28px" />

</DmColumn>
<DmColumn header="A DataFrame API wins on" tone="violet" divider>

- Abstraction (functions, modules)
- Control flow (if, for, while)
- Testing
- Ecosystem (linting, typing, packaging)

</DmColumn>
</DmColumns>

<div class="flex justify-center mt-2">
  <img src="/img/hamlet.jpg" alt="Hamlet holding a skull" style="height: 118px; border-radius: 8px" />
</div>

<!--
A discussion about the advantages and disadvantages of SQL vs. the DataFrame API.

Advantages: readable, lingua franca, powerful.
Disadvantages: higher level abstractions are missing, not general purpose, limited support for
software engineering practices (testing, version control, linting), which is what dbt tries to fix.

In the case of Polars: there is a SQLContext, but it lags the development of the DataFrame API a
bit. Stability should improve.
-->

---
layout: default
label: 3 · Expressing a query
---

# Beyond relational algebra: contexts and <span class="dm-accent">expressions</span>

Polars adds its own DSL on top of the relational engine. An **expression** is a tree of operations
describing how to build one or more Series. Expressions are always evaluated inside a **context**:
`select`, `with_columns`, `filter` and `group_by`.

```py {all|8-9|10-11|12-13}
df = pl.DataFrame({
    "integer": [1, 2, 3],
    "date": [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)],
    "float": [4.0, 5.0, 6.0],
    "text": ["a", "b", "c"],
})

query = df.with_columns(                                    # context
    (pl.col("float") * pl.col("integer")).alias("int*float")  # expression
).filter(                                                   # context
    pl.col("date") >= datetime(2024, 1, 2)                    # expression
).select(                                                   # context
    pl.all()                                                  # expression
)
```

---
layout: default
label: 3 · Expressing a query
---

# Polars comes with a big bag of <span class="dm-accent">batteries</span> included

<DmColumns class="mt-4" :gap="16">
<DmColumn header="Column selectors" tone="navy">

```py
from polars import selectors as cs

df.select(cs.contains("a"))
df.select(cs.numeric())
```

Meta-queries over the schema, instead of hard-coded column lists.

</DmColumn>
<DmColumn header="Type namespaces" tone="navy" divider>

```py
df.with_columns(
  pl.col("baz").str.to_uppercase()
)
df.with_columns(
  pl.col("ts").dt.year()
)
```

Type-specific functions live in `.str`, `.dt`, `.list` and `.struct`.

</DmColumn>
<DmColumn header="Testing helpers" tone="violet" divider>

```py
from polars.testing import (
  assert_frame_equal)

assert_frame_equal(df1, df2)
# AssertionError: columns
# ['foo', 'bar', 'baz'] in left
# DataFrame, but not in right
```

Frame and series comparisons that fail with a readable message.

</DmColumn>
</DmColumns>

---
layout: statement
title: Exercise - relational algebra
---

# Exercise time: relational algebra

<p class="mt-6 text-lg opacity-80"><code>3-basic-transforms/</code></p>

---
layout: default
label: 3 · Expressing a query
---

# Windowing and <span class="dm-accent">aggregations</span>

<DmColumns class="mt-4">
<DmColumn header="Window: one row in, one row out" tone="navy">

```py
import polars as pl

df = (
  pl.read_csv("cars.csv")
  .with_columns(
    pl.col("price")
    .min()
    .over("model_type")
    .alias("price_without_options"),
  )
)
```

Calculate a value over a group and add it to every record of that group.

</DmColumn>
<DmColumn header="Aggregation: one group, one row" tone="violet" divider>

```py
import polars as pl

df = (
  pl.read_csv("cars.csv")
  .group_by("model_type")
  .agg(
    pl.col("price")
    .min()
    .alias("price_without_options"),
  )
)
```

Calculate a value over a group and return one record per group.

</DmColumn>
</DmColumns>

---
layout: statement
title: Exercise - windowing and aggregations
---

# Exercise time: windowing and aggregations

<p class="mt-6 text-lg opacity-80"><code>4-window-aggregations/</code></p>

---
layout: default
label: 3 · Expressing a query
---

# The standard <span class="dm-accent">join types</span>

<div class="flex justify-center mt-2">
  <img src="/img/sql-joins.png" alt="SQL join types as Venn diagrams" style="height: 340px" />
</div>

---
layout: default
label: 3 · Expressing a query
---

# Polars supports all <span class="dm-accent">standard</span> join operations

```py
DataFrame.join(
    other: DataFrame,
    on: str | Expr | Sequence[str | Expr] | None = None,
    how: JoinStrategy = 'inner',
    *,
    left_on: str | Expr | Sequence[str | Expr] | None = None,
    right_on: str | Expr | Sequence[str | Expr] | None = None,
    suffix: str = '_right',
    validate: JoinValidation = 'm:m',
    join_nulls: bool = False,
    coalesce: bool | None = None,
) -> DataFrame
```

`validate` is worth remembering: it turns a silent row explosion into an error.

---
layout: default
label: 3 · Expressing a query
---

# ... and even <span class="dm-accent">non-standard</span> joins

```py
DataFrame.join_asof(
    other: DataFrame,
    left_on: str | None | Expr = None,
    right_on: str | None | Expr = None,
    on: str | None | Expr = None,
    by_left: str | Sequence[str] | None = None,
    by_right: str | Sequence[str] | None = None,
    by: str | Sequence[str] | None = None,
    strategy: AsofJoinStrategy = 'backward',
    suffix: str = '_right',
    tolerance: str | int | float | timedelta | None = None,
    allow_parallel: bool = True,
    force_parallel: bool = False,
) -> DataFrame
```

Match on the nearest key rather than an exact one. Useful for time series: sensor readings joined
to the most recent configuration change.

---
layout: statement
title: Exercise - joins
---

# Exercise time: joins

<p class="mt-6 text-lg opacity-80"><code>5-joins/</code></p>

---
layout: section
---

# How the engine <span class="dm-accent">executes</span> it

---
layout: default
label: 4 · How the engine executes it
---

# Lazy vs. <span class="dm-accent">eager</span> evaluation

<DmColumns class="mt-2">
<DmColumn header="Eager: read_csv" tone="navy">

<img src="/img/polar-bear-eager.jpg" alt="A polar bear running" style="height: 175px; width: 100%; object-fit: cover; border-radius: 8px" />

Every step runs the moment you write it. Fine for exploration, wasteful for pipelines.

</DmColumn>
<DmColumn header="Lazy: scan_csv" tone="violet" divider>

<img src="/img/polar-bear-lazy.jpg" alt="A polar bear sleeping" style="height: 175px; width: 100%; object-fit: cover; border-radius: 8px" />

Nothing runs until `.collect()`. The optimiser sees the whole query and rewrites it.

</DmColumn>
</DmColumns>

---
layout: default
label: 4 · How the engine executes it
---

# Some optimisations: <span class="dm-accent">pushdown</span>

<DmColumns class="mt-4">
<DmColumn>

- **Predicate pushdown**: filter rows as early as possible
- **Projection pushdown**: drop columns as early as possible
- **Query pushdown**: push filters, joins and aggregations into the data source

Typically applied while reading the data, so the rows never enter memory at all.

</DmColumn>
<DmColumn divider>

<div class="flex justify-center">
  <img src="/img/parquet-pushdown.png" alt="Predicate and projection pushdown into Parquet row groups" style="height: 300px" />
</div>

</DmColumn>
</DmColumns>

---
layout: default
label: 4 · How the engine executes it
---

# Some optimisations: join <span class="dm-accent">reordering</span>

<div class="flex justify-center mt-2">
  <img src="/img/join-reordering.png" alt="Two join orders, one producing 40 rows and one producing 6 million" style="height: 320px" />
</div>

<p class="text-center mt-2 opacity-80">Same three inputs, same result, 6 million intermediate rows of difference.</p>

---
layout: default
label: 4 · How the engine executes it
---

# Polars streaming: when you are <span class="dm-accent">resource-constrained</span>

Instead of processing the data all at once, Polars can execute the query in batches, which lets you
process datasets larger than memory.

<DmColumns class="mt-4">
<DmColumn>

```py
q1 = (
    pl.scan_csv("car.csv")
    .filter(pl.col("price") < 30_000)
    .group_by("brand")
    .agg(pl.col("max_speed").max())
)
df = q1.collect(streaming=True)
```

</DmColumn>
<DmColumn header="Supported operations" tone="navy" divider>

`filter`, `slice`, `head`, `tail`, `with_columns`, `select`, `group_by`, `join`, `unique`, `sort`,
`explode`, `melt`, `scan_csv`, `scan_parquet`, `scan_ipc`

</DmColumn>
</DmColumns>

---
layout: default
label: 4 · How the engine executes it
---

# A bit <span class="dm-accent">unread</span> is a bit less to process

<div class="flex justify-center mt-2">
  <img src="/img/carrying-boxes.jpg" alt="One person carrying a single box, another carrying a tower of boxes" style="height: 268px; border-radius: 8px" />
</div>

<p class="mt-4">Pushdown is the engine skipping bytes for you. It can only skip what the layout
allows, so partition along the column you filter on first.</p>

<!--
Interactive discussion: suppose you have a large collection of parquet files, but are only
interested in a subset of the data (e.g. year = 2019). How do you query the data efficiently?
-->

---
layout: statement
title: Demo - hive partitioning
---

# Demo: hive-partitioned vs. plain Parquet

---
layout: default
label: 4 · How the engine executes it
---

# When SQL doesn't cut it: user defined <span class="dm-accent">functions</span>

<DmColumns class="mt-4" :gap="16">
<DmColumn header="map_rows" tone="navy">

```py
df.map_rows(
  lambda t: (t[0] * 2, t[1] * 3)
)
```

Every row as a tuple. Column names are lost, and it is the slowest of the three.

</DmColumn>
<DmColumn header="map_batches" tone="navy" divider>

```py
pl.col("features").map_batches(
  lambda s: model.forward(
    s.to_numpy())
)
```

The whole Series at once, so NumPy and PyTorch run once per column.

</DmColumn>
<DmColumn header="map_elements" tone="violet" divider>

```py
pl.col("a").map_elements(
  lambda x: x * 2,
  return_dtype=pl.Int64,
)
```

One value at a time. Pass `return_dtype` or Polars infers it from the first result.

</DmColumn>
</DmColumns>

<p style="margin-top: 32px;">Every UDF drops out of the optimised engine and back into the Python
interpreter, so check for a builtin first.</p>

---
layout: statement
title: Exercise - user defined functions
---

# Exercise time: UDFs

<p class="mt-6 text-lg opacity-80"><code>6-udf/</code></p>

---
layout: section
---

# Big <span class="dm-accent">Data</span>?

---
layout: default
label: 5 · Choosing an engine
---

# The data processing landscape over the <span class="dm-accent">years</span>

<EraTimeline />

<div class="mt-12">

- 📈 First wave optimised for **scale**: commodity machines, open source, structured and
  semi-structured data

<v-clicks>

- 💆 Second wave optimised for **simplicity**: managed platforms hid the cluster
- 💰 Third wave optimised for **cost**: Kubernetes brought the cluster back, cheaper

</v-clicks>

</div>

<!--
The promise of Spark and distributed processing was: scaling out cheaply on commodity machines,
relying on open source so you are not locked in to a vendor, and supporting both structured and
semi-structured data. The downside was that distributed processing was difficult.

The bottleneck then shifted towards maintaining the cluster of machines. Companies struggled with
managing them, which is why the second evolution introduced managed systems that abstract away the
complexity: Snowflake and Databricks. In 2018, Spark answered these private companies by leveraging
Kubernetes.

If we plot these three characteristics as the corners of a triangle...
-->

---
layout: default
label: 5 · Choosing an engine
---

# Emerging single node processing <span class="dm-accent">technologies</span>

<TradeoffTriangle />

<!--
Separation of compute and storage allowed for effective scalability. The main evolution over the
past years was to simplify this complex cluster of machines, which resulted in expensive systems
(Snowflake, Databricks). The alternative was doing everything yourself, which takes time and
requires a strong team.

On the click: not all pipelines need to scale to terabytes. Single machine specs in the cloud have
improved a lot, which created room for Polars and DuckDB. Pandas has been around since 2008.
-->

---
layout: default
label: 5 · Choosing an engine
---

# Interest in big data, and what one machine <span class="dm-accent">now holds</span>

<DmColumns class="mt-4">
<DmColumn header="Interest in 'big data' is past its peak" tone="navy">

<img src="/img/trends-big-data.png" alt="Google Trends for the search term Big Data" style="width: 100%; max-height: 240px; object-fit: contain; border-radius: 6px" />

</DmColumn>
<DmColumn header="One machine now holds 12 TB of RAM" tone="violet" divider>

<img src="/img/aws-large-instances.png" alt="AWS instance types with up to 12288 GiB of memory" style="width: 100%; max-height: 240px; object-fit: contain; object-position: top; border-radius: 6px" />

</DmColumn>
</DmColumns>

---
layout: default
label: 5 · Choosing an engine
---

# You can't please all of the people all the time, luckily there is an <span class="dm-accent">escape hatch</span>

<ArrowHub />

<!--
TODO in the original: rework the arrow image to use other technologies and formats.

Arrow is the columnar memory format that Spark, pandas, Polars and DuckDB all speak, and it reads
from the same files and object stores they do. Handing a DataFrame from one engine to another costs
no serialisation, so the choice of engine can be made per step instead of per project. That is the
escape hatch: you are not locked into the engine you started with.
-->

---
layout: default
label: 5 · Choosing an engine
---

# When do I use <span class="dm-accent">what</span>?

```mermaid {scale: 0.72}
graph TD
  A["Process more than 100 GB?"] -->|Yes| B["Simple to manage?"]
  A -->|No| C["Who maintains your pipelines?"]
  B -->|"Yes ($$$)"| D["Snowflake / Databricks"]
  B -->|"No ($)"| E["Spark on Kubernetes"]
  C -->|"Data scientist"| F["pandas"]
  C -->|"Data analyst"| G["DuckDB"]
  C -->|"Data engineer"| H["Polars"]
```

---
layout: section
---

# Apache <span class="dm-accent">Spark</span>

---
layout: default
label: 6 · PySpark
---

# The same query in <span class="dm-accent">PySpark and Polars</span>

<DmColumns class="mt-4">
<DmColumn header="PySpark" tone="navy">

```py
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as sf

spark = SparkSession.builder.getOrCreate()

df = (
  spark.read.csv("measurements.csv")
  .withColumn("year", sf.year("timestamp"))
  .withColumn("max_weight_per_year",
              sf.max("weight")
              .over(Window.partitionBy("year"))
              )
)

df.collect()
```

</DmColumn>
<DmColumn header="Polars" tone="violet" divider>

```py
import polars as pl

df = (
  pl.scan_csv("measurements.csv")
  .with_columns(
    pl.col("timestamp").dt.year()
    .alias("year")
  )
  .with_columns(
    pl.col("weight").max().over("year")
    .alias("max_weight_per_year")
  )
)

df.collect()
```

</DmColumn>
</DmColumns>

<p class="mt-4">Both express the same operations, and both are lazy. The rest of this section covers
what changes when the work runs on a cluster instead of in one process.</p>

---
layout: default
label: 6 · PySpark
---

# Large jobs are limited by <span class="dm-accent">I/O</span>, and a cluster adds bandwidth

<DmColumns class="mt-4">
<DmColumn>

<DmColumn header="One machine" tone="navy">

- One network card, one set of disks: a few GB/s at best
- 10 TB at 1 GB/s: three hours before any computation starts
- The CPUs idle, waiting for bytes

</DmColumn>

<DmColumn header="A cluster" tone="violet" class="mt-5">

- Every executor reads its own slice, so bandwidth grows with the machine count
- 10 TB across 60 executors: minutes, if the object store keeps up
- Memory scales the same way

</DmColumn>

</DmColumn>
<DmColumn divider>

<div class="flex justify-center">
  <img src="/img/io-bottleneck.jpg" alt="A giant locomotive with a single entrance and a long queue of passengers, next to a modern train whose cars all have their own doors" style="width: 100%; object-fit: contain" />
</div>

</DmColumn>
</DmColumns>

<!--
Easy to miss: distributing is not mainly about CPU, it is about I/O. A single machine is capped by
its network card and its disks, and on a large scan the processors are idle most of the time,
waiting for bytes. The Goliath on the left is that machine: an impressive engine with one entrance,
and everyone queues at it. Making the locomotive bigger does not shorten the queue.

Add machines and the aggregate read bandwidth grows with them, which is why a cluster finishes a
10 TB scan in minutes rather than hours. That is the city line on the right: three cars, every car
with its own door, passengers boarding in parallel. The numbers are round arithmetic, not a
benchmark: 1 GB/s per machine, 10 TB, 60 executors.

The doors only help if the platform can feed them, which is the object store caveat, and the same
reason a badly partitioned dataset leaves executors idle.

It also explains why the first half mattered: columnar formats and partitioning shrink the bytes you
read in the first place, and that helps on one machine and on sixty.
-->

---
layout: default
label: 6 · PySpark
---

# A submitted job runs on a <span class="dm-accent">driver and its executors</span>

Scaling out means adding machines rather than buying a bigger one. This is the machinery that makes
that possible.

<DmColumns class="mt-3">
<DmColumn>

<img src="/img/spark-cluster.png" alt="Driver program, cluster manager and worker nodes" style="width: 100%" />

Your program runs in the driver. The cluster manager allocates executors on worker nodes, and the
driver ships the code and the tasks to them.

</DmColumn>
<DmColumn divider>

```bash
$ ./bin/spark-submit \
    --master k8s://https://<host>:<port> \
    --deploy-mode cluster \
    --name spark-pi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=<image> \
    local:///path/to/examples.jar
```

`spark-submit` sets `SPARK_HOME` and `JAVA_HOME` and hands your program to the launcher.

Note the arrow between the workers: executors talk to each other, not only to the driver. The next
slide is about that arrow.

</DmColumn>
</DmColumns>

<!--
1. To start a Spark application, you submit it. spark-submit comes bundled with the Spark binary and
   is a short script that sets environment variables, looks for a Java installation and passes
   options to the launcher, written in Java.
2. Your program starts a SparkContext, in the driver process. It connects to a cluster manager and
   asks for computing resources.
3. The cluster manager allocates them to executor processes on the worker nodes.
4. Spark sends the application code and its dependencies to the executors, then sends tasks.

The cluster manager keeps checking the workers are alive and the driver listens for new worker
announcements, which is where resiliency comes from.
-->

---
layout: default
label: 6 · PySpark
---

# Wide transformations <span class="dm-accent">shuffle</span> data across the network

<DmColumns class="mt-3">
<DmColumn header="Narrow: no data moves" tone="navy">

`select`, `filter`, `withColumn`, `union`

Each executor works on the partitions it already holds. Spark chains these into one stage.

</DmColumn>
<DmColumn header="Wide: rows meet on one executor" tone="violet" divider>

`groupBy`, `join`, `distinct`, `sort`, `repartition`

All rows with the same key have to end up in the same place, so Spark writes shuffle files and moves
them over the network. That ends a stage and starts the next.

</DmColumn>
</DmColumns>

```py
df.filter(sf.col("age") > 18).groupBy("country").count().explain()
# AdaptiveSparkPlan isFinalPlan=false                        (abridged)
# +- HashAggregate(keys=[country], functions=[count(1)])
#    +- Exchange hashpartitioning(country, 200)     <- the shuffle
#       +- HashAggregate(keys=[country], [partial_count(1)])
#          +- Filter (age > 18)
```

<p class="mt-2">No Polars equivalent: in one process a <code>group_by</code> is a hash table, not a
network transfer.</p>

---
layout: default
label: 6 · PySpark
---

# <span class="dm-accent">Partition count</span> decides how much of the cluster stays busy

<DmColumns class="mt-2" :gap="16">
<DmColumn header="72 vCPUs, idle at the tail" tone="navy">

<img src="/img/spark-stages-idle.png" alt="Spark stage timeline with idling CPUs near the end" style="width: 100%; max-height: 104px; object-fit: cover; object-position: top" />
<img src="/img/ganglia-idle.jpg" alt="Cluster load dropping to 25 percent" style="width: 100%; max-height: 118px; object-fit: contain; margin-top: 8px" />

</DmColumn>
<DmColumn header="Partitions matched to cores" tone="violet" divider>

<img src="/img/spark-stages-tuned.png" alt="Spark stage timeline with more, smaller partitions" style="width: 100%; max-height: 104px; object-fit: cover; object-position: top" />
<img src="/img/ganglia-tuned.jpg" alt="Shorter job with almost no idling" style="width: 100%; max-height: 118px; object-fit: contain; margin-top: 8px" />

</DmColumn>
</DmColumns>

<p class="mt-3">The 200 in that <code>Exchange</code> is the default of
<code>spark.sql.shuffle.partitions</code>, applied to every shuffle whatever your data or cluster
size. Make it a multiple of the cluster cores. Since Spark 3.2 adaptive execution coalesces them at
runtime, so treat 200 as a starting point.</p>

<!--
A cluster of 72 CPUs over 9 nodes. On the partition distribution (top left) the workers process
partitions in parallel, but near the end some CPUs start idling: the load drops to about 25% for
roughly 5 minutes. Wasting 75% of a 72 vCPU cluster for 5 minutes is costly.

The fix is to make the partition count a multiple of the vCPU count, which is what was done on the
right. The blocks are smaller because there are more partitions, the total work is the same. Memory
usage was only 50%, so memory could be halved and the CPU count doubled for the same price.
-->

---
layout: default
label: 6 · PySpark
---

# Transformations are <span class="dm-accent">lazy</span>, actions trigger execution

<DmColumns class="mt-4">
<DmColumn>

```py
import pyspark.sql.functions as sf

df1 = spark.range(3)
df2 = df1.withColumn("foo", sf.lit("bar"))
df3 = df2.withColumn("bar", sf.col("id") < 2)
df4 = df3.filter(sf.col("id") != 1)
df5 = df4.select("foo", "bar", "id",
                 (sf.col("id") + 2).alias("plus2"))
df6 = df5.drop("id")
df7 = df6.withColumnRenamed("bar", "lessthan2")

df7.printSchema()   # free: bookkeeping only
print(df7.count())  # action: the plan runs
df7.show()          # action
```

</DmColumn>
<DmColumn divider>

Polars taught you this with `scan_csv` and `collect`. Spark works the same way: transformations
build a plan, actions run it.

Two things are different once the plan runs on a cluster:

- ⚠️ Errors surface at the **action**, not at the line that caused them, and they arrive as a Java
  stack trace from an executor.
- `DataFrame.explain()` shows the physical plan, including every `Exchange`.

</DmColumn>
</DmColumns>

---
layout: default
label: 6 · PySpark
---

# Chaining drops the intermediate names, <span class="dm-accent">transform</span> makes steps testable

<DmColumns class="mt-3" :gap="16">
<DmColumn header="Chain the calls" tone="navy">

```py
df = (
    spark.range(3)
    .withColumn("foo", sf.lit("bar"))
    .withColumn("bar", sf.col("id") < 2)
    .filter(sf.col("id") != 1)
    .select("foo", "bar", "id",
            (sf.col("id") + 2).alias("plus2"))
    .drop("id")
    .withColumnRenamed("bar", "lessthan2")
)
```

No `df1` to `df7` to keep straight, and no filtering `df3` when you meant `df4`.

</DmColumn>
<DmColumn header="Name the steps with transform" tone="violet" divider>

```py
def add_flags(df: DataFrame) -> DataFrame:
    return (df
        .withColumn("foo", sf.lit("bar"))
        .withColumn("bar", sf.col("id") < 2))

def drop_middle(df: DataFrame) -> DataFrame:
    return df.filter(sf.col("id") != 1)

df = (spark.range(3)
      .transform(add_flags)
      .transform(drop_middle))
```

A `DataFrame -> DataFrame` function is testable on three rows, no cluster involved.
`transform` is PySpark's pipe; Polars spells it `.pipe()`.

</DmColumn>
</DmColumns>

<!--
The reassignment style on the previous slide is what most PySpark code in the wild looks like. It
reads top to bottom, but every intermediate name is a chance to reference the wrong one, and none of
the steps can be tested on its own.

Chaining fixes the naming. transform fixes the testing: the moment a step is a named function taking
a DataFrame and returning a DataFrame, it can be unit tested with a handful of rows, and the same
function works in a pipeline of any size.
-->

---
layout: default
label: 6 · PySpark
---

# A DataFrame used twice is computed twice, unless you <span class="dm-accent">cache</span> it

<DmColumns class="mt-2" :gap="16">
<DmColumn header="Two actions, two full recomputations" tone="navy">

```mermaid {scale: 0.42}
graph TD
  A["scan, filter, join"] --> D["count"]
  A2["scan, filter, join"] --> E["write parquet"]
```

</DmColumn>
<DmColumn header="Cached: computed once, read twice" tone="violet" divider>

```mermaid {scale: 0.42}
graph TD
  A["scan, filter, join"] --> M[("cached rows")]
  M --> D["count"]
  M --> E["write parquet"]
```

</DmColumn>
</DmColumns>

```py
enriched = (spark.read.parquet("events")
            .filter(sf.col("year") == 2024)
            .join(dim_user, "user_id")
            .cache())          # lazy too: the first action fills it
enriched.count()               # computes, then keeps the rows
enriched.write.parquet("out")  # reads the cache instead
```

<p class="mt-3">Only worth it when one DataFrame feeds more than one action. Call
<code>unpersist()</code> when the branch is done.</p>

<!--
A Spark plan is lineage, not a result. Every action walks the plan back to the source, so a
DataFrame used by two actions is computed twice, all the way from the files.

cache() marks it to be kept after the first action computes it. persist() is the same thing with a
storage level you choose. Neither computes anything on its own.

The default storage level for a DataFrame is MEMORY_AND_DISK, so a cached frame that does not fit
in memory spills, and you pay for both the memory pressure and the disk read.

Ask the room: where would you put a cache in a pipeline that writes three reports from one joined
dataset? And what happens if the cached frame is bigger than the executor memory?
-->

---
layout: default
label: 6 · PySpark
---

# A UDF runs Python per row, <span class="dm-accent">outside</span> Spark's optimiser

<DmColumns class="mt-4">
<DmColumn>

```py
import pyspark.sql.functions as sf
from pyspark.sql.types import IntegerType

def square(x):
    return x**2

square_as_udf = sf.udf(
    square, returnType=IntegerType())
df.withColumn("squared", square_as_udf("id"))
```

You must declare the return type: the optimiser cannot infer it from Python.

</DmColumn>
<DmColumn divider>

In Polars a UDF drops from Rust into Python in the same process. In Spark, every row is serialised
out of the JVM into a separate Python worker and back again.

That round trip is why `pandas_udf` exists: it hands the worker an Arrow batch instead of a row, so
the crossing happens once per batch.

The rule from the Polars half still holds, only more so: look for a builtin first.

</DmColumn>
</DmColumns>

<!--
Higher order functions are a feature people know from functional programming. udf takes a function
and returns a new function.
-->

---
layout: default
label: 6 · PySpark
---

# One core, four libraries: <span class="dm-accent">SQL, streaming, MLlib, GraphX</span>

<div class="flex justify-center mt-2 mb-4">
  <img src="/img/logo-spark.png" alt="Apache Spark" style="height: 54px" />
</div>

<DmProcess class="mt-4">
<DmPhase label="SQL" />
<DmPhase label="Streaming" />
<DmPhase label="MLlib" />
<DmPhase label="GraphX" />
</DmProcess>

<p style="margin-top: 28px;">All four sit on the Spark core, whose abstraction is the resilient
distributed dataset (RDD). The core also handles task dispatch, scheduling and I/O.</p>

<p class="mt-2">They share one API and one deployment, in Scala, Java, Python, R and SQL with almost
identical names. Training a model on a batch and then scoring a stream needs no second system.</p>

<!--
Spark offers SQL-like queries against massive datasets. Streaming processes data as it arrives, like
sensor readings from an IoT device. MLlib covers machine learning. GraphX handles graph-like data
where relations matter.

Even though Spark is written in Scala, it has bindings in 5 officially supported languages. Whatever
you learn in one language is named identically in the others, R excepted.
-->

---
layout: default
label: 6 · PySpark
---

# Batch and streaming share the <span class="dm-accent">same transformations</span>

<DmColumns class="mt-4">
<DmColumn header="Batch: aggregate a database table" tone="navy">

```py
df = (spark
  .read
  .format("jdbc")
  .option("url", url)
  .option("dbtable", "people")
  .load()
  )

counts_by_age = df.groupBy("age").count()
```

</DmColumn>
<DmColumn header="Streaming: count words as they arrive" tone="violet" divider>

```py
lines = (spark
  .readStream
  .format("socket")
  .option("host", host)
  .option("port", port)
  .load()
  )

words = lines.select(
    explode(split(lines.value, " ")).alias("word"))
word_counts = words.groupBy("word").count()

query = (word_counts.writeStream
         .format("console").start())
```

</DmColumn>
</DmColumns>

<p class="mt-4">Swap <code>read</code> for <code>readStream</code> and the business logic is
identical: <code>select</code>, <code>groupBy</code>, <code>count</code>.</p>

<!--
There are not many databases that can do streaming like this. Note the similarities: select,
groupBy, count. The transformations are identical between the batch and the streaming case.
-->

---
layout: default
label: 6 · PySpark
---

# SQL and the DataFrame API compile to the <span class="dm-accent">same plan</span>

Both go through the same optimiser and run on the same executors. Neither is faster, and neither is
"more distributed" than the other, so the choice is about maintaining the code.

<DmColumns class="mt-4">
<DmColumn header="Write it in SQL" tone="navy">

```py
with open("min_max_by_user.sql") as fh:
    query = fh.read()
spark.sql(query)
```

- Everyone on the team reads it
- Says what, not how
- No second API to learn

</DmColumn>
<DmColumn header="Write it in Python" tone="violet" divider>

- Functions and modules instead of copy and paste
- Branches and loops
- Unit tests on the transformation
- Type checking and linting before you deploy
- Machine learning in the same program

</DmColumn>
</DmColumns>

<p class="mt-3">Spark distributes the work either way, so scale is not the tiebreaker.</p>

<!--
The same argument as "To SQL or not to SQL?" in the first half, with one difference: there the
choice was also about what the engine could do, here both paths run on the same engine.

dbt counters some of these shortcomings with macros, but there is a richness to a general purpose
language, like specialised types, that a SQL layer does not have.
-->

---
layout: section
---

# Running it in <span class="dm-accent">practice</span>

---
layout: default
label: 6 · PySpark
---

# Polars ships as a <span class="dm-accent">wheel</span>; PySpark needs a <span class="dm-accent">JVM</span>

<DmColumns class="mt-4">
<DmColumn header="Polars" tone="navy">

```bash
uv add polars
```

- One wheel with a Rust binary inside
- No runtime to install, no services to start
- The same code runs in a notebook, a Lambda and a CI job

</DmColumn>
<DmColumn header="PySpark" tone="violet" divider>

```bash
uv add pyspark               # ~300 MB
apt install openjdk-17-jre   # + JAVA_HOME
```

```py
spark = (SparkSession.builder
    .master("local[*]")          # one machine
    .config("spark.sql.shuffle.partitions", 200)
    .getOrCreate())
```

- `local[*]` for your laptop, a cluster manager for anything else
- Settings live in `conf/spark-defaults.conf`, this repo ships one

</DmColumn>
</DmColumns>

<p class="mt-3">The cost of the second engine is the runtime around it: a JVM of the right version,
a cluster manager, and configuration.</p>

<!--
The JDK version really does matter: on this repo's own venv, Java 23 with PySpark 4.1 fails with
"UnsupportedOperationException: getSubject is supported only if a security manager is allowed".
Spark 4 wants Java 17 or 21.

Some platforms (Databricks, spark-shell, pyspark) create the SparkSession for you, which is
convenient but hides this. The number of config options is large because Spark integrates with YARN,
Mesos and Kubernetes and manages a JVM on every worker. The defaults are usually well chosen.

local[*] runs Spark locally with as many worker threads as logical cores on your machine.
-->

---
layout: default
label: 6 · PySpark
---

# Connectors need matching <span class="dm-accent">JARs</span> and configuration

<DmColumns class="mt-4" :gap="16">
<DmColumn header="AWS S3 outside EMR" tone="navy">

```py
config = {
    "spark.jars.packages":
        "org.apache.hadoop:hadoop-aws:<version>",
    "spark.hadoop.fs.s3a.aws.credentials.provider":
        "org.apache.hadoop.fs.s3a"
        ".SimpleAWSCredentialsProvider",
}
conf = SparkConf().setAll(config.items())
spark = SparkSession.builder.config(
    conf=conf).getOrCreate()

df = spark.read.csv(f"s3a://{BUCKET}/{KEY}",
                    header=True)
```

</DmColumn>
<DmColumn header="Snowflake" tone="violet" divider>

```py
snowflake_pkgs = [
    "net.snowflake:snowflake-jdbc:<version>",
    "net.snowflake:spark-snowflake_2.12:<version>",
]
config = {
    "spark.jars.packages": ",".join(snowflake_pkgs),
}
conf = SparkConf().setAll(config.items())
spark = SparkSession.builder.config(
    conf=conf).getOrCreate()
```

</DmColumn>
</DmColumns>

<p class="mt-4">Versions have to line up: hadoop-aws against the Hadoop libraries in your Spark
install, spark-snowflake against your Spark version. Then come the authentication options. Polars
reads <code>s3://</code> with <code>pip install polars[aws]</code>.</p>

---
layout: default
label: 6 · PySpark
---

# Readers and writers handle formats, folders and <span class="dm-accent">partitioning</span>

<DmColumns class="mt-4">
<DmColumn>

```py
frame = spark.read.csv(
    str(csv_file_path), sep=";", header=True)

frame = (
    spark.read
    .options(header="true", sep=";", inferSchema=True)
    .format("csv")
    .load(str(csv_file_path))
)

frame.write.parquet(
    "some_location",
    mode="overwrite",
    partitionBy="country",
)
```

</DmColumn>
<DmColumn header="Hive-partitioned output" tone="navy" divider>

```text
├── date=2021-10-08
│   ├── train_id=200
│   │   ├── part-00000-6d…
│   │   └── part-00001-6d…
│   ├── train_id=231
│   │   ├── part-00000-6d…
│   │   └── part-00001-6d…
│   └── train_id=4361
│       ├── part-00000-6d…
│       └── part-00001-6d…
├── date=2021-10-09
│   ├── train_id=200
```

One file per partition per writer, in folders named after the column value. The same layout Polars
read from earlier: partition on what you filter on first.

</DmColumn>
</DmColumns>

<!--
The first method is pythonic: the file type is known in advance. The second is general purpose, with
options() and load(). Writing works the same way.

You can read a folder of nested files by supplying the top-level path, as long as they share a
schema: no CSVs and JSONs together.

Best practice: partition on the full date, not on year, month and day separately, which makes
filtering harder afterwards.
-->

---
layout: default
label: 6 · PySpark
---

# When to reach for <span class="dm-accent">Spark</span>

<DmColumns class="mt-6">
<DmColumn header="Spark earns its keep" tone="navy">

- The data does not fit one machine, and streaming it through does not help
- You already run a platform that hosts it: Databricks, EMR, Kubernetes
- You need batch, streaming and ML behind one API
- A job runs long enough that losing a node matters

</DmColumn>
<DmColumn header="Stay on one node" tone="violet" divider>

- It fits in memory, or streams through a single machine
- You want a fast local loop and a short install
- The team is small and the pipeline is simple
- Cost per query matters more than peak scale

</DmColumn>
</DmColumns>

<p class="mt-6">A cluster costs a JVM, configuration, shuffles and idle CPUs, whether or not the
data needs the scale. The decision tree from the first half still applies.</p>

---
layout: default
label: Recap
---

# What we <span class="dm-accent">covered</span>

<div class="dm-recap mt-6">

1. **Same data, different storage.** Operational and analytical systems hold the same facts. Storing
   them row by row or column by column is what decides which questions are cheap to ask.
2. **Let the engine do the heavy lifting.**
   - It turns what you asked for into a plan, then reorders joins and pushes filters and column
     selections down into the scan, so it reads less.
   - You help it by storing data columnar and partitioning along the questions you actually ask.
     It can only skip what the layout allows.
3. **Relational algebra has lasted.** Project, filter, join, aggregate, window. SQL and the DataFrame
   API are two ways of writing the same operations.
4. **One node goes a long way.** For most pipelines a single machine is simpler, cheaper and quicker
   to iterate on. Reach for Spark when the data is genuinely large.

</div>

---
layout: thanks
title: Thank you
---

# Thank you
