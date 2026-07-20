import polars as pl
import json

FILENAME = "../data/data.csv"

lf = (
    pl.scan_csv(
        FILENAME,
        has_header=False,
        new_columns=["url", "ts"],
        schema_overrides={"url": pl.String, "ts": pl.String},
    )
    .with_columns(
        (
            "/" + pl.col("url")
                .str.splitn("://", 2).struct.field("field_1")
                .str.splitn("/", 2).struct.field("field_1")
        ).alias("path"),
        pl.col("ts").str.slice(0, 10).alias("date"),
    )
    .group_by(["path", "date"])
    .agg(pl.len().alias("count"))
    # .sort(["path", "date"])  # cheap now — runs on the aggregated result, not 100M rows
)

df = lf.collect()

result = {}
for path, date, count in df.iter_rows():
    result.setdefault(path, {})[date] = count

print(json.dumps(result, indent=4))

# result_df, timings = lf.profile()
# print(timings)

