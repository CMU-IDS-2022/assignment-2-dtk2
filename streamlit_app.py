import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
import altair as alt
import streamlit as st
alt.data_transformers.disable_max_rows()
from IPython.display import Image
from IPython.display import display, HTML


st.title("Data Visualization, Sustainable Development Goal: Clean Water & Sanitation")


waterdf = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-dtk2/master/water.csv", on_bad_lines='skip', encoding = "ISO-8859-1")
#sanitdf = pd.read_csv('/content/drive/MyDrive/SPRING 2022 COURSES/05-839 Interactive Data Science/Assignments/Assignment 3/DATA/sanitation.csv', encoding = "ISO-8859-1")

print(waterdf.shape)
print(waterdf.describe())
print(waterdf.isna().sum())

waterdf = waterdf.dropna(subset=['POP_THOUS'])
print(waterdf.shape)
waterdf.isnull().sum()



waterdf['POP_THOUS'] = waterdf['POP_THOUS'].str.replace(' ', '')
waterdf['POP_THOUS'] = waterdf['POP_THOUS'].astype(int)


print(waterdf.head())
print(waterdf.describe())

st.write(Image('https://unstats.un.org/sdgs/assets/img/sliders/2017-Regions-E-large.png'))

#Correlation Matrix
cor_data = (waterdf[['BASIC_WAT_NAT', 	'LIMITED_WAT_NAT', 	'UNIMPROVED_WAT_NAT', 	'SURFACE_WAT_NAT', 	'SAFELY_MANAGED_NAT', 	'ACCESS_ONPREMISE_NAT', 	'AVAIL_WHEN_NEEDED_NAT', 	
                    'NON_CONTAMIN_NAT', 	'PIPED_NAT', 	'NONPIPED_NAT']]
            ).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})

cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
#print(cor_data)

base = alt.Chart(cor_data).encode(
    x='variable2:O',
    y='variable1:O'    
)

# Text layer with correlation labels
# Colors are for easier readability
text = base.mark_text().encode(
    text='correlation_label',
    color=alt.condition(
        alt.datum.correlation > 0.1, 
        alt.value('black'),
        alt.value('white')
    )
)

# The correlation heatmap
cor_plot = base.mark_rect().encode(
    
    color=alt.Color('correlation:Q', scale=alt.Scale(scheme='plasma'))
).properties(
    width=500,
    height=500,
    title="The Correlation Matrix: Drinking Water"
)

st.altair_chart((cor_plot + text))

waterpie = waterdf[['COUNTRY','YEAR','BASIC_WAT_NAT','LIMITED_WAT_NAT','UNIMPROVED_WAT_NAT','SURFACE_WAT_NAT']]
#waterpie = waterpie[waterpie['YEAR']==2020]
#waterpie
waterpie_melt = pd.melt(waterpie, id_vars=['COUNTRY','YEAR'], value_vars=['BASIC_WAT_NAT','LIMITED_WAT_NAT','UNIMPROVED_WAT_NAT','SURFACE_WAT_NAT'])

#waterpie_melt
#waterpie_melt.isna().sum()

slider1 = alt.binding_range(min=2000, max=2020, step=1, name='YEAR')
select_year1 = alt.selection_single(name="YEAR", fields=['YEAR'],
                                   bind=slider1, init={'YEAR': 2000})


popsdgchart = alt.Chart(waterdf).mark_bar(tooltip=True).encode(
    
    y = alt.Y('POP_THOUS',
              axis=alt.Axis(title='Population (in 1000s)'), sort='-x',
              scale=alt.Scale(domain=(0, 2400000))),
    
    x = alt.X('SDG region:O',
              axis=alt.Axis(title='SDG Regions'), 
              scale=alt.Scale(zero=False), sort='y'
              ),
              
    color= alt.Color('COUNTRY:O', legend = None, scale=alt.Scale(scheme='plasma'))
).properties(
    width = 300,
    height = 300,
    title="Population (2000-2020): SDG Regions"
).transform_filter(
    select_year1
).add_selection(
    select_year1
)

popyearchart = alt.Chart(waterdf).mark_bar(tooltip=True).encode(
    
    y = alt.Y('POP_THOUS',
              axis=alt.Axis(title='Population (in 1000s)'), sort='-x',
              scale=alt.Scale(domain=(0, 1600000))),
                  
    x = alt.X('COUNTRY:O',
              axis=alt.Axis(title='Countries'), 
              scale=alt.Scale(zero=False), sort='-y'
              ),  
    color= alt.Color('COUNTRY', legend = None, scale=alt.Scale(scheme='plasma'))
).transform_filter(
    select_year1
).add_selection(
    select_year1
).transform_filter(
    alt.datum.POP_THOUS > 40000
).properties(
    width = 300,
    height = 300,
    title="Population (2000-2020): World Nations"
)
###

popgrowth= alt.concat(
    popsdgchart, popyearchart
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

st.altair_chart(popgrowth)

selection = alt.selection_single(fields=['YEAR','COUNTRY'])

###
pipedwaterchart = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(
    x=alt.X('YEAR:O', axis=alt.Axis(title='Year')),
    y=alt.Y('PIPED_NAT', axis=alt.Axis(title='% Population with Piped Water Connections')),
    size='POP_THOUS',
    #shape='SDG region',
    color = alt.Color('COUNTRY', scale=alt.Scale(scheme='plasma')),
    tooltip='COUNTRY'
).add_selection(selection).encode(
    color=alt.condition(selection, "COUNTRY", alt.value("grey"), legend=None, scale=alt.Scale(scheme='plasma'))
).properties(
    title="Increase in Access to Piped Water Connections over Time",
    width=400
)
###

nationpie = alt.Chart(waterpie_melt).mark_arc().encode(
    theta=alt.Theta(field='mean_value', type="quantitative"),
    color=alt.Color('variable', scale=alt.Scale(scheme='plasma')),
    tooltip=('variable:O', 'mean_value:Q', 'COUNTRY:O', 'YEAR:O')
).transform_filter(
    selection
).transform_aggregate(
    mean_value='mean(value):Q',
    groupby=["variable"]
).properties(
    title="Access to Drinking Water"
)

chart_pie = alt.hconcat(
    pipedwaterchart , nationpie
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

st.altair_chart(chart_pie)

slider2 = alt.binding_range(min=2000, max=2020, step=1, name='YEAR')
select_year2 = alt.selection_single(name="YEAR", fields=['YEAR'],
                                   bind=slider2, init={'YEAR': 2000})


## NSCM - Non Contaminated VS Safely Managed
NCSM = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('SAFELY_MANAGED_NAT'),
    y = alt.Y('NON_CONTAMIN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    select_year2
).add_selection(
    select_year2
).properties(
    title="Safely Managed Non Contaminated Drinking Water",
    width = 300,
    height = 300
)
## NCNP Non Contaminated VS NON Piped
NCNP = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('NONPIPED_NAT'),
    y = alt.Y('NON_CONTAMIN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    select_year2
).add_selection(
    select_year2
).properties(
    title="Non Piped Access to Non Contaminated Drinking Water",
    width = 300,
    height = 300,
)
## NCP Non Contaminated VS Piped
NCP = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('PIPED_NAT',),
    y = alt.Y('NON_CONTAMIN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    select_year2
).add_selection(
    select_year2
).properties(
    title="Piped Access to Non Contaminated Drinking Water",
    width = 300,
    height = 300,
)

worldpop = alt.Chart(waterdf).mark_bar().encode(
    x="YEAR:O",
    y=alt.Y("sum(POP_THOUS):Q",scale=alt.Scale(domain=(0,8000000)),axis=alt.Axis(title='World Population (in 1000s)')),
    color=alt.Color('YEAR:N', scale=alt.Scale(scheme='plasma', zero=False)),
    tooltip = 'YEAR'
).transform_filter(
    select_year2
).add_selection(
    select_year2
)

st.write(alt.concat(
    (worldpop | NCSM | NCNP) & NCP
).resolve_scale(
    color='shared'
).configure_view(
    stroke=None
)
)

st.markdown("This project was created by Student1 and Student2 for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
