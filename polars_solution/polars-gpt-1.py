import polars as pl

FILENAME = "../data/data.csv"

result = (
    pl.scan_csv(
        FILENAME,
        has_header=False,
        new_columns=["url", "timestamp"],
    )

    .with_columns(
        # keep only the path
        pl.col("url").str.extract(r"https?://[ˆ/]+(.*)",1).alias("path"),

        # YYYY-DD-MM
        pl.col("timestamp").str.slice(0,10).alias("date"),
    )

    .group_by(["path", "date"])
    .len()
    .collect(streaming=True)
)


print(result)

