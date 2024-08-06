import streamlit as st
import plotly.express as px
import pandas as pd
import os 
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Maven Hospital Challenge", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Massachusetts General Hospital (MGH)")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\user\Desktop\Maven Hospital Challenge\Hospital_Patient_Records")
    df = pd.read_csv("encounters.csv")
    df2 = pd.read_csv('encounters.csv')
    df3 = pd.read_csv('organizations.csv')
    df4 = pd.read_csv('patients.csv')
    df5 = pd.read_csv('payers.csv')
    df6 = pd.read_csv('procedures.csv')

col1, col2 = st.columns((2))


# Getting the start and the end date
startDate = pd.to_datetime(df2['START'], format = '%Y-%m-%dT%H:%M:%SZ').min()
endDate = pd.to_datetime(df2['STOP'], format = '%Y-%m-%dT%H:%M:%SZ').max()

# converting start and end date to datetime
df2['START'] = pd.to_datetime(df2['START'], format = '%Y-%m-%dT%H:%M:%SZ')
df2['STOP'] = pd.to_datetime(df2['STOP'], format = '%Y-%m-%dT%H:%M:%SZ')

df6['START'] = pd.to_datetime(df6['START'], format = '%Y-%m-%dT%H:%M:%SZ')
df6['STOP'] = pd.to_datetime(df6['STOP'], format = '%Y-%m-%dT%H:%M:%SZ')


with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df2 = df2[(df2['START'] >= date1) & (df2['STOP'] <= date2)].copy()
df6 = df6[(df6['START'] >= date1) & (df6['STOP'] <= date2)].copy()


st.sidebar.header("Choose your filter: ")

# Create for State
state = st.sidebar.multiselect("Pick your State", df4["STATE"].unique())
if not state:
    df21 = df2.copy()
    df61 = df6.copy()
    
else:
    df21 = df2[df2['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id'])]
    df61 = df6[df6['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id'])]
    

# Create for County
county = st.sidebar.multiselect("Pick the County", df4["COUNTY"].unique())
if not county:
    df23 = df21.copy()
    df63 = df61.copy()
    
else:
    df23 = df2[df2['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id'])]
    df63 = df6[df6['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id'])]
    

#create for City
city = st.sidebar.multiselect("Pick the City", df4["CITY"].unique())

#Filter the data based on Region, State and City

if not county and not state and not city:
    filtered_df2 = df2
    filtered_df6 = df6
   
elif not state and not city:
    filtered_df2 = df2[df2['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id'])]
    filtered_df6 = df6[df6['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id'])]
   
elif not county and not city:

    filtered_df2 = df2[df2['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id'])]
    filtered_df6 = df6[df6['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id'])]
elif state and city:
    
    filtered_df2 = df23[df2['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) & df23['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]
    filtered_df6 = df63[df6['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) & df63['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]
elif county and city:
    filtered_df2 = df23[df2['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df23['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]
    filtered_df6 = df63[df6['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df63['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]
elif county and state:
    filtered_df2 = df23[df2['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df23['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) ]
    filtered_df6 = df63[df6['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df63['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) ]
elif city:
    filtered_df2 = df23[df23["City"].isin(city)]
    filtered_df6 = df63[df63["City"].isin(city)]
else:
    filtered_df2 = df23[df2['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df23['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) & df23['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]
    filtered_df6 = df63[df6['PATIENT'].isin(df4[df4["COUNTY"].isin(county)]['Id']) & df63['PATIENT'].isin(df4[df4["STATE"].isin(state)]['Id']) & df63['PATIENT'].isin(df4[df4["CITY"].isin(city)]['Id']) ]


top_5_encounter = filtered_df2.groupby('DESCRIPTION')['TOTAL_CLAIM_COST'].sum().reset_index(name = 'Revenue').sort_values(by = 'Revenue', ascending = False)[:5]
description_counts = filtered_df2[filtered_df2["DESCRIPTION"].isin(top_5_encounter["DESCRIPTION"])].groupby('DESCRIPTION').size().reset_index(name = 'Occurence')
top_5_encounter = pd.merge(top_5_encounter, description_counts, on = 'DESCRIPTION', how = 'left')
top_5_procedure = filtered_df6.groupby('DESCRIPTION')['BASE_COST'].sum().reset_index(name = 'Revenue').sort_values(by = 'Revenue', ascending = False)[:5]
description_counts = filtered_df6[filtered_df6["DESCRIPTION"].isin(top_5_procedure["DESCRIPTION"])].groupby('DESCRIPTION').size().reset_index(name = 'Occurence')
top_5_procedure = pd.merge(top_5_procedure, description_counts, on = 'DESCRIPTION', how = 'left')



st.subheader("Top 5 Revenue Generating Encounter")
fig = px.bar(top_5_encounter, x = "DESCRIPTION", y = "Revenue", text = ['{} Occurrence'.format(x) for x in top_5_encounter['Occurence']],
                template = "presentation", labels = {'DESCRIPTION': "Description"})
fig = px.scatter(top_5_encounter, x = 'DESCRIPTION', y= 'Revenue', size = 'Occurence', template = 'gridon')
fig['layout'].update(xaxis = dict(title = "Description", titlefont = dict(size = 19)), 
                                   yaxis = dict(title = "Revenue", titlefont = dict(size=19)))

st.plotly_chart(fig,use_container_width=True, height = 400)

with st.expander("Top_5_Encounter_ViewData"):
    st.write(top_5_encounter.style.background_gradient(cmap="Blues"))
    csv = top_5_encounter.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "top_5_encounter.csv", mime = "text/csv",
                       help = 'Click here to download the data as a CSV file')
    

st.subheader("Top 5 Revenue Generating Procedure")
fig = px.bar(top_5_procedure, x = "DESCRIPTION", y = "Revenue", text = ['{} Occurence'.format(x) for x in top_5_procedure['Occurence']],
                template = "plotly", labels = {'DESCRIPTION': 'Description'})
st.plotly_chart(fig,use_container_width=True, height = 400)
with st.expander("Top_5_Procedure_ViewData"):
    st.write(top_5_procedure.style.background_gradient(cmap="Oranges"))
    csv = top_5_procedure.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "top_5_procedure", mime = "csv/text",
                       help = "Click here to download the data as a CSV file")


# Procedures covered by insurance

## Note
# The same procedure can have different BASE_COST based on different occurrence
# One Encounter can have many procedures
# Important fields Encounters('Id', 'BASE_ENCOUNTER_COST', 'TOTAL_CLAIM_COST', 'PAYER_COVERAGE')
# Important fields Procedures('ENCOUNTER', 'BASE_COST')

# filter procedures dataframe (df6) by keyword 'procedure'
df6_filtered = filtered_df6[filtered_df6["DESCRIPTION"].str.contains('procedure', case=False, regex = True)].sort_values(by = "DESCRIPTION", ascending = True)
# 32575 rows contains 'procedure'
#len(df6_filtered)

# group df6 by ENCOUNTER field and sum the BASE_COST
df6_grouped_foreign_key = df6_filtered.groupby("ENCOUNTER")["BASE_COST"].sum().reset_index(name = 'TOTAL_PROCEDURE_COST').sort_values(by = "ENCOUNTER", ascending = True).reset_index(drop = True)
# 9531 rows of ENCOUNTER dataframe Id(s)
#df6_grouped_foreign_key

#filter encounters dataframe(df2) for the 9531 Id(s)
df2_filtered = filtered_df2[filtered_df2["Id"].isin(df6_grouped_foreign_key["ENCOUNTER"])]
df2_filtered = df2_filtered.sort_values(by = "Id", ascending = True).reset_index(drop = True)


#check PROCEDURE('TOTAL_PROCEDURE_COST') that is covered by ENCOUNTER('PAYER_COVERAGE')
# 815 encounters covered
df2_filtered = df2_filtered[df2_filtered["PAYER_COVERAGE"] >= df6_grouped_foreign_key["TOTAL_PROCEDURE_COST"]]


#search the 815 foreign keys inside df6_filtered
df6_filtered_covered = df6_filtered[df6_filtered["ENCOUNTER"].isin(df2_filtered["Id"])]
# 2340 procedures covered by insurance
covered_by_insurance = len(df6_filtered_covered)
not_covered_by_insurance = 32575-covered_by_insurance
covered_total_base_cost = df6_filtered_covered["BASE_COST"].sum()
not_covered_total_base_cost = df6_filtered["BASE_COST"].sum() - covered_total_base_cost
data_df = pd.DataFrame({'Type':['Insurance Covered','Not Covered'],
                        'Revenue':[covered_total_base_cost,not_covered_total_base_cost],
                        'Occurence':[covered_by_insurance,not_covered_by_insurance]})

st.subheader("Procedures That are Covered by Insurance and Revenue Generated")
fig = px.pie(data_df, values = "Occurence", names = "Type", hole = 0.5, template = 'simple_white')
fig.update_traces( text = data_df["Revenue"].apply(lambda x: '${:,.2f}'.format(x)), textposition = "outside")
st.plotly_chart(fig, uses_container_width = True)
with st.expander("Procedures_Covered_Insurance_ViewData"):
    st.write(data_df.style.background_gradient(cmap = "Blues"))
    csv = data_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "procedures_covered_insurance.csv", mime = "csv/text",
                       help = "Click here to download the data as a csv file")

# Encounter by encounter class and the revenue generated
# can use pie chart
df2_filtered = filtered_df2.groupby("ENCOUNTERCLASS")["TOTAL_CLAIM_COST"].sum().reset_index(name = 'Revenue')
encounter_class_count = filtered_df2.groupby("ENCOUNTERCLASS").size().reset_index(name = 'Occurence')
df2_filtered = pd.merge(df2_filtered,encounter_class_count, on = 'ENCOUNTERCLASS',how = 'left' )
st.subheader('Encounter Class and the Revenue Generated')
fig = px.pie(df2_filtered, values = "Occurence", names = "ENCOUNTERCLASS", hole = 0.5, template = 'plotly_dark', labels = {"ENCOUNTERCLASS":"Encounter Class"})
fig.update_traces( text = df2_filtered['Revenue'].apply(lambda x: "${:,.2f}".format(x)), textposition = "outside")
st.plotly_chart(fig, uses_container_width = True)
with st.expander("Encounter_Class_ViewData"):
    st.write(df2_filtered.style.background_gradient(cmap = "Oranges"))
    csv = df2_filtered.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "encounter_class.csv", mime = "csv/text",
                       help = "Click here to download the data as a csv file")

# Average Cost Per Visit

## Note
# Important field encounter('BASE_ENCOUNTER_COST')
# How to solve
# step 1: Just find the mean of BASE_ENCOUNTER_COST? is it that easy?
#       - can try to find desc that have 'visit' in it? only 1873 instances found. Not logical to pick only those

st.subheader('Average Cost Per Visit')
average_cost = df2['BASE_ENCOUNTER_COST'].mean()
fig = px.line(filtered_df2, x = 'Id', y = 'BASE_ENCOUNTER_COST', labels = {'BASE_ENCOUNTER_COST':'Revenue', 'Id':'Encounter'}, height = 500, width = 1000, template = 'presentation' )

fig.add_hline(y = average_cost, line_dash = "dash", line_color = "red",
              annotation_text = f"Average Cost: ${average_cost:.2f}",
               annotation_position = "top left", annotation_font = dict(color = 'black') )
fig.update_xaxes(showticklabels = False)
st.plotly_chart(fig, uses_container_width = True)


# Average Patients Staying time

## Note
# Important fields encounter('START','STOP', 'PATIENT')
# How to solve:
# step 1: calculate the different between start time and stop time
#         - check the format of the time.
#         - should we include the patients that were readmitted? Yes we should because they occupied the facility regardless of how many time
#         - so average of 27791 admissions time range

# step 2: Sum and average all

# calculate difference between start time and stop time
df2_filtered = filtered_df2.groupby(['PATIENT','START','STOP']).size().reset_index(name = "Count").sort_values(by = "Count", ascending = False)
#27791 admissions
# df2_filtered

df2_filtered['START'] = pd.to_datetime(df2_filtered['START'], format = '%Y-%m-%dT%H:%M:%SZ')
df2_filtered['STOP'] = pd.to_datetime(df2_filtered['STOP'], format = '%Y-%m-%dT%H:%M:%SZ')
df2_filtered['DURATION'] = (df2_filtered['STOP'] - df2_filtered['START']).dt.total_seconds() / 3600 # in hours

#Sum and Average
average_staying_time = df2_filtered['DURATION'].mean() # average of 27791 admissions time range
st.subheader('Average Patient Staying Time')
fig = px.line(df2_filtered, x = 'PATIENT', y = 'DURATION', labels = {'PATIENT':'Patient', 'DURATION':'Duration'}, height = 500, width = 1000, template = 'gridon')
fig.add_hline(y = average_staying_time, line_dash = "dash", line_color = "red",
              annotation_text = '{} Hours'.format(average_staying_time), annotation_position = "top left",
              annotation_font = dict(color = 'black'))
fig.update_xaxes(showticklabels = False)
st.plotly_chart(fig, uses_container_width = True)


# patients that were admitted and readmitted overtime

## Note
# Important field encounters('START','STOP',PATIENT')
# how to solve
# step 1: find the duplicated patient key inside encounters dataframe
#         - how about group patient key with the time start and stop? result: 27791 rows, what does that mean? it means 27791 patients were admitted (could be the same patients multiple time)

# try to group patient key with time start and time stop (it means a patient could undergo multiple encounters at the same time frame)
df2_filtered = filtered_df2.groupby(['PATIENT','START','STOP']).size().reset_index(name = "Count").sort_values(by = "Count", ascending = False)
#27791 admissions
# df2_filtered

# further grouped patient key with different timeframe in df2_filtered
df2_filtered_admitted = df2_filtered.groupby("PATIENT").size().reset_index(name = "Count").sort_values(by = "Count", ascending = False)
#974 rows (number of patients admitted)
# df2_filtered

# filter admitted count that's > 1
df2_filtered_readmitted = df2_filtered_admitted[df2_filtered_admitted['Count'] > 1]
#854 patients readmitted
# df2_filtered

st.subheader('Patients that Were Admitted and Readmitted overtime')
data_df = pd.DataFrame({'Type':['Total Admitted', 'Readmitted'],
                        'Occurence': [len(df2_filtered_admitted),len(df2_filtered_readmitted)]})
fig = px.bar(data_df, x = 'Type', y = 'Occurence', text = data_df["Occurence"], template = 'presentation')
st.plotly_chart(fig, uses_container_width = True)
with st.expander("Patient_Admitted_Readmitted_ViewData"):
    st.write(data_df.style.background_gradient(cmap = "Blues"))
    csv = data_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Patient_Admitted_Readmitted.csv", mime = "csv/text",
                       help = "Click here to download the data as a csv file")

# Gender, Race and Revenue Generated
df2_filtered = df2.groupby('PATIENT', as_index = False)["TOTAL_CLAIM_COST"].sum()
df2_filtered.columns= ['Id','TOTAL_CLAIM_COST']


df4_filtered = pd.merge(df2_filtered,df4, on = 'Id', how = 'left')

df4_filtered_size = df4_filtered.groupby(['GENDER','RACE']).size().reset_index(name = 'Count')
df4_filtered_revenue = df4_filtered.groupby(['GENDER','RACE'])["TOTAL_CLAIM_COST"].sum().reset_index(name = 'Revenue')
df4_filtered = pd.merge(df4_filtered_size, df4_filtered_revenue, on =['GENDER','RACE'], how = 'left')
st.subheader('Gender, Race, and Revenue Generated')
fig = px.bar(df4_filtered, x = 'RACE', y = 'Revenue', color = 'GENDER', text = df4_filtered['Count'],
                labels = {'RACE':'Race', 'GENDER':'Gender'}, template = 'presentation')
fig.update_layout(barmode = 'stack')
st.plotly_chart(fig, uses_container_width = True)
with st.expander("Gender_Race_Revenue_ViewData"):
    st.write(df4_filtered.style.background_gradient(cmap = "Oranges"))
    csv = df4_filtered.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Gender_Race_Revenue.csv", mime = "csv/text",
                       help = "Click here to download the data as a csv file")
    