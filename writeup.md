# United Nations' Sustainable Development Goal 6: Clean Water and Sanitation

![image](https://user-images.githubusercontent.com/98185275/155863655-ae677235-9eee-4ce5-860c-581fa1dbb03b.png)

## Team
Tanay Kulkarni and Devashri Karve are graduate students at the Department of Civil and Environmental Engineering at CMU. They both are the founders of DTK Hydronet Solutions (www.dtkhydronet.com) - a startup that focuses on developing digital solutions around water infrastructure systems.

## Motivation
United Nations has gloabally designed several Sustainable Developement Goals(SDGs) as actions to end poverty, protect the planet and ensure peace and prosperity for human beings. SDGs are the extensions of Millenium Developement Goals(MDGs), which were started in the year 2000 to serve the same purpose. SDG-6 is to ensure availability of safely and sustainably managed drinking water and sanitation to all. This project analyzes overall developement of countries around the world, towards safely managing drinking water and sanitation. 

## Project Goals
This goals of this project are:
- Exploratory analysis of different aspects and parameters that govern safety in drinking water and sanitation.
- Analysis of developement in managing drinking water and sanitation in the world, over past 20 years.
- Correlational Exploratory Visualization of several important features to understand a trend and direction in which the world nations are headed.


## Design

- **Section 1 Growth in World Population over Time:** Population is an important and consistently growing parameter on which, developement of any nation largely depends. This section shows a pair of histograms showing population growth in different countries and different SDG Regions in the the world between from the year 2000 to 2020. The color scheme is based on population of countries. **Hovering** the cursor on bars displays the Name, SDG Region and Population of a country. To visualize data for various years, we tried drop-down list and radio-buttons, however, we used **sliders** as it helps understand(visualize) the changes over the years, smoothly and dynamically.

 
- **Section 2 Drinking Water:** The data has 10 different parameters. To visualize the correlation (connection) between these parameters, a correlation matrix is plotted. Many parameters show strong correlation among themselves. The SDG is to ensure clean drinking water, hence the most important parameter is 'Non Contaminated Water', which shows significantly high (80%) correlation with the 'Piped Water'. This indicates that as the piped water networks increase, the delivery of non-contaminated water increases. 


- **Section 2.1 Classification of Drinking Water Infrastructure/ Methods:** From ancient ground/surface water withdrawl to modern pipe networks, methods of access to drinking water are developing continuously. The scatter plot in this section shows increase in population of different countries having access to safe/purified piped water through 20 years. The different dot sizes depict population of a country. As we hover over the beads in the graph, the **Tooltip (cursor)** shows name of the country of a particular data point. **Single Selection** which acts as a dynamic query filter, enables user to click on any point and disaply its details on-demand in the form of a pie chart, alongside. The pie chart shows the accessability to Basic, Limited, Unimproved or Surface water in each country. This gives overall idea of the country's water infrastructure. 
- ![image](https://user-images.githubusercontent.com/98185275/156105796-54e44a8d-a499-47d5-b0ff-a46bad405a4c.png)

- **Section 2.2 Performance by Nations in Delivering Non-contaminated, Safe Drinking Water to its Citizens:** As the goal of the SDG is to provide clean/safe drinking water to all, the scatter plots are created to show **World Population** and **Non_Contaminated Water** vs. **Safely Managed Water**, **Non-Contaminated vs. Non-Piped Water**, and **Non-Contaminated vs. Water Availability when needed**. The different dot sizes depict population of a country. The **Slider** of Years, help dynamically compare the progress of different nations over the time. For most of the countries, the parameters in all the three graphs show clear relation. Non-Contaminated water increases as the Safe management of water increases. However, there is downfall in safe management of water, for some countires. Non-piped water increases/decreases, Non-contaminated water decreases/increases. Non-contaminated water increases as Pipe water increases.

- **Section 3 Sanitation:** Sanitatary waste-water systems have been a tremendously neglected infrastructure, especially in the developing and under-developed countries. The data obtained has 11 different parameters. To visualize the correlation (connection) between these parameters, a correlation matrix is plotted. A couple of parameters show strong correlation among themselves. The SDG is to ensure safe management of sanitary waste, hence the most important parameter is 'Safely Managed Sanitary SYstem', which shows significantly high (91%) correlation with the 'Sewer Connection'. This indicates that as the Connections to Sewer Networks increase, the Safe Management of Sewer Waste increases.

- **Section 3.1 Classification of Sewerage Infrastructure/ Methods:** Although Open-defecation is extremely unhygenic, a large number of world-population rely on it. However, the situation is slowly changing. Most of the countries have underground and safe sewer-systems on their developement agenda. The scatter-plot in this section shows increase in population having Sewerage Connection, over 20 years. The different dot sizes depict population of a country. As we hover over the graph, the **tooltip (cursor)** shows name of the country of a particular data point. **Single Selection** which acts as a dynamic query filter, enables user to click on any point and disaply its details on-demand in the form of a pie chart, alongside. The pie chart shows classification of Sewerage Infrastructure in Basic, imited-shared, Unimproved Sanition and Open defecation. It gives over-all idea of the country's sewerage infrastructure and availability of safely managed sewerage systems. Most of the countries show significant improvement in 20 years.
- ![image](https://user-images.githubusercontent.com/98185275/156108059-c444f574-0209-4013-8271-ddaa78eeb092.png)


- **Section 3.2 Performance by Nations in Safe Collection and Disposal of Sanitary Wastewater from its Citizens:** SDGs aim to irradicate open defecation and provide safely managed sewerage infrastructure to the people. This section contains scatter plots showing **Treated Waste-Water** vs. **Safely Managed Sanitary System**. As their names suggest, these are interdependent and most of the countries show relative progress in these two parameters. The scatter-plot of **Treated Waste-Water** vs. **Open-defecation** shows that irradicating open-defecation is a slow yet continuously progresssing process. Waste-water can be treated only when it is connected to a sewer system, is collected and carried to a treatment plant. The third scatter plot in this section, **Treated Waste-Water** vs. **Sewer Connections** show almost direct relation for most of the countries. The different dot sizes depict population of a country. The **Slider** of Years, help dynamically compare the progress of different nations over the time. For most of the countries, the parameters in all the three graphs show clear relation.

## Development

- The data is obtained from WHO-UNICEF JOINT MONITORING PROGRAM https://washdata.org/how-we-work/sdg-monitoring as a CSV. The preliminary inspection and understanding the data was carried out in Microsoft Excel. However, the data cleaning (removing NA values, changing data types of variables as per the requirement, etc) and processing was done using Python. 
- We tried sketching and drawing different types of graphs, histograms, pie charts, scatter plots of different data parameters and arrived on a few, which are presented in the app. 
- We both were involved in sketching, data cleaning (using Python), in developing the code and the write-up. It helped us support each other as well as learn many new things together. 
- Overall, this assignment took 20 man-hours each. Total of 40 man-hours.
  Data Collection - 3 hrs
  Data cleaning - 5 hrs
  Sketching - 4 hrs
  Developing the app - 25 hrs
  Write-up - 3
- Out of numerous coding challanges, deploying the app on streamlit and generating the results on it took comparitively more time. Especially, deploying **Slider** was a lengthy process as we encountered most challanges in it. The Year data/graphs did not show for the sliders in streamlit. Eventually, we leaned that the slider needs 'float' type data, and not 'integer'.

## Success Story

- The app shows dynamic changes in population and many other parameters over the period of 20 years. It helps quickly understand the progress on any/all nation/s. 
- Population histograms show steep 30% in India's Population in 20 years.
- China shows massive success in improving safe management of drinking water, by increasing Pipe Network Infrastructure from 50% in 2000, to 80% in 2020.
- India clearly needs to increase piped water connections to cater safe water to its fast growing population. Beads graph in section 2.1 clarifies why the Indian Government started heavily investing in schemes like 'Jal Jeevan Mission' (https://jaljeevanmission.gov.in/) that envisions to provide safe and adequate drinking water through individual household tap connections by 2024 to all households in rural India.
- It is safe to assume that all the countries are progressing and improving their infrastructure. However, this project helps identify that a few counties viz. Pakistan, Nigeria, Ethiopia witnessed increase in proportion of its people having non-piped access to fairly contaminated drinking water, in 20 years.
- China shows massive development in connecting its cities to underground sewerage systems. However, India also shows impressive progress in diminishing Open Defecation from 745 in 2000 to 15% in 2020, but not proportionate increase in Sewer Connections. On further research, we learned that India conventionally has decentralized sanitation, meaning the absence of a centralized sanitary wastewater collection and treatment infrastructure. It ensures the reduction in open defecation essentially by having in-situ septic tanks which are not connected to a centralized underground wastewater network infrastructure. 

