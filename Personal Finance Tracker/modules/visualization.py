import seaborn as sns  # import seaborn for plotting
import matplotlib.pyplot as plt  # import matplotlib for plotting
import pandas as pd  # import pandas for data handling
from modules.database import get_transactions  # import get_transactions from the database module

# convert the transaction tuples to a dataframe
def get_transaction_df():
    data = get_transactions()  # get all transactions from the database
    df = pd.DataFrame(data, columns=["ID", "Category", "Amount", "Date", "Description"])  # create dataframe with specific columns
    df["Date"] = pd.to_datetime(df["Date"])  # make sure 'Date' column is in datetime format
    return df  # return the dataframe

# plot total spending by category
def plot_spending_by_category():
    df = get_transaction_df()  # get the dataframe
    grouped = df.groupby('Category')['Amount'].sum().reset_index()  # group data by category and sum the spending

    sns.set(style='whitegrid')  # set the background style for the plot
    plt.figure(figsize=(8, 5))  # set the figure size
    sns.barplot(data=grouped, x='Amount', y='Category', palette='Blues_r')  # create a bar plot of spending by category
    plt.title("Total Spending by Category")  # add a title to the plot
    plt.xlabel("Amount")  # add a label to the x-axis
    plt.ylabel("Category")  # add a label to the y-axis
    plt.tight_layout()  # make the layout tight to prevent cut-off
    plt.show()  # show the plot

# plot monthly spending trend with a line chart
def plot_monthly_spending_trend():
    df = get_transaction_df()  # get the dataframe
    df['Month'] = df['Date'].dt.to_period('M').astype(str)  # create a 'Month' column based on the Date column
    monthly = df.groupby('Month')['Amount'].sum().reset_index()  # group data by month and sum the spending

    sns.set(style='darkgrid')  # set the background style for the plot
    plt.figure(figsize=(8, 5))  # set the figure size
    sns.lineplot(data=monthly, x='Month', y='Amount', marker='o', color='purple')  # create a line plot for monthly spending
    plt.title("Monthly Spending Trend")  # add a title to the plot
    plt.xticks(rotation=45)  # rotate the x-axis labels for better readability
    plt.tight_layout()  # make the layout tight to prevent cut-off
    plt.show()  # show the plot
