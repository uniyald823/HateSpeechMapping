import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from plotly import graph_objs as go
import plotly.express as px
df = pd.read_csv("C:/Users/Drishya/list_to_be_checked.csv")
# Iris bar figure
'''def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])'''

def drawFigure():
    return    html.Div(
                children=[
 #Description below the header
        dcc.Dropdown(id='BM-dropdown',
                options=[{'label': x, 'value': x}
                        for x in df['Location'].unique()],
                 value='Location',
                 multi=False, clearable=True),
    dcc.Graph(id='bar-chart')]
             
)

def drawFigure1():
    return  html.Div(
            children=[
                html.Div(children=[
                    dcc.Dropdown(id='dropdown1',
                              options=[{'value':x,'label':x} 
                                       for x in df.Username.unique()],
                              clearable=False,
                              value='Bangkok',
                              ),
                    ], className='menu-l'
                    ),
                dcc.Graph(id='interaction2',
                          config={'displayModeBar':False},
                          className='card')]                
            )

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Mapping Online Hate Speech to Offline Crimes"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])


# Build App
app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

server = app.server

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col([drawText()], width=13),
            ], align='center'),
            
            html.Br(),
            dbc.Row([
            dbc.Col([drawFigure()], width=5),
            dbc.Col([drawFigure1()], width=3)
            #dbc.Col([drawFigure()], width=6),
            ], align='center'),
            
            #html.Br(),
            #dbc.Row([dbc.Col([drawFigure()], width=9),
            #dbc.Col([drawFigure()], width=3),
           # ])
            
    ])
    )
])

@app.callback(
    Output(component_id="bar-chart", component_property="figure"),
    [Input(component_id="BM-dropdown", component_property="value")],
)
        
def display_BM_composition(selected_BM):
    filtered_BM = df[df.Username == selected_BM]  # Only use unique values in column "BM_NAME" selected in dropdown

    barchart = px.line(
        data_frame=filtered_BM,
        x="Label").update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )
    return barchart


@app.callback(
 Output('interaction2', 'figure'),
    [Input('dropdown1','value')]
)


def update_pie_chart(select_d1):
    df3=df.loc[df['Username']==select_d1]
    ## using dash to make the pie chart
    fig1=go.Figure(data=[go.Pie(labels=df3['Label'].value_counts().index.tolist(),
                         values=list(df3['Label'].value_counts()))])
    ## customizing the title of the pie chart
    #names={'sex':'Sex','risk':'Case Origin'}
    
    fig1.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',)
    return fig1 #to be outputted!




# Run app and display result inline in the notebook
app.run_server()
