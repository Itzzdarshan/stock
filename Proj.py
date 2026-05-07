# IBM Stock Data Assignment – Complete Code (Questions 1–6)

```python
# ============================================================
# IBM Data Science Assignment
# Analyzing Historical Stock/Revenue Data and Building Dashboard
# ============================================================

# ------------------------------------------------------------
# Import Required Libraries
# ------------------------------------------------------------

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# Question 1: Use yfinance to Extract Tesla Stock Data
# ============================================================

# Extract Tesla stock data

tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period="max")

# Reset index

tesla_data.reset_index(inplace=True)

# Display first five rows

print("Tesla Stock Data:")
print(tesla_data.head())


# ============================================================
# Question 2: Use Webscraping to Extract Tesla Revenue Data
# ============================================================

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

html_data = requests.get(url).text

soup = BeautifulSoup(html_data, "html.parser")

# Create empty dataframe

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Extract table data

for table in soup.find_all("table"):
    if "Tesla Quarterly Revenue" in str(table):

        for row in table.find_all("tr")[1:]:
            col = row.find_all("td")

            if len(col) == 2:
                date = col[0].text
                revenue = col[1].text

                tesla_revenue = pd.concat([
                    tesla_revenue,
                    pd.DataFrame({"Date": [date], "Revenue": [revenue]})
                ], ignore_index=True)

# Clean revenue column

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r'\\$,', '', regex=True)

# Remove empty values

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Display last five rows

print("\nTesla Revenue Data:")
print(tesla_revenue.tail())


# ============================================================
# Question 3: Use yfinance to Extract GameStop Stock Data
# ============================================================

# Extract GameStop stock data

gme = yf.Ticker("GME")

gme_data = gme.history(period="max")

# Reset index

gme_data.reset_index(inplace=True)

# Display first five rows

print("\nGameStop Stock Data:")
print(gme_data.head())


# ============================================================
# Question 4: Use Webscraping to Extract GameStop Revenue Data
# ============================================================

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/gamestop_revenue.htm"

html_data = requests.get(url).text

soup = BeautifulSoup(html_data, "html.parser")

# Create empty dataframe

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Extract table data

for table in soup.find_all("table"):
    if "GameStop Quarterly Revenue" in str(table):

        for row in table.find_all("tr")[1:]:
            col = row.find_all("td")

            if len(col) == 2:
                date = col[0].text
                revenue = col[1].text

                gme_revenue = pd.concat([
                    gme_revenue,
                    pd.DataFrame({"Date": [date], "Revenue": [revenue]})
                ], ignore_index=True)

# Clean revenue column

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(r'\\$,', '', regex=True)

# Remove empty values

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Display last five rows

print("\nGameStop Revenue Data:")
print(gme_revenue.tail())


# ============================================================
# Function to Plot Graphs
# ============================================================


def make_graph(stock_data, revenue_data, stock):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data_specific.Date),
            y=stock_data_specific.Close.astype("float"),
            name="Share Price"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data_specific.Date),
            y=revenue_data_specific.Revenue.astype("float"),
            name="Revenue"
        ),
        row=2,
        col=1
    )

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)

    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    fig.show()


# ============================================================
# Question 5: Plot Tesla Stock Graph
# ============================================================

make_graph(tesla_data, tesla_revenue, 'Tesla Stock Data Graph')


# ============================================================
# Question 6: Plot GameStop Stock Graph
# ============================================================

make_graph(gme_data, gme_revenue, 'GameStop Stock Data Graph')

```
