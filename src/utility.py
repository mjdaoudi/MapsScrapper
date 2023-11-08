import pandas as pd

df = pd.read_csv("leads_complete.csv")

df.drop_duplicates(
    subset=["name", "Business Type", "email"], keep="first", inplace=True
)

df.to_csv("leads_complete_no.csv", index=False)
