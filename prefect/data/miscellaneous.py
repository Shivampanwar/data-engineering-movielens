import pandas as pd
df = pd.read_parquet('/home/shivam/data-engineering-movielens/prefect/data/movies_data.parquet')

df = pd.read_csv('/home/shivam/data-engineering-movielens/prefect/data/results-20230415-224601 - results-20230415-224601.csv')

print (df.shape)
print (df.head(1))
print (df.dtypes)