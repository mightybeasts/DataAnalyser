import plotly.express as px
import plotly.graph_objects as go



def region_chart(df):
    region = df.groupby("Region")["Sales"].sum().reset_index()
    return px.bar(region, x="Region", y="Sales", title="Sales by Region")

def product_chart(df):
    product = df.groupby("Product")["Sales"].sum().reset_index()
    return px.pie(product, names="Product", values="Sales", title="Sales Distribution")
def sales_trend(df):
    df = df.sort_values("Date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Sales"],
        mode="lines+markers",
        line=dict(shape='spline', color="royalblue"),
        fill="tozeroy",
        name="Sales Trend"
    ))
    fig.update_layout(
        title="📈 Sales Trend",
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig