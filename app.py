import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



app = dash.Dash(__name__)

server = app.server

def display_value():
    df_sup=data.loc[(data['salary']!=0) & (data['Expires']!=0)]
    fig = make_subplots(rows=1, cols=3)

    fig.add_trace(
        go.Box(y=df_sup['Avg. Salary'],text=df_sup['Player Name'],
            name="Salary",
            boxpoints='outliers', # only outliers
        marker_color='#ff2882',
        line_color='#963cff'),
        row=1, col=1
    )

    fig.add_trace(
        go.Box(y=df_sup['Transfer Fee'],text=df_sup['Player Name'],
            name="Transfer",
            boxpoints='outliers', # only outliers
        marker_color='#ff2882',
        line_color='rgb(0,0,0)'),
        row=1, col=2
    )

    fig.add_trace(
        go.Box(y=df_sup['time'],text=df_sup['Player Name'],
            name="Years contract",
                boxpoints='outliers', # only outliers
        marker_color='rgb(107,174,214)',
        line_color='#ff2882'),
        row=1, col=3,
    )

    fig.update_layout(height=600, width=800, title_text="Salary, transfer and years contract")
    return fig

def display_value3():
    df_sup_t=data.loc[data['Expires']!=0]
    Player_groups=df_sup_t.groupby("Player Name").sum().reset_index()
    Player_groups=Player_groups.sort_values('Transfer Fee', ascending=False)
    fig = px.bar(Player_groups.head(10), x="Player Name", y="Transfer Fee")
    fig.update_traces(marker_color='#ff2882',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Top Average transfer fee')
    return fig

def display_value5():
    df_sup_t=data.loc[data['Expires']!=0]
    Player_groups=df_sup_t.groupby("Player Name").sum().reset_index()
    Player_groups=Player_groups.sort_values('Avg. Salary', ascending=False)
    fig = px.bar(Player_groups.head(10), x="Player Name", y="Avg. Salary",)
    fig.update_traces(marker_color='#ff2882',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Top Average salary')
    return fig

def teams_trans():
    df_sup_t=data[['team','Transfer Fee','Pos.']]
    df_sup_t=df_sup_t.groupby(["team",'Pos.'])['Transfer Fee'].sum().reset_index()
    df_sup_t=df_sup_t.sort_values('Transfer Fee', ascending=False)
    fig = px.bar(df_sup_t, x="team", y="Transfer Fee", color="Pos.",
                color_discrete_sequence=['#ff2882', 'rgb(0,0,0)','#963cff','#37003c'],)
    fig.update_layout(title_text='Transfer fee spend by team and position')
    return fig

def teams_sal():
    df_sup_t=data[['team','Avg. Salary','Pos.']]
    df_sup_t=df_sup_t.groupby(["team",'Pos.'])['Avg. Salary'].sum().reset_index()
    df_sup_t=df_sup_t.sort_values('Avg. Salary', ascending=False)
    fig = px.bar(df_sup_t, x="team", y="Avg. Salary", color="Pos.",
                color_discrete_sequence=['#ff2882', 'rgb(0,0,0)','#963cff','#37003c'])
    fig.update_layout(title_text='Salary spend by team and position')
    return fig


data=pd.read_csv('salarios_epl.csv')
fig1=display_value()
fig2=teams_trans()
fig3=display_value3()
#fig5=display_value5()
fig4=teams_sal()

app.layout = html.Div([
    html.Div(className='Cabecera', children=[
        html.H3('Transfer Fee by players and teams on the English Premiere League')
    ]),
    dcc.Tabs(parent_className='custom_tabs',children=[
        dcc.Tab(label='All teams', className='custom-tab',
                selected_className='custom-tab--selected', children=[
            html.Div(className='grid', children=[
                html.Div(className='caja', children=[
                    dcc.Graph(figure=fig1),
                ]),
                html.Div(className='caja', children=[
                    dcc.Graph(figure=fig2),
                ]),
                html.Div(className='caja', children=[
                        dcc.Graph(figure=fig3),
                ]),
                html.Div(className='caja', children=[
                        dcc.Graph(figure=fig4),
                ]),
                html.Div(className='caja', children=[
                        dcc.Graph(id='figure5'),
                        dcc.RangeSlider(
                            id='slide-top',
                            min=10,
                            max=20,
                            step=1,
                            value=[10]
                        ),
                ]),                
            ]),
        ]),
        dcc.Tab(label='Filter team', className='custom-tab',
                selected_className='custom-tab--selected', children=[
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in data['team'].unique()],
                placeholder="Select a team or teams",
                multi=True,
            ),
            html.Div(className='grid', children=[
                html.Div(className='caja', children=[
                    dcc.Graph(id='display-tree'),
                ]),
                html.Div(className='caja', children=[
                    dcc.Graph(id='display-two'),
                ]),
                html.Div(className='caja', children=[
                    dcc.Graph(id='display-spyder'),
                ]),
                html.Div(className='caja', children=[
                    dcc.Graph(id='display-meanage'),
                ]),
                html.Div(className='caja', children=[
                    dcc.Graph(id='display-facet'),
                ])
            ])
        ]),
    ]),
])

@app.callback(Output('display-tree', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value3(value):
    print(value)
    df_sup=data.loc[(data['salary']!=0) & (data['Expires']!=0)]
    fil_team=df_sup
    if (value != None):
        if (len(value)>0):
        #fil_team=df_sup.loc[df_sup['team']==value]
            fil_team=df_sup.loc[df_sup['team'].isin(value)]
    fig = px.treemap(fil_team, path=['Pos.', 'Player Name'], values='salary',
                  color='salary', hover_data=['Age'],
                  color_continuous_scale='RdBu')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig

@app.callback(Output('display-two', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value2(value):
    df_sup=data.loc[data['Expires']!=0]
    df_sup['time']= df_sup['time'].astype(int)
    if (value != None):
        if (len(value)>0):
            df_sup=df_sup.loc[df_sup['team'].isin(value)]
    fig = px.scatter(df_sup, x="Transfer Fee", y="salary", color="team", size='time',
                 hover_data=['Player Name'], title="Relation between transfer fee and salary")
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ), 
     paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(opacity=0.75)
    return fig

@app.callback(Output('display-spyder', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value4(value):
    print(value)
    df_sup=data.loc[(data['salary']!=0) & (data['Expires']!=0)]
    if (value != None):
        if (len(value)>0):
        #df_sup=df_sup.loc[df_sup['team']==value]
            df_sup=df_sup.loc[df_sup['team'].isin(value)]
    edades=df_sup.groupby("Age").count().reset_index()
    edades['Age']=edades['Age'].astype(str)

    fig = go.Figure(data=go.Scatterpolar(r=edades['salary'],
            theta=edades['Age'],
            fill='toself'
            ))
    fig.update_traces(marker_color='#ff2882',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True),),showlegend=False,
                    title_text='Players Age count')
    return fig

@app.callback(Output('display-meanage', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_age_mean(value):
    print(value)
    df_sup=data.loc[(data['salary']!=0) & (data['Expires']!=0)]
    if (value != None):
        if (len(value)>0):
        #df_sup=df_sup.loc[df_sup['team']==value]
            df_sup=df_sup.loc[df_sup['team'].isin(value)]
    edades=df_sup.groupby("Age").count().reset_index()
    edades['Age']=edades['Age'].astype(str)

    fig = px.histogram(df_sup, x="Age",
                   marginal="box", # or violin, rug
                   hover_data=df_sup.columns)
    fig.update_traces(marker_color='#ff2882',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Players Age Histogram')
    return fig

@app.callback(Output('display-facet', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_facet(value):
    print(value)
    df_sup=data.loc[data['Expires']!=0]
    if (value != None):
        if (len(value)>0):
        #df_sup=df_sup.loc[df_sup['team']==value]
            df_sup=df_sup.loc[df_sup['team'].isin(value)]
    edades=df_sup.groupby("Age").count().reset_index()
    edades['Age']=edades['Age'].astype(str)
    fig = px.bar(df_sup, x="Transfer Fee", y="Player Name",facet_col="Pos.",
            facet_col_wrap=2,
            facet_col_spacing=0.19,
            category_orders={"Pos.": ["GK", "D", "M", "F"]})
    fig.update_traces(marker_color='#963cff',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_yaxes(matches=None,showticklabels=True)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True),),showlegend=False,
                        title_text='Player by position makingcomparisson transfer fee')
    return fig

@app.callback(
    dash.dependencies.Output('figure5', 'figure'),
    [dash.dependencies.Input('slide-top', 'value')])
def top_slider(value):
    df_sup_t=data.loc[data['Expires']!=0]
    Player_groups=df_sup_t.groupby("Player Name").sum().reset_index()
    Player_groups=Player_groups.sort_values('Avg. Salary', ascending=False)
    fig = px.bar(Player_groups.head(value[0]), x="Player Name", y="Avg. Salary")
    fig.update_traces(marker_color='#ff2882',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Top Average salary')
    return fig




if __name__ == '__main__':
    app.run_server(debug=False)
