import streamlit as st
import csv
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cricket Worldcup Dashboard",page_icon="	:cricket_bat_and_ball:",layout="wide")

st.title(body=":orange[Cricket WorldCup Data Visulization Dashboard]")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.sidebar.title(":blue[Cricket Worldcup winner]")
st.sidebar.markdown("---")
with open('Worldcupwinners.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    years = []
    winners = []
    
    csv_reader.__next__()
    
    for row in csv_reader:
        years.append(row[0])
        winners.append(row[2])
        
    col1_side,col2_side = st.sidebar.columns(2)
    col1_side.markdown("<h2 style='font-weight: bold;'>Year</h2>", unsafe_allow_html=True)
    col2_side.markdown("<h2 style='font-weight: bold;'>Winner Team</h2>", unsafe_allow_html=True)
    for year,winner in zip(years,winners):
        col1_side.write(year)
        col2_side.write(winner)
        
#graph ploting using pyplot

col1,col2=st.columns(2)

col1.header("chart of match win by team")

#taking vlaue from the employee
teams=[]
with open("Match_percentage.csv") as file:
    csv_reader = csv.reader(file)
    
    header=csv_reader.__next__()
    
    for row in csv_reader:
        teams.append(row[0])
    
    team_value = col1.selectbox("Select a Value",teams)
    team_data=[]
    file.seek(1)
    
    for row in csv_reader:
        if(team_value==row[0]):
            team_data=row
            break
    
    #pie chart
    pie_team_label=header[3:10]
    pie_team_data=[]
    total=team_data[2]
    for i in range(3,10):
        temp=float(team_data[i])/float(total) *100
        pie_team_data.append(temp)
        
    print(pie_team_data)
    
    fig1, ax = plt.subplots(figsize=(8,6))
    ax.pie(pie_team_data, labels=pie_team_label, autopct='%1.1f%%', startangle=90,labeldistance=1)
    ax.axis('equal')
    ax.set_facecolor('#111')
    fig1.patch.set_facecolor('#262730')
    col1.pyplot(fig1)
    

# col1.markdown("""<div style='background-color:#111'>
              
#               </div>""",unsafe_allow_html=True)

col2.header("Winner list every year")
