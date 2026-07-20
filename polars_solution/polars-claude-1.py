import polars as pl
import json

FILENAME = "../data/data.csv"

lf = (
    pl.scan_csv(
        FILENAME,
        has_header=False,
        new_columns=["url","ts"],
    )

    .with_columns(
        pl.col("url").str.extract(r"^https?://[^/]+(/.*)$",1).alias("path"),
        pl.col("ts").str.slice(0,10).alias("date"),
    )
    .group_by(["path", "date"])
    .agg(pl.len().alias("count"))
)

# df = lf.collect(engine="streaming")
#
# result: dict[str, dict[str, int]] = {}
#
# for path, date, count in df.iter_rows():
#     result.setdefault(path, {})[date] = count
#
# print(json.dumps(result, indent=4))

result_df, timings = lf.profile()
print(timings)
