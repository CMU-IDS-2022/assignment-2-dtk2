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
st.write("United Nations has gloabally designed several Sustainable Developement Goals(SDGs) as actions to end poverty, protect the planet and ensure peace and prosperity for human beings. SDGs are the extensions of Millenium Developement Goals(MDGs), which were started in the year 2000 to serve the same purpose. SDG-6 is to ensure availability and safe and sustainable management of water and sanitation for all. This project analyzes overall developement of countries around the world, towards safely managing drinking water and sanitation.")

##WORLD POPULATION SLIDER
st.header("1. Growth in World Population over Time")
st.image('https://unstats.un.org/sdgs/assets/img/sliders/2017-Regions-E-large.png')
st.write("The United Nations categorized the world nations in Eight Major Regions, viz.,",
         "'Sub-Saharan Africa', 'Northern & Western Africa', 'Central & Southern Asia', 'Eastern & South-Eastern Asia'",
         ", 'Latin America & the Caribbean', 'Australia & New-Zealand','Oceania', and 'Europe & Northern America'.")

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
st.write("The world population grew exponentially from around 6 Billion in 2000 to about 8 Billion by 2020! This steep rise in population put great stress on the world economies to ensuring clean potable drinking water and safe sanitation to each and every human being on the planet. Population is an important and consistently growing parameter on which, developement of any nation largely depends. This section shows a pair of histograms depicting population growth in different countries and different SDG Regions in the the world between from the year 2000 to 2020. ")
st.write("**Interactivity Guide:** Move the slider, hover on the bars to view more details...")
st.subheader("***🔑 Key Insight***")
st.write("*Notice the steep 30% increase in India's population. Compare it with China's and USA's population over the past 20 years!*")

## PART A - CLEAN WATER
st.header("2. Drinking Water")

## THE WATER CORRELATION MATRIX
st.write("The data obtained has 10 different parameters [Link to Variable Dictionary](https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-dtk2/f367084a4fef6684455252465e3bd7f6e9ae9a67/Dictionary%20-%20water.csv). To visualize the correlation (connection) between these parameters, a correlation matrix is plotted. Many parameters show strong correlation among themselves.")

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
st.write("The SDG is to ensure clean drinking water, hence the most important parameter is 'Non Contaminated Water', which shows significantly high (80%) correlation with the 'Piped Water'. This indicates that as the piped water networks increase, the delivery of non-contaminated water increases.")

## CLASSIFICATION OF DRINKING WATER INFRASTRUCTURE/ METHODS
st.header("2.1. Classification of Drinking Water Infrastructure/ Methods")
st.write("From ancient ground/surface water withdrawl to modern pipe networks, methods of access to drinking water are developing continuously. The scatter plot in this section shows increase in population of different countries having access to safe/purified piped water through 20 years. The different dot sizes depict population of a country. ")
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
st.write("**Interactivity Guide:** Hover/ Click the 'Country' beads to see the pie change adaptively for the selected Country and Year. To deselect click on whitespace...")
st.write("As we hover over the graph, the tooltip (cursor) shows name of the country of a particular data point. Single Selection which acts as a dynamic query filter, enables user to click on any point and disaply its details on-demand in the form of a pie chart, alongside. The pie chart shows the accessability to Basic, Limited, Unimproved or Surface water in each country. This gives overall idea of the country's water infrastructure.")
st.subheader("***🔑 Key Insight***")
st.write("*Notice how China enhances delivery of drinking water to 80% of its people with Piped Water Connections in 2020 from a 50% in 2000. India clearly needs to improve its delivery through piped water connectivity. This is a clear indication why the Indian Government started heavily investing in schemes like 'Jal Jeevan Mission' (https://jaljeevanmission.gov.in/) that envisions to provide safe and adequate drinking water through individual household tap connections by 2024 to all households in rural India.*")


## PERFORMANCE OF COUNTRIES IN DELIVERING NONCONTAMINATED DRINKING WATER
st.header("2.2. Performance by Nations in Delivering Non-contaminated, Safe Drinking Water to its Citizens")
st.write("As the goal of the SDG is to provide clean/safe drinking water to all, the scatter plots are created to show World Population vs. Safely Managed Water, Non-Contaminated vs. Non-Piped Water, and Non-Contaminated vs. Piped Water. The different dot sizes depict population of a country. The Slider of Years, help dynamically compare the progress of different nations over the time. ")
slider2 = alt.binding_range(min=2000, max=2020, step=1, name='Select year:')
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
## NCAWN Non Contaminated VS Availability When Needed
NCP = alt.Chart(waterdf).mark_circle(opacity=0.9).encode(  
    x = alt.X('AVAIL_WHEN_NEEDED_NAT',),
    y = alt.Y('NON_CONTAMIN_NAT'),
    color=alt.Color('SDG region:O',scale=alt.Scale(scheme='plasma')),
    size='POP_THOUS:Q',
    tooltip=('COUNTRY', 'SDG region')
).transform_filter(
    select_year2
).add_selection(
    select_year2
).properties(
    title="Availability of Non Contaminated Drinking Water When Needed",
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
st.write("**Interactivity Guide:** Move the slider to and fro to visualize. Hover on the circles to identify the country.")
st.write("For most of the countries, the parameters in all the three graphs show clear relation. Non-Contaminated water increases as the Safe management of water increases. Non-piped water increases/decreases, Non-contaminated water decreases/increases. Non-contaminated water increases as Pipe water increases.")
st.subheader("***🔑 Key Insight***")
st.write("*While most of the countries in the World are improving their water infrastructure systems, these charts help us identify the countries with poor development or the ones that need drastic positive changes. Notice Pakistan (near (x=40,y=40)) moving in opposite direction as compared to the rest of world indicating it has failed to provide any improvement in delivering non-contaminated safely managed clean drinking water to its citizens. The lower left chart shows Pakistan, Nigeria, and Ethiopia witnessed increase in proportion of its people having non-piped access to fairly contaminated drinking water. The lower right chart shows that Ethiopia and Nigeria ensured improvement in availability of water when its needed to its citizens but the quality of water fairly contaminated, whereas Pakistan couldn't ensure any development in both the parameters.*")



#########################################################################################################################    
    
## PART B - SANITATION 
st.header("3. Sanitation")
## THE SANITATION CORRELATION MATRIX
st.write("Sanitatary waste-water systems have been a tremendously neglected infrastructure, especially in the developing and under-developed countries. The data obtained has 11 different parameters [Link to Variable Dictionary](https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-dtk2/f367084a4fef6684455252465e3bd7f6e9ae9a67/Dictionary%20-%20sanitary.csv). To visualize the correlation (connection) between these parameters, a correlation matrix is plotted. A couple of parameters show strong correlation among themselves.")
 
sanit_cor_data = (sanitdf[['BASIC_SAN_NAT', 	'LIMITED_SHARED_SAN_NAT', 	'UNIMPROVED_SAN_NAT', 	'OPENDEFECATION_SAN_NAT', 	'SAFELYMANAGED_SAN_NAT', 	'DISPOSED_INSITU_SAN_NAT', 	'EMP_TREAT_SAN_NAT', 	
                    'WW_TREATED_SAN_NAT', 	'LATRINES_SAN_NAT', 	'SEPTICTANKS_SAN_NAT', 'SEWERCONNECTION_SAN_NAT']]
            ).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'})
sanit_cor_data['correlation_label'] = sanit_cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
s_base = alt.Chart(sanit_cor_data).encode(
    x='variable2:O',
    y='variable1:O'    
)

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
    width=700,
    height=500,
    title = "The Correlation Matrix: Sanitation"
)
st.write(sanit_cor_plot + text)
st.caption("Correlation Matrix for Sanitation Feature Data")
st.write("The SDG is to ensure safe management of sanitary waste, hence the most important parameter is 'Safely Managed Sanitary SYstem', which shows significantly high (91%) correlation with the 'Sewer Connection'. This indicates that as the Connections to Sewer Networks increase, the Safe Management of Sewer Waste increases.")

## CLASSIFICATION OF SANITATION SEWERAGE INFRASTRUCTURE/ METHODS
st.header("3.1. Classification of Sewerage Infrastructure/ Methods")
st.write("Although Open-defecation is extremely unhygenic, a large number of world-population rely on it. However, the situation is slowly changing. Most of the countries have underground and safe sewer-systems on their developement agenda. The scatter-plot in this section shows increase in population having Sewerage Connection, over 20 years. The different dot sizes depict population of a country. As we hover over the graph, the tooltip (cursor) shows name of the country of a particular data point. Single Selection which acts as a dynamic query filter, enables user to click on any point and disaply its details on-demand in the form of a pie chart, alongside.")

s_selection = alt.selection_single(fields=['YEAR','COUNTRY'])
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
     title="Increase in Underground Sewerage Over Time",
     width=400
)
s_nationpie = alt.Chart(sanitpie_melt).mark_arc().encode(
    theta=alt.Theta(field='mean_value', type="quantitative"),
    color=alt.Color('variable', scale=alt.Scale(scheme='plasma')),
    tooltip=('variable:O', 'mean_value:Q')
).transform_filter(
    s_selection
).transform_aggregate(
    mean_value='mean(value):Q',
    groupby=["variable"]
).properties(
    title="Disposal Method of Sanitary Waste"
)
st.write(alt.hconcat(
    sewerconnectionchart , s_nationpie
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
))
st.caption("Increase in Underground Sewerage (left) and Type of Disposal of Sanitary Waste (right) (Interactive)")
st.write("**Interactivity Guide:** Hover/ Click the 'Country' beads to see the pie change adaptively for the selected Country and Year. To deselect click on whitespace...")
st.write("The pie chart shows classification of Sewerage Infrastructure in Basic, imited-shared, Unimproved Sanition and Open defecation. It gives over-all idea of the country's sewerage infrastructure and availability of safely managed sewerage systems. Most of the countries show significant improvement in 20 years.")
st.subheader("***🔑 Key Insight***")
st.write("*China's impressive development in connecting its cities to underground sewerage systems. Notice that India needs to make massive investments in improving its sewerage infrastructure. Notice that India reduces the percentage of open defecation from 74% in 2000 to 15% in 2020!*")





## PERFORMANCE OF COUNTRIES IN DELIVERING NONCONTAMINATED DRINKING WATER
st.header("3.2. Performance by Nations in Safe Collection and Disposal of Sanitary Wastewater from its Citizens")
st.write("SDGs aim to irradicate open defecation and provide safely managed sewerage infrastructure to the people. This section contains scatter plots showing Treated Waste-Water vs. Safely Managed Sanitary System. As their names suggest, these are interdependent and most of the countries show relative progress in these two parameters. The scatter-plot of Treated Waste-Water vs. Open-defecation shows that irradicating open-defecation is a slow yet continuously progresssing process. ")
s_slider = alt.binding_range(min=2000, max=2020, step=1, name='Select year:')
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
).properties(
    title="Safely Managed and Treated Wastewater",
    width=500,
    height=250)
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
).properties(
    title="Wastewater Treatment vs. Open Defecation",
    width=250,
    height=250)
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
).properties(
    title="Wastewater Treatment vs. Sewerage Connectivity",
    width=250,
    height=250)

s_worldpop = alt.Chart(sanitdf).mark_bar().encode(
    x="YEAR:O",
    y=alt.Y("sum(POP_THOUS):Q",scale=alt.Scale(domain=(0,8000000)),axis=alt.Axis(title='World Population (in 1000s)')),
    color=alt.Color('YEAR:N', scale=alt.Scale(scheme='plasma', zero=False)),
    tooltip = 'YEAR'
).transform_filter(
    s_select_year
).add_selection(
    s_select_year
).properties(
    height=250)

st.write(alt.concat(
    (s_worldpop | WTSF) & (WTOD | WTSC)
).resolve_scale(
    color='shared'
).configure_view(
    stroke=None
))
st.caption("Performance by Nations in Safe Collection and Disposal of Sanitary Wastewater(Interactive)")
st.write("**Interactivity Guide:** Move the slider to and fro to visualize.")  
st.write("Waste-water can be treated only when it is connected to a sewer system, is collected and carried to a treatment plant. The third scatter plot in this section, Treated Waste-Water vs. Sewer Connections show almost direct relation for most of the countries. The different dot sizes depict population of a country. The Slider of Years, help dynamically compare the progress of different nations over the time. For most of the countries, the parameters in all the three graphs show clear relation.")
st.subheader("***🔑 Key Insight***")
st.write("*These charts help us identify the countries with poor development or the ones that need drastic positive changes. In the upper chart notice that on one hand India seems to struggle in treating wastewater but also shows drastic improvement in safely managing the waterwater. The lower two charts help us understand why! Observe the lower two charts carefully, India reduces open defecation but there is almost no increase in proportional treatment of wastewater. This is primarily because India conventionally has decentralized sanitation, meaning the absence of a centralized sanitary wastewater collection and treatment infrastructure. It ensures the reduction in open defecation essentially by having in-situ septic tanks which are not connected to a centralized underground wastewater network infrastructure.*")



st.markdown("***Data Source:** WHO-UNICEF JOINT MONITORING PROGRAM [Webpage](https://washdata.org/how-we-work/sdg-monitoring).*")
st.markdown("This project was created by [Tanay Kulkarni](https://www.linkedin.com/in/tanaykulkarni/) and [Devashri Karve](https://www.linkedin.com/in/devashrikarve/) for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
