#IMPORTING LIBRARIES
import pandas as pd
pd.set_option('display.max_columns', None)
import altair as alt
import streamlit as st
alt.data_transformers.disable_max_rows()

#IMPORTING THE DATA
waterdf = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-dtk2/master/water.csv", on_bad_lines='skip', encoding = "ISO-8859-1")
sanitdf = pd.read_csv("https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-dtk2/master/sanitation.csv", on_bad_lines='skip', encoding = "ISO-8859-1")

#INSPECTING THE DATA AND CLEANING OF DATA
#DATA NO.1 : WATER
print(waterdf.shape)
print(waterdf.describe())
print(waterdf.isna().sum())
waterdf = waterdf.dropna(subset=['POP_THOUS'])
print(waterdf.shape)
waterdf.isnull().sum()
waterdf['POP_THOUS'] = waterdf['POP_THOUS'].str.replace(' ', '')
waterdf['POP_THOUS'] = waterdf['POP_THOUS'].astype(int)
waterdf['YEAR_STR'] = waterdf['YEAR'].astype(str)
waterdf['YEAR'] = waterdf['YEAR'].astype(float)
print(waterdf.head())
print(waterdf.describe())
waterpie = waterdf[['COUNTRY','YEAR','YEAR_STR','BASIC_WAT_NAT','LIMITED_WAT_NAT','UNIMPROVED_WAT_NAT','SURFACE_WAT_NAT']]
waterpie_melt = pd.melt(waterpie, id_vars=['COUNTRY','YEAR','YEAR_STR'], value_vars=['BASIC_WAT_NAT','LIMITED_WAT_NAT','UNIMPROVED_WAT_NAT','SURFACE_WAT_NAT'])

#DATA NO.2 : SANITATION
print(sanitdf.shape)
print(sanitdf.describe())
print(sanitdf.isnull().sum())
sanitdf = sanitdf.dropna(subset=['POP_THOUS'])
print(sanitdf.shape)
sanitdf.isnull().sum()
sanitdf['POP_THOUS'] = sanitdf['POP_THOUS'].str.replace(' ', '')
sanitdf['POP_THOUS'] = sanitdf['POP_THOUS'].astype(int)
sanitdf['YEAR'] = sanitdf['YEAR'].astype(float)
sanitdf.head()
sanitpie = sanitdf[['COUNTRY','YEAR','BASIC_SAN_NAT','LIMITED_SHARED_SAN_NAT','UNIMPROVED_SAN_NAT','OPENDEFECATION_SAN_NAT']]
sanitpie_melt = pd.melt(sanitpie, id_vars=['COUNTRY','YEAR'], value_vars=['BASIC_SAN_NAT','LIMITED_SHARED_SAN_NAT','UNIMPROVED_SAN_NAT','OPENDEFECATION_SAN_NAT'])

##TITLE AND INTRO
st.title("UN SDG 6: Clean Water and Sanitation")
st.subheader("An Exploratory Visualization Application to Find Key Insights")
st.image("https://blantyre.dorium.community/uploads/default/optimized/1X/6fc93ea6f54ff0312e52bf977c07f91e35efdf40_2_1035x322.jpeg")
st.write("This is an introduction to the topic")

##WORLD POPULATION SLIDER
st.header("1. Growth in World Population over Time")
st.image('https://unstats.un.org/sdgs/assets/img/sliders/2017-Regions-E-large.png')
st.write("This is an introduction to the topic")
slider1 = alt.binding_range(min=2000, max=2020, step=1, name='Select year:')
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
    width = 400,
    height = 300,
    title="Population (2000-2020): World Nations"
)

popgrowth= alt.concat(
    popsdgchart, popyearchart
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)
st.altair_chart(popgrowth, use_container_width=True)
st.caption("Growth in World's Population over Time (2000-2020) (Interactive)")

## PART A - CLEAN WATER
st.header("2. Clean Water")

## THE WATER CORRELATION MATRIX
st.write("This text introduces the various features and the correlation matrix")

# THE MATRIX
cor_data = (waterdf[['BASIC_WAT_NAT', 	'LIMITED_WAT_NAT', 	'UNIMPROVED_WAT_NAT', 	'SURFACE_WAT_NAT', 	'SAFELY_MANAGED_NAT', 	'ACCESS_ONPREMISE_NAT', 	'AVAIL_WHEN_NEEDED_NAT', 	
                    'NON_CONTAMIN_NAT', 	'PIPED_NAT', 	'NONPIPED_NAT']]
            ).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})
cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal

base = alt.Chart(cor_data).encode(
    x='variable2:O',
    y='variable1:O'    
)

text = base.mark_text().encode(
    text='correlation_label',
    color=alt.condition(
        alt.datum.correlation > 0.1, 
        alt.value('black'),
        alt.value('white')
    )
)

## THE HEATMAP
cor_plot = base.mark_rect().encode(
    color=alt.Color('correlation:Q', scale=alt.Scale(scheme='plasma'))
).properties(
    width=700,
    height=500,
    title="The Correlation Matrix: Drinking Water"
)
st.altair_chart((cor_plot + text))
st.caption("Correlation Matrix for Water Feature Data")


## CLASSIFICATION OF DRINKING WATER INFRASTRUCTURE/ METHODS
st.header("2.1. Classification of Drinking Water Infrastructure/ Methods")
st.write("This text introduces the topic")
selection = alt.selection_single(fields=['YEAR_STR','COUNTRY'])

pipedwaterchart = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(
    x=alt.X('YEAR_STR:O', axis=alt.Axis(title='Year')),
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
nationpie = alt.Chart(waterpie_melt).mark_arc().encode(
    theta=alt.Theta(field='mean_value', type="quantitative"),
    color=alt.Color('variable', scale=alt.Scale(scheme='plasma')),
    tooltip=('variable:O', 'mean_value:Q')
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
st.caption("Increase in Access to Piped Drinking Water (left) and Type of Access to Drinking Water (right) (Interactive)")

## PERFORMANCE OF COUNTRIES IN DELIVERING NONCONTAMINATED DRINKING WATER
st.header("2.2. Performance by Nations in Delivering Non-contaminated, Safe Drinking Water to its Citizens")
st.write("This text introduces the topic")
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
    width = 500,
    height = 250
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
    width = 250,
    height = 250,
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
    width = 250,
    height = 250,
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
).properties(
    height= 250)
st.write(alt.concat(
    (worldpop | NCSM)& (NCNP | NCP)
).resolve_scale(
    color='shared'
).configure_view(
    stroke=None
)
)
st.caption("Performance by Nations in Delivering Safely Managed Drinking Water to its Citizens(Interactive)")
    
#########################################################################################################################    
    
## PART B - SANITATION  
#Correlation Matrix
sanit_cor_data = (sanitdf[['BASIC_SAN_NAT', 	'LIMITED_SHARED_SAN_NAT', 	'UNIMPROVED_SAN_NAT', 	'OPENDEFECATION_SAN_NAT', 	'SAFELYMANAGED_SAN_NAT', 	'DISPOSED_INSITU_SAN_NAT', 	'EMP_TREAT_SAN_NAT', 	
                    'WW_TREATED_SAN_NAT', 	'LATRINES_SAN_NAT', 	'SEPTICTANKS_SAN_NAT', 'SEWERCONNECTION_SAN_NAT']]
            ).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})

sanit_cor_data['correlation_label'] = sanit_cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
#print(cor_data)

s_base = alt.Chart(sanit_cor_data).encode(
    x='variable2:O',
    y='variable1:O'    
)

# Text layer with correlation labels
# Colors are for easier readability
text = s_base.mark_text().encode(
    text='correlation_label',
    color=alt.condition(
        alt.datum.correlation > 0.1, 
        alt.value('black'),
        alt.value('white')
    )
)

# The correlation heatmap
sanit_cor_plot = s_base.mark_rect().encode(
    color=alt.Color('correlation:Q', scale=alt.Scale(scheme='plasma'))
).properties(
    width=500,
    height=500,
    title = "The Correlation Matrix: Sanitation"
)
sanit_cor_plot + text



s_slider = alt.binding_range(min=2000, max=2020, step=1, name='YEAR')
s_select_year = alt.selection_single(name="YEAR", fields=['YEAR'],
                                   bind=s_slider, init={'YEAR': 2000})


s_popsdgchart = alt.Chart(sanitdf).mark_bar(tooltip=True).encode(
    
    y = alt.Y('POP_THOUS',
              axis=alt.Axis(title='Population in Thousands'), sort='-x',
              scale=alt.Scale(domain=(0, 2400000))),
    
    x = alt.X('SDG region:O',
              axis=alt.Axis(title='SDG Regions'), 
              scale=alt.Scale(zero=False), sort='y'
              ),
              
    color= alt.Color('COUNTRY:O', legend = None, scale=alt.Scale(scheme='plasma'))
).properties(
    width = 300,
    height = 400,
     title="Population (2000-2020): SDG Regions"
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
)

s_popyearchart = alt.Chart(sanitdf).mark_bar(tooltip=True).encode(
    
    y = alt.Y('POP_THOUS',
              axis=alt.Axis(title='Population in Thousands'), sort='-x',
              scale=alt.Scale(domain=(0, 1600000))),
                  
    x = alt.X('COUNTRY:O',
              axis=alt.Axis(title='COUNTRY'), 
              scale=alt.Scale(zero=False), sort='-y'
              ),  
    color= alt.Color('COUNTRY', legend = None, scale=alt.Scale(scheme='plasma'))
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
).transform_filter(
    alt.datum.POP_THOUS > 40000
).properties(
    width = 400,
    height = 400,
    title="Population (2000-2020): World Nations"
)
###

alt.concat(
    s_popsdgchart, s_popyearchart
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

s_selection = alt.selection_single(fields=['YEAR','COUNTRY'])

###
sewerconnectionchart = alt.Chart(sanitdf).mark_circle(opacity=0.9).encode(
    x=alt.X('YEAR:O',axis=alt.Axis(title='Year')),
    y=alt.Y('SEWERCONNECTION_SAN_NAT', axis=alt.Axis(title='% Population with Sewerage Connections')),
    size='POP_THOUS',
    #shape='SDG region',
    color = alt.Color('COUNTRY', scale=alt.Scale(scheme='plasma')),
    tooltip='COUNTRY'
).add_selection(s_selection).encode(
    color=alt.condition(s_selection, "COUNTRY", alt.value("grey"), legend=None, scale=alt.Scale(scheme='plasma')),
   ).properties(
     title="Beads Chart: Proportional State of Sewerage Connections",
     width=800
)
###

s_nationpie = alt.Chart(sanitpie_melt).mark_arc().encode(
    theta=alt.Theta(field='mean_value', type="quantitative"),
    color=alt.Color('variable', scale=alt.Scale(scheme='plasma')),
    tooltip=('variable:O', 'mean_value:Q', 'COUNTRY:O', 'YEAR:O')
).transform_filter(
    s_selection
).transform_aggregate(
    mean_value='mean(value):Q',
    groupby=["variable"]
).properties(
    title="Sewerage Connecions"
)

alt.hconcat(
    sewerconnectionchart , s_nationpie
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

s_slider = alt.binding_range(min=2000, max=2020, step=1, name='YEAR')
s_select_year = alt.selection_single(name="YEAR", fields=['YEAR'],
                                   bind=s_slider, init={'YEAR': 2000})
## WTSM WW Treated vs. Safely Managed
WTSF = alt.Chart(sanitdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('SAFELYMANAGED_SAN_NAT'),
    y = alt.Y('WW_TREATED_SAN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
)
## WTOD WW Treated vs. Open Defecation
WTOD = alt.Chart(sanitdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('OPENDEFECATION_SAN_NAT'),
    y = alt.Y('WW_TREATED_SAN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
)
## SWC WW Treated vs. Sewer Connection 
WTSC = alt.Chart(sanitdf).mark_circle(opacity=0.9).encode(
    
    x = alt.X('SEWERCONNECTION_SAN_NAT'),
    y = alt.Y('WW_TREATED_SAN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
)

s_worldpop = alt.Chart(sanitdf).mark_bar().encode(
    x="YEAR:O",
    y=alt.Y("sum(POP_THOUS):Q",scale=alt.Scale(domain=(0,8000000))),
    color=alt.Color('YEAR:N', scale=alt.Scale(scheme='plasma', zero=False)),
    tooltip = 'YEAR'
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
)

alt.hconcat(
    s_worldpop, WTSF , WTOD, WTSC
).resolve_scale(
    color='shared'
).configure_view(
    stroke=None
)

alt.Chart(sanitdf).mark_bar().encode(
    x="YEAR:O",
    y="sum(POP_THOUS):Q",
    color=alt.Color('YEAR', scale=alt.Scale(scheme='plasma')),
    #tooltip = 
)
st.markdown("This project was created by Tanay Kulkarni and Devashri Karve for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
