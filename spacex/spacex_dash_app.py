# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

marksmap={}
for i in range(0,12500,2500):
  marksmap[i]=str(i)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                      {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                      {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                      {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                    value='ALL',
                                    placeholder='Select a launch site here:',
                                    searchable=True)),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks=marksmap,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data=spacex_df[spacex_df['class']==1][['Launch Site','class']].groupby(['Launch Site'],as_index=False).count()
        print(data.columns)
        print(data)
        fig = px.pie(data, values='class', 
            names='Launch Site', 
            title='Total success lauches by site')
        return fig
    else:
        data=spacex_df[spacex_df['Launch Site']==entered_site][['class']].groupby(['class'],as_index=False).count()
        data=spacex_df[spacex_df['Launch Site']==entered_site].groupby('class',as_index=False).count()
        #print(data.columns)
        #print(data)
        fig = px.pie(data, values='Launch Site', 
            names='class', 
            title='Successes and failures at '+entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

'''Next, we want to plot a scatter plot with the x axis to be the payload and the y axis to be the launch outcome 
(i.e., class column).
As such, we can visually observe how payload may be correlated with mission outcomes for selected site(s).

In addition, we want to color-label the Booster version on each scatter point so that we may
observe mission outcomes with different boosters.

Now, let’s add a call function including the following application logic:

    Input to be [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
    Note that we have two input components, one to receive selected launch site and another to receive selected payload range
    Output to be Output(component_id='success-payload-scatter-chart', component_property='figure')
    A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
        If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) 
        and variable class.
        In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
        If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart 
        to show
        values Payload Mass (kg) and class for the selected site, and color-label the point 
        using Boosster Version Category likewise.
'''

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
def make_scatterplot(siteInput,payloadInput):
  print(payloadInput[0])
  print(payloadInput[1])
  if 'ALL'==siteInput:
    data = spacex_df
  else:
    data = spacex_df[spacex_df['Launch Site']==siteInput]
  data=data[(data['Payload Mass (kg)']>=payloadInput[0]) & (data['Payload Mass (kg)']<=payloadInput[1])]
  return px.scatter(data,x='Payload Mass (kg)',y='class',color='Booster Version Category')

'''
    Which site has the largest successful launches? KSK lc-39A
    Which site has the highest launch success rate? KSK lc-39A
    Which payload range(s) has the highest launch success rate? 2/4k
    Which payload range(s) has the lowest launch success rate? 6/10k
    Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest 
    launch success rate? FT
'''


# Run the app
if __name__ == '__main__':
    app.run_server()

