
import pandas as pd
from modules import database

#Load the transactions into the dataframe
def get_transaction_df():
    data = database.get_transactions()
    df = pd.DataFrame(data,columns=["ID","Category","Amount","Date","Description"])

    # changing the structure of the datetime existed
    df["Date"] = pd.to_datetime(df["Date"])
    return df

#Analyse the total spending on the basic of category

def spending_by_category():
    df = get_transaction_df()
    return df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

def monthly_spending_trend():
    df = get_transaction_df()
    df["Month"] = df["Date"].dt.to_period("M")
    return df.groupby("Month")["Amount"].sum()