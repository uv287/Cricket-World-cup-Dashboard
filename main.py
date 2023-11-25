import streamlit as st
import csv
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Cricket Worldcup Dashboard",page_icon="	:cricket_bat_and_ball:",layout="wide")

st.title(body=":orange[Cricket WorldCup Data Visulization Dashboard]")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.sidebar.title(":blue[Cricket Worldcup winner]")
st.sidebar.markdown("---")

years = []

with open('Worldcupwinners.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
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
with open("Match_percentage.csv") as file1:
    csv_reader = csv.reader(file1)
    
    header=csv_reader.__next__()
    
    for row in csv_reader:
        teams.append(row[0])
    
    team_value = col1.selectbox("Select a Value",teams)
    team_data=[]
    file1.seek(1)
    
    for row in csv_reader:
        if(team_value==row[0]):
            team_data=row
            break
    
    #pie chart
    pie_team_label=[]
    pie_team_data=[]
    total=team_data[2]
    for i in range(3,10):
        temp=float(team_data[i])/float(total) *100
        if(temp!=0.0):
            pie_team_data.append(temp)
            pie_team_label.append(header[i])
    
    fig1, ax = plt.subplots(figsize=(7,4))
    ax.pie(pie_team_data, labels=pie_team_label,shadow=True,wedgeprops={"linewidth": 2, "edgecolor": "#262730"}, startangle=90,labeldistance=1.05,textprops={'color': 'white'})
    ax.axis('equal')
    circle = plt.Circle((0, 0), 0.6, color='#262730')
    ax.add_artist(circle)
    ax.set_facecolor('#111')
    fig1.patch.set_facecolor('#262730')
    col1.pyplot(fig1)
    

# col1.markdown("""<div style='background-color:#111'>
              
#               </div>""",unsafe_allow_html=True)


col2.header("Team Performance in each year")
#we have already teams and the year just want to 

user_year=col2.selectbox("Select Year ",years)

with open("Matches.csv") as file2:
    
    year_data=[]
    #first=win , second = lost , third = no result, fourth=tie
    team_performance=[[0, 0, 0, 0] for _ in range(len(teams))]
    #print(teams)
    #print(team_performance)
    csv_reader=csv.reader(file2)
    
    header=csv_reader.__next__()
    result=["Win","Lost","No Result","Tie"]
    
    for row in csv_reader:
        if(user_year in row[1]):
            year_data.append(row)
            
    for row in year_data:
        team= row[3].split(" v ")
        team1=team[0]
        team2=team[1]
        
        if(team1 in row[-1]):
            win_index=teams.index(team1)
            lost_index=teams.index(team2)
            team_performance[win_index][0]+=1
            team_performance[lost_index][1]+=1
        elif(team2 in row[-1]):
            win_index=teams.index(team2)
            lost_index=teams.index(team1)
            team_performance[win_index][0]+=1
            team_performance[lost_index][1]+=1
        elif(row[-1]=="No result"):
            index1=teams.index(team1)
            index2=teams.index(team2)
            team_performance[index1][2]+=1
            team_performance[index2][2]+=1
        elif(row[-1]=="Match tied"):
            index1=teams.index(team1)
            index2=teams.index(team2)
            team_performance[index1][3]+=1
            team_performance[index2][3]+=1
        
    #print(team_performance)
    
    width=0.3
    multiplier=0
    x = range(len(teams))
    
    fig, ax = plt.subplots(layout='constrained',figsize=(7,4))
    
    for i, r in enumerate(result):
        offset = width * i
        ax.bar([pos + offset for pos in x], [row[i] for row in team_performance], width, label=r,)
    
    ax.set_xticks([pos + (width * len(result)-1.1) for pos in x])
    ax.set_xticklabels(teams,rotation=90)
    ax.legend()
    col2.pyplot(fig)
    

col1,col2 = st.columns(2,gap="medium")

team_value2 = col1.selectbox("Select a Value",teams,key="first")

# Graph 4

year_value3 = col2.selectbox("Select a year",years[6:],key="Second")

df = pd.read_csv("Bowl_"+year_value3+".csv")

top5_values = df.nlargest(5,'W')

st.title('Horizontal Bar Graph for bowlers')

fig, ax = plt.subplots()
ax.barh(top5_values['Player'], top5_values['W'], color='skyblue')
ax.set_xlabel('Wickets')
ax.set_ylabel('Player')
ax.set_title('Horizontal Bar Graph')

# Display the plot using Streamlit
st.pyplot(fig)        

# Graph 4 over

# Graph 5 and 6

col1,col2 = st.columns(2,gap="medium")
    
 # Graph 5    
    
    
    
