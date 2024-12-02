import pandas as pd
import plotly.graph_objects as go
import math

df = pd.read_csv("modified_dataset.csv")

#Converting States to numeric data
df['STATE_N'] = df['STATE'].astype('category').cat.codes
state_mapping = dict(zip(df['STATE'], df['STATE_N']))

#Converting States to numeric data
df['CONSTITUENCY_N'] = df['CONSTITUENCY'].astype('category').cat.codes
constituency_mapping = dict(zip(df['CONSTITUENCY'], df['CONSTITUENCY_N']))

#Converting States to numeric data
df['PARTY_N'] = df['PARTY'].astype('category').cat.codes
party_mapping = dict(zip(df['PARTY'], df['PARTY_N']))

#Converting States to numeric data
df['GENDER_N'] = df['GENDER'].astype('category').cat.codes
gender_mapping = dict(zip(df['GENDER'], df['GENDER_N']))
gender_mapping = {k: v for k, v in gender_mapping.items() if not (isinstance(k, float) and math.isnan(k))}

#Converting States to numeric data
df['CATEGORY_N'] = df['CATEGORY'].astype('category').cat.codes
category_mapping = dict(zip(df['CATEGORY'], df['CATEGORY_N']))
category_mapping = {k: v for k, v in category_mapping.items() if not (isinstance(k, float) and math.isnan(k))}


#Converting States to numeric data
df['EDUCATION_N'] = df['EDUCATION'].astype('category').cat.codes
education_mapping = dict(zip(df['EDUCATION'], df['EDUCATION_N']))


def get_pcp_default():
    fig = go.Figure(data=
        go.Parcoords(
            line = dict(color = df['WINNER'],
                    colorscale = [[0,'purple'],[1,'gold']]),
            dimensions = list([
                dict(
                    range=[min(list(gender_mapping.values())),max(list(gender_mapping.values()))],
                    tickvals = list(gender_mapping.values()),
                    ticktext = list(gender_mapping.keys()),
                    label = "GENDER", values = df['GENDER_N']),
                dict(
                    range=[min(list(category_mapping.values())),max(list(category_mapping.values()))],
                    tickvals = list(category_mapping.values()),
                    ticktext = list(category_mapping.keys()),
                    label = "CATEGORY", values = df['CATEGORY_N']),
                dict(
                    range=[min(list(education_mapping.values())),max(list(education_mapping.values()))],
                    tickvals = list(education_mapping.values()),
                    ticktext = list(education_mapping.keys()),
                    label = "EDUCATION", values = df['EDUCATION_N']),
                dict(
                    range=[0,1],
                    tickvals= [0,1],
                    ticktext=['Lost','Won'],
                    label = 'WINNER', values = df['WINNER']),
                dict(
                    range=[min(list(df['CRIMINAL_CASES'])),max(list(df['CRIMINAL_CASES']))],
                    label = 'CRIMINAL_CASES', values = df['CRIMINAL_CASES']),
                dict(
                    range=[min(list(df['AGE'])),max(list(df['AGE']))+10],
                    label = 'AGE', values = df['AGE']),
                dict(
                    range=[min(list(df['ASSETS'])),max(list(df['ASSETS']))],
                    label = 'ASSETS', values = df['ASSETS']),
                dict(
                    range=[min(list(df['LIABILITIES'])),max(list(df['LIABILITIES']))],
                    label = 'LIABILITIES', values = df['LIABILITIES']),
                dict(
                    range=[min(list(df['GENERAL_VOTES'])),max(list(df['GENERAL_VOTES']))],
                    label = 'GENERAL_VOTES', values = df['GENERAL_VOTES']),
                dict(
                    range=[min(list(df['POSTAL_VOTES'])),max(list(df['POSTAL_VOTES']))],
                    label = 'POSTAL_VOTES', values = df['POSTAL_VOTES']),
                dict(
                    range=[min(list(df['TOTAL_VOTES'])),max(list(df['TOTAL_VOTES']))],
                    label = 'TOTAL_VOTES', values = df['TOTAL_VOTES']),
                dict(
                    range=[min(list(df['TOTAL_ELECTORS'])),max(list(df['TOTAL_ELECTORS']))],
                    label = 'TOTAL_ELECTORS', values = df['TOTAL_ELECTORS']),
                
            
            ]       
        )
        )
    )

    fig.update_layout(
        xaxis_tickangle=45,  # Rotate tick labels by 45 degrees
        font=dict(size=10),  # Reduce label font size
        plot_bgcolor = 'white',
        paper_bgcolor = 'white'
    )
    fig.update_layout(
    title=dict(
        text='Parallel Coordinates Plot for India',
        x=0.5,  # Center the title horizontally
        y=0.95,  # Position the title at the top of the plot
        xanchor='center',  # Anchor the title's horizontal position to its center
        yanchor='top',  # Anchor the title's vertical position to the top
        font=dict(
            family="Arial, sans-serif",  # Specify the font family
            size=20,  # Specify the font size
            color="black"  # Specify the font color
        )
    ),
    xaxis_tickangle=45,  # Rotate tick labels by 45 degrees
    font=dict(size=10),  # Reduce label font size
    plot_bgcolor='white',
    paper_bgcolor='white'
)

    return fig

def get_pcp_state(state):
    
    fig = go.Figure(data=
        go.Parcoords(
            line = dict(color = df[df['STATE']==state]['WINNER'],
                    colorscale = [[0,'purple'],[1,'gold']]),
            dimensions = list([
                dict(
                    range=[min(list(gender_mapping.values())),max(list(gender_mapping.values()))],
                    tickvals = list(gender_mapping.values()),
                    ticktext = list(gender_mapping.keys()),
                    label = "GENDER", values = df[df['STATE']==state]['GENDER_N']),
                dict(
                    range=[min(list(category_mapping.values())),max(list(category_mapping.values()))],
                    tickvals = list(category_mapping.values()),
                    ticktext = list(category_mapping.keys()),
                    label = "CATEGORY", values = df[df['STATE']==state]['CATEGORY_N']),
                dict(
                    range=[min(list(education_mapping.values())),max(list(education_mapping.values()))],
                    tickvals = list(education_mapping.values()),
                    ticktext = list(education_mapping.keys()),
                    label = "EDUCATION", values = df[df['STATE']==state]['EDUCATION_N']),
                dict(
                    range=[0,1],
                    tickvals= [0,1],
                    ticktext=['Lost','Won'],
                    label = 'WINNER', values = df[df['STATE']==state]['WINNER']),
                dict(
                    range=[min(list(df['CRIMINAL_CASES'])),max(list(df['CRIMINAL_CASES']))],
                    label = 'CRIMINAL_CASES', values = df[df['STATE']==state]['CRIMINAL_CASES']),
                dict(
                    range=[min(list(df['AGE'])),max(list(df['AGE']))+10],
                    label = 'AGE', values = df[df['STATE']==state]['AGE']),
                dict(
                    range=[min(list(df['ASSETS'])),max(list(df['ASSETS']))],
                    label = 'ASSETS', values = df[df['STATE']==state]['ASSETS']),
                dict(
                    range=[min(list(df['LIABILITIES'])),max(list(df['LIABILITIES']))],
                    label = 'LIABILITIES', values = df[df['STATE']==state]['LIABILITIES']),
                dict(
                    range=[min(list(df['GENERAL_VOTES'])),max(list(df['GENERAL_VOTES']))],
                    label = 'GENERAL_VOTES', values = df[df['STATE']==state]['GENERAL_VOTES']),
                dict(
                    range=[min(list(df['POSTAL_VOTES'])),max(list(df['POSTAL_VOTES']))],
                    label = 'POSTAL_VOTES', values = df[df['STATE']==state]['POSTAL_VOTES']),
                dict(
                    range=[min(list(df['TOTAL_VOTES'])),max(list(df['TOTAL_VOTES']))],
                    label = 'TOTAL_VOTES', values = df[df['STATE']==state]['TOTAL_VOTES']),
                dict(
                    range=[min(list(df['TOTAL_ELECTORS'])),max(list(df['TOTAL_ELECTORS']))],
                    label = 'TOTAL_ELECTORS', values = df[df['STATE']==state]['TOTAL_ELECTORS']),
                
            
            ]       
        )
        )
    )

    fig.update_layout(
        xaxis_tickangle=45,  # Rotate tick labels by 45 degrees
        font=dict(size=10),  # Reduce label font size
        plot_bgcolor = 'white',
        paper_bgcolor = 'white'
    )
    fig.update_layout(
    title=dict(
        text='Parallel Coordinates Plot for ' + state,
        x=0.5,  # Center the title horizontally
        y=0.95,  # Position the title at the top of the plot
        xanchor='center',  # Anchor the title's horizontal position to its center
        yanchor='top',  # Anchor the title's vertical position to the top
        font=dict(
            family="Arial, sans-serif",  # Specify the font family
            size=20,  # Specify the font size
            color="black"  # Specify the font color
        )
    ),
    xaxis_tickangle=45,  # Rotate tick labels by 45 degrees
    font=dict(size=10),  # Reduce label font size
    plot_bgcolor='white',
    paper_bgcolor='white'
    )

    return fig