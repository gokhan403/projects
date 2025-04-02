import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("data/CSV/combined_data.csv")

print(df)
print("\n")
print(df.head(10))
print("\n")
print(df.tail(10))
print("\n")
print(df.dtypes)
print("\n")
print(df.shape)
print("\n")
print(df.info())
print("\n")
print(df.describe())

#pd.set_option("display.max.rows", 275528)
#pd.set_option("display.max.columns", 21)
#print(df)

#pd.set_option("display.max.rows", 1000)
print(df.filter(["totalSourceBytes", "Label"]))
print("\n")
print(df.isnull().sum())
print("\n")
print(df.value_counts("Label"))
print("\n")
attacks = df[df["Label"] == "Attack"]
pd.set_option("display.max.rows", 100)
print(attacks.drop_duplicates(subset="appName"))
print("\n")
