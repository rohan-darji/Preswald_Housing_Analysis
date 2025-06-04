import pandas as pd
import plotly.express as px
from preswald import connect, get_df, table, text, query, plotly, slider

connect()
df = get_df("housing_csv")
# Convert all numerical columns to integers
for col in ["price", "area", "bedrooms", "bathrooms", "stories", "parking"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").astype('Int64')

text("""
# Housing Data Explorer 🏠\n
Welcome to the interactive housing data dashboard!\n
This app allows you to explore a dataset of houses, including their prices, areas, features, and more.\n
- **Full Dataset:** View all available housing data.\n- **No Basement Filter:** See only houses without a basement.\n- **Visualizations:** Explore price vs. area, price distributions, and more.\n\nUse the charts and tables below to gain insights into the housing market!
""")

text("## Full Housing Dataset\nBelow is the complete dataset loaded from the CSV file. Each row represents a house with its features and price.")
# Add a slider for number of rows to display in the main table
rows = slider("Rows to Display", min_val=5, max_val=50, default=10)
table(df, title="All Rows from housing_csv (limited)", limit=rows)


sql = """
    SELECT *
    FROM housing_csv
    WHERE basement = 'no'
"""
filtered_df = query(sql, "housing_csv")

text("## Houses with No Basement\nThis table shows only the houses that do not have a basement.")
table(filtered_df, title="Houses with no basement")

fig1 = px.scatter(
    df,
    x="area",
    y="price",
    title="Price vs. Area (All Houses)",
    labels={"area": "Area (sq ft)", "price": "Price (USD)"}
)
text("### Scatter Plot: Price vs. Area (All Houses)\nThis chart shows the relationship between the area of a house and its price for all houses in the dataset.")
fig1.update_layout(template="plotly_white")
plotly(fig1)

fig2 = px.box(
    filtered_df,
    x="area",
    y="price",
    title="Price Distribution of Houses with No Basement",
    labels={"area": "Area (sq ft)", "price": "Price (USD)"}
)
text("### Box Plot: Price Distribution of Houses with No Basement\nThis box plot visualizes the distribution of house prices for different areas, but only for houses without a basement.")
fig2.update_layout(template="plotly_white")
plotly(fig2)

fig3 = px.histogram(
    df,
    x="price",
    title="Price Distribution of All Houses",
    labels={"price": "Price (USD)"},
    nbins=30
)
text("### Histogram: Price Distribution of All Houses\nThis histogram shows how house prices are distributed across all houses in the dataset.")
fig3.update_layout(template="plotly_white")
plotly(fig3)

text("## Interactive: Number of Houses in Selected Price Range\nUse the slider below to select a price range. The histogram will show the number of houses within that range.")

min_price = int(df["price"].min())
max_price = int(df["price"].max())

price_range = slider(
    label="Select maximum price (USD)",
    min_val=min_price,
    max_val=max_price,
    default=max_price,
    step=50000
)

houses_in_range = df[df["price"] <= price_range]

fig_range = px.histogram(
    houses_in_range,
    x="price",
    title=f"Number of Houses with Price ≤ {price_range:,} USD",
    labels={"price": "Price (USD)"},
    nbins=30
)
fig_range.update_layout(template="plotly_white")
plotly(fig_range)