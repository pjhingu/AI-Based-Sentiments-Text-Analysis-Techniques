# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:08:37 2021

@author: DELL2
"""
import dash
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd 
from datapreprocessing import preprocessingnpredictions,etsyprediction
import plotly 
import plotly.express as px
import plotly.io as pio
import os.path
import webbrowser

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
project_name= 'Review Sentiment Analysis'


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

def newdf():        
    df=pd.read_csv(r'estypredictedreviews.csv')
    dfn=df[df['predictedvalue']==0] 
    dfn=dfn.iloc[:6,:]
    dfp=df[df['predictedvalue']==1]
    dfp=dfp.iloc[:6,:]
    df1=pd.concat([dfp,dfn])       
    return  df1  

def pie():
    df=pd.read_csv(r'estypredictedreviews.csv')
    dfn=df[df['predictedvalue']==0] 
    dfn=dfn.iloc[:6,:]
    dfp=df[df['predictedvalue']==1]
    dfp=dfp.iloc[:6,:]
    df1=pd.concat([dfp,dfn])

    pie_chart=px.pie(
        data_frame=df,
        values=[df['predictedvalue'].value_counts()[1],df['predictedvalue'].value_counts()[0]],
        names=['Positive Reviews','Negative Reviews'],
        color=['Positive Reviews','Negative Reviews'],
        color_discrete_sequence=['Green','Red'],
        title='Positive and Negative Reviews Distribution',
        #width=600,                          
        #height=380,                         
        #hole=0.5, 
    )
    return pie_chart

def create_app_ui():
    layout = dbc.Container([
        #title
        dbc.Row([
            dbc.Col(html.H1("Review Sentiment Analysis"),className='text-center')
            ]),
        #pie chart
        dbc.Row([
            dbc.Card(dcc.Graph(figure = pie()),className='card',
                     style ={"box-shadow": "10px 10px 5px grey",
                             "transition":"all ease 0.4s",
                             "padding": "50px",
                             "margin": "auto",
                             "transform":"scale(0.98) translate",
                             }
                             )
            ]),
        #dropdown reviews
        dbc.Row([
            dbc.Col(
                html.Div([html.H2(children='Etsy Reviews',className='text-center',style={"margin":"20px"}),
                          dcc.Dropdown(id='dropdown',
                          placeholder="Select exisiting Review",
                          options=[{'label':i,'value':i}for i in newdf().review],
                          value='Select the etsy reviews',
                          optionHeight=70,
                          style ={
                             "padding": "50px",
                             "margin": "auto",}
                          
                    ),
                dbc.Button("Submit", 
                id='submitdropdown',
                color="dark", 
                className="mr-1",
                n_clicks=0,
                style={'margin':'0 45%','padding':'5px 15px'}
                ),
                html.Div(id='container1',style={'padding-top':'15px'})
                
                ])),
            #word cloud
            dbc.Row([
                dbc.Col([
                    html.Div([html.H2('Word Cloud',style={"margin":"20px"}),
                    dbc.Button("ALL Words",
                    id="allbt",
                    outline=True,
                    color="info", 
                    className="mr-1",
                    n_clicks_timestamp=0,
                    style={'margin':'auto',}
                    ),
                   dbc.Button("Positve Words",
                   id="posbt",
                   outline=True,
                   color="success", 
                  className="mr-1",
                  n_clicks_timestamp=0,
                  style={'margin':'auto',}
                  ),
                 dbc.Button("Negative Words",
                 id="negbt",
                 outline=True, 
                 color="danger",
                 className="mr-1",
                 n_clicks_timestamp=0,
                 style={'margin':'auto',}
                 )
                 ],style={'margin':'auto'}
                 ),
                 html.Div(id='container',style={'padding':'15px'})
                    
                    ]),
                #_________Try it Yourself part________
            dbc.Col([
            html.H2("Try it Yourself!",style={'padding':'15px'}),
            html.Div([
              dcc.Textarea(
                id='textarea',
                placeholder="Enter Your review text here",
                rows=5,
                # cols=8,
                style={'width':'650px','height':'300'}
            ),
            html.Div(id='container2',style={'padding':'15px 15px 15px 10px'})
         ])
        ])
                                 
                ])
            ]),
        dbc.Row([
            dbc.Col(html.H4("Thank You..."),className='text-center')
            ]),
               
        ])   
    return layout

@app.callback(
    Output('container','children'),
    [
        Input('allbt','n_clicks_timestamp'),
        Input('posbt','n_clicks_timestamp'),
        Input('negbt','n_clicks_timestamp'),
    ]
)
def wordcloudbutton(allbt,posbt,negbt):

    if int(allbt) > int(posbt) and int(allbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('wholeword.png'))])
    elif int(posbt) > int(allbt) and int(posbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('posword.png'))
            ])
    elif int(negbt) > int(allbt) and int(negbt) > int(posbt):
       return html.Div([
           html.Img(src=app.get_asset_url('wholeword.png'))
           ])
    else:
        pass
    
@app.callback(
    Output('container1','children'),
    [
        Input('submitdropdown','n_clicks')
    ],
    State('dropdown','value'))

def dropdownui(n_clicks,value):
    predict=preprocessingnpredictions(value)
    if (n_clicks>0):
        if(int(predict)==1):
            return html.Div([
                dbc.Alert("Its a Positive review", color="success")
                ])
        else:
            return html.Div([
                    dbc.Alert("Its a Negative review", color="danger")
                ])

@app.callback(
    Output('container2','children'),
    [
        Input('textarea','value')
    ])

def updatetextarea(textvalue):
    predicted_value=preprocessingnpredictions(textvalue)
    if(int(predicted_value)==1):
            return html.Div([
                dbc.Alert("Its a Positive review", color="success")
                ])
    else:
        return html.Div([
                dbc.Alert("Its a Negative review", color="danger")
                ])


  
# Main Function to control the Flow of your Project
def main():
    print("Start of your project")
    open_browser()
    global project_name
    global app
    
    project_name = "Sentiment Analysis with Insights"
    #print("My project name = ", project_name)
    #print('my scrapped data = ', scrappedReviews.sample(5) )
    
    
    app.title = project_name
    app.layout = create_app_ui()
    app.run_server()
    
    
    
    print("End of my project")
    project_name = None
    app = None
    
        
# Calling the main function 
if __name__ == '__main__':
    main()