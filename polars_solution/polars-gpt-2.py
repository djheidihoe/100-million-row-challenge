import polars as pl

FILENAME = "../data/data.csv"

result = (
    pl.scan_csv(
        FILENAME,
        has_header=False,
        new_columns=["url", "timestamp"],
    )

    .select(
        path=pl.col("url").str.split("/").list.slice(3).list.join("/").radd("/"),
        date=pl.col("timestamp").str.slice(0,10),
    )

    .group_by(["path", "date"])
    .len()
    .collect(streaming=True)
)


print(result)

