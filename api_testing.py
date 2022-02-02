from flask import Flask, jsonify 
from flask_restful import Resource, Api , reqparse
import pandas as pd
import plotly.express as px
import pandas as pd

from plotly import graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

df=pd.read_csv('C:/Users/Drishya/checkkarrhe.csv')
        
    
def drawFigure3():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                       df, x="Datetime", y="Label", color="Location", title="Long-Form Input"
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
    ])
    
    
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

def drawFigure2():
    return    html.Div(
                children=[
 #Description below the header
        dcc.Dropdown(id='BM-dropdown2',
                options=[{'label': x, 'value': x}
                        for x in df['Username'].unique()],
                 value='Username',
                 multi=False, clearable=True),
    dcc.Graph(id='bar-chart2')]
             
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



app=Flask(__name__)
api=Api(app)

# Build App
app1 = dash.Dash(external_stylesheets=[dbc.themes.SLATE],server=app)
app1.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col([drawText()], width=13),
            ], align='center'),
            
            html.Br(),
            dbc.Row([
            dbc.Col([drawFigure()], width=6),
            dbc.Col([drawFigure1()], width=3)
            ], align='center'),
            
            html.Br(),
            dbc.Row([dbc.Col([drawFigure2()], width=6),
                     dbc.Col([drawFigure3()], width=6),
            #dbc.Col([drawFigure()], width=3),
            ])
            
    ])
    )
])


data_arg=reqparse.RequestParser()
data_arg.add_argument("ID" , type=int ,help="Enter ID")
data_arg.add_argument("Datetime" , type=str ,help="Enter Datetime")
data_arg.add_argument("Username" , type=str ,help="Enter Username")
data_arg.add_argument("Location" , type=str ,help="Enter Location")
data_arg.add_argument("Label" , type=str ,help="Enter Label")


class read_Delete(Resource):
    def __init__(self):
        # read csv file
        self.data = pd.read_csv('C:/Users/Drishya/checkkarrhe.csv')
    # GET request on the url will hit this function
    def get(self,ID):
        # find data from csv based on user input
        data_fount=self.data.loc[self.data['ID'] == ID].to_json(orient="records")
        # return data found in csv
        return jsonify({'message': data_fount})
    # Delete request on the url will hit this function
    def delete(self,ID):
        if ((self.data['ID'] == ID).any()):
            # Id it present delete data from csv
            self.data = self.data.drop(self.data["ID"].loc[self.data["ID"] == ID].index)
            self.data.to_csv("C:/Users/Drishya/list_testing.csv", index=False)
            return jsonify({"message": 'Deleted successfully'})
        else:
            return jsonify({"message": 'Not Present'})
                
        
class Create_Update(Resource):
    def __init__(self):
        # read data from csv
        self.data = pd.read_csv('C:/Users/Drishya/checkkarrhe.csv')

    # POST request on the url will hit this function
    def post(self):
        # data parser to parse data from url
        args = data_arg.parse_args()
        # if ID is already present
        if((self.data['ID']==args.ID).any()):
            return jsonify({"message": 'ID already exist'})
        else:
            # Save data to csv
            self.data= self.data.append(args, ignore_index=True)
            self.data.to_csv("C:/Users/Drishya/checkkarrhe.csv", index=False)
            return jsonify({"message": 'Done'})

    # PUT request on the url will hit this function
    def put(self):
        args = data_arg.parse_args()
        if ((self.data['ID'] == args.ID).any()):
            # if ID already present Update it
            self.data=self.data.drop(self.data["ID"].loc[self.data["ID"] == args.ID].index)
            self.data = self.data.append(args, ignore_index=True)
            self.data.to_csv("C:/Users/Drishya/checkkarrhe.csv", index=False)
            return jsonify({"message": 'Updated successfully'})
        else:
            # If ID not present Save that data to csv
            self.data = self.data.append(args, ignore_index=True)
            self.data.to_csv("C:/Users/Drishya/checkkarrhe.csv", index=False)
            return jsonify({"message": 'successfully Created'})
        
        

api.add_resource(read_Delete, '/<int:ID>')
api.add_resource(Create_Update,'/')

@app1.callback(
    Output(component_id="bar-chart", component_property="figure"),
    [Input(component_id="BM-dropdown", component_property="value")],
)
        
def display_BM_composition(selected_BM):
    filtered_BM = df[df.Location == selected_BM]  # Only use unique values in column "BM_NAME" selected in dropdown

    barchart = px.bar(
        data_frame=filtered_BM,
        x="Label",
        opacity=0.9).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )

    return barchart


@app1.callback(
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



@app1.callback(
    Output(component_id="bar-chart2", component_property="figure"),
    [Input(component_id="BM-dropdown2", component_property="value")],
)
        
def display_BM_composition(selected_BM):
    filtered_BM = df[df.Username == selected_BM]  # Only use unique values in column "BM_NAME" selected in dropdown

    barchart = px.bar(
        data_frame=filtered_BM,
        x="Label",
        opacity=0.9).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    )

    return barchart


if __name__ == '__main__':
    app1.run_server(port=8050)
