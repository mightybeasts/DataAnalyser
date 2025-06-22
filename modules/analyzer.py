def get_summary(df):
    return {
        "Total Sales": df["Sales"].sum(),
        "Average Sale": df["Sales"].mean(),
        "Max Sale": df["Sales"].max(),
        "Min Sale": df["Sales"].min(),
        "Top Region": df.groupby("Region")["Sales"].sum().idxmax(),
        "Top Product": df.groupby("Product")["Sales"].sum().idxmax()
    }
