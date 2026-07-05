import polars as pl

FILENAME = "../data/data.csv"

result = pl.read_csv(FILENAME)

print(result)

