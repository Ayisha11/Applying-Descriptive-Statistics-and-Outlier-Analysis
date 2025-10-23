import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

file_path = '/Users/ayishasalmira/Downloads/CustomerBehaviourProject /Customer Purchasing Behaviors.csv'
data = pd.read_csv(file_path)

app = Dash(__name__)
app.title = "Customer Purchase Behavior Dashboard"

avg_age = round(data['age'].mean(), 1)
avg_income = round(data['annual_income'].mean(), 0)
avg_purchase = round(data['purchase_amount'].mean(), 0)
avg_loyalty = round(data['loyalty_score'].mean(), 2)


hist_fig = px.histogram(
    data,
    x='purchase_amount',
    nbins=15,
    title="Distribution of Purchase Amounts",
    color_discrete_sequence=['#636EFA']
)

box_fig = px.box(
    data,
    y='purchase_amount',
    title="Purchase Amount Outlier Analysis",
    color_discrete_sequence=['#EF553B']
)

region_fig = px.bar(
    data.groupby('region')['purchase_amount'].mean().reset_index(),
    x='region',
    y='purchase_amount',
    title="Average Purchase Amount by Region",
    color='region',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

app.layout = html.Div([
    html.H1("Customer Purchase Behavior Dashboard", style={'textAlign': 'center', 'color': '#003366'}),
    html.P("Visual Analysis of Descriptive Statistics and Outlier Detection", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H4(f"Average Age: {avg_age} years"),
            html.H4(f"Average Income: ₹{avg_income}"),
            html.H4(f"Avg Purchase Amount: ₹{avg_purchase}"),
            html.H4(f"Avg Loyalty Score: {avg_loyalty}")
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

        html.Div([
            dcc.Graph(figure=region_fig)
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(figure=hist_fig),
        dcc.Graph(figure=box_fig)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
