import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os
file_path = os.path.join(os.path.dirname(__file__), 'data', 'Customer Purchasing Behaviors.csv')
data = pd.read_csv(file_path)

app = Dash(__name__)
server=app.server
app.title = "Customer Purchase Behavior Dashboard"

avg_age = round(data['age'].mean(), 1)
avg_income = round(data['annual_income'].mean(), 0)
avg_purchase = round(data['purchase_amount'].mean(), 0)
avg_loyalty = round(data['loyalty_score'].mean(), 2)

hist_fig = px.histogram(
    data, x='purchase_amount', nbins=15,
    title="Distribution of Purchase Amounts",
    color_discrete_sequence=['#636EFA']
)

box_fig = px.box(
    data, y='purchase_amount', color_discrete_sequence=['#EF553B'],
    title="Purchase Amount Outlier Analysis"
)

region_fig = px.bar(
    data.groupby('region')['purchase_amount'].mean().reset_index(),
    x='region', y='purchase_amount', color='region',
    title="Average Purchase Amount by Region",
    color_discrete_sequence=px.colors.qualitative.Plotly
)

scatter_fig = px.scatter(
    data, x='annual_income', y='purchase_amount',
    color='region', size='loyalty_score',
    hover_data=['age', 'purchase_frequency'],
    title="Relationship Between Income and Purchase Amount"
)
pie_fig = px.pie(
    data, names='region',
    title="Regional Distribution of Customers",
    color_discrete_sequence=px.colors.qualitative.Safe
)

violin_fig = px.violin(
    data,
    x='region',
    y='loyalty_score',
    box=True,            
    points='all',        
    hover_data=['age', 'purchase_amount'],
    title="Distribution of Loyalty Score by Region",
    color='region',
    color_discrete_sequence=px.colors.qualitative.Bold
)

app.layout = html.Div([
    html.H1("Customer Purchase Behavior Dashboard", 
            style={'textAlign': 'center', 'color': '#003366', 'marginBottom': '10px'}),

    html.P("Visual Analysis of Descriptive Statistics and Outlier Detection",
           style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H4(f"Average Age: {avg_age} years"),
            html.H4(f"Average Income: ₹{avg_income}"),
            html.H4(f"Avg Purchase Amount: ₹{avg_purchase}"),
            html.H4(f"Avg Loyalty Score: {avg_loyalty}")
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            dcc.Graph(figure=pie_fig)
        ], style={'width': '50%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        dcc.Graph(figure=region_fig),
        dcc.Graph(figure=violin_fig)
    ]),

    html.Div([
        dcc.Graph(figure=hist_fig),
        dcc.Graph(figure=box_fig)
    ]),

    html.Div([
        dcc.Graph(figure=scatter_fig)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
