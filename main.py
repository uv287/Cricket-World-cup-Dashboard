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
teams=[]
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

col1,col2= st.columns(2,gap="medium")

#Third Graph

col1.header("Highest Runscorer in the Perticular Year")

year3=years[6:]
year3_value = col1.selectbox("Select a Year",year3,key="Third")

filename="Bat_"+year3_value+".csv"

with open(filename) as reader:
    batsman_data=[]
    
    csv_reader=csv.reader(reader)
    
    head=csv_reader.__next__()
    
    for row in csv_reader:
        batsman_data.append(row)
    
    # print(batsman_data[0][4])
    top5_run=[]
    top5_batsman_name=[]
    for i in range(5):
        max=0
        i=0
        j=0
        for btsmn in batsman_data :
            if(int(btsmn[2]) > int(max)):
                max=btsmn[2]
                j=i    
            i=i+1
        top5_run.append(int(batsman_data[j][2]))
        top5_batsman_name.append(batsman_data[j][0])
        batsman_data.remove(batsman_data[j])
        
    print(top5_batsman_name)
    print(top5_run)

   # Plotting the horizontal bar graph
    fig, ax = plt.subplots(figsize=(7,4))
    ax.barh(top5_batsman_name, top5_run, color='skyblue')
    ax.invert_yaxis()
    ax.invert_xaxis()
    
    # Displaying y-labels beside the bars
    for name,run in zip(top5_batsman_name,top5_run):
        dis=name+" : "+str(run)
        ax.text(run, name, str(dis), ha='right', va='center',color="white")
        
    ax.set_facecolor('#262730')
    ax.set_yticklabels([])
    


    ax.set_xlim(800,200)
    col1.pyplot(fig)


# Graph 4

col2.header('Horizontal Bar Graph for bowlers')

year_value3 = col2.selectbox("Select a year",years[6:],key="Second")

df = pd.read_csv("Bowl_"+year_value3+".csv")

top5_values = df.nlargest(5,'W')

fig, ax = plt.subplots(figsize=(7,4))
ax.barh(top5_values['Player'], top5_values['W'], color='skyblue')
ax.set_xlim(10,35)
ax.invert_yaxis()

for name,wickets in zip(top5_values['Player'],top5_values['W']):
        dis=name+" : "+str(wickets)
        ax.text(wickets, name, str(dis), ha='left', va='center',color="white")
        
ax.set_facecolor('#262730')
ax.set_yticklabels([])

# Display the plot using Streamlit
col2.pyplot(fig)        

# Graph 4 over

# Graph 5, 6 and 7

col1,col2,col3,col4=st.columns(4,gap="large")

#col1 to select team

team1 = col1.selectbox("Select First Team : ",teams)

team2 =col1.selectbox("Select Second Team : ",teams)

# team display


#col2 to display the team logo

#col3 to display the total matches
total_matches = 0
t1=0
t2=0
with open("Matches.csv") as matches :
    reader = csv.reader(matches)
    
    for match in reader:
        if(team1 is not None and team2 is not None and team1 != team2 and team1 in match[3] and team2 in match[3]):
            total_matches += 1
            if(team1 in match[4]):
                t1 += 1
            else:
                t2 +=1

col3.markdown(f'''
    <div style="display: inline-flex; align-items: center;">
        <div>
            <div style="width: 150px; height: 40px; display: flex;
                    justify-content: center; align-items: center; color: white; font-size: 20px;padding-top:40px">
                <center>Total Matches</center>
            </div>
            <br>
            <center>
            <div style="width: 100px; height: 100px; border-radius: 50%; background-color:#262730; display: flex;
                        justify-content: center; align-items: center; color: white; font-size: 80px;margin-top:20px">
                <center><h1> {total_matches}</h1></center>
            </div>
            </center>
        </div>
        ''',unsafe_allow_html=True)

col4.markdown(f'''
    <div style="display: inline-flex; align-items: center;">
        <div style="margin-top=0px;">
            <div style="width: 100px; height: 40px; display: flex;
                    justify-content: center; align-items: center; color: white; font-size: 20px;padding-top:0px">
                <center>{team1}</center>
            </div>
            <br>
            <div style="width: 100px; height: 100px; border-radius: 50%; background-color:#262730; display: flex;
                        justify-content: center; align-items: center; color: white; font-size: 80px;padding-top:0px">
                <center><h1> {t1}</h1></center>
            </div>
        </div>
        <div style="padding:100px 50px 0px 30px;width:10px;" ><h2> - <h2></div>
        <div style="margin-top=0px;">
            <div style="width: 100px; height: 40px; display: flex;
                    justify-content: center; align-items: center; color: white; font-size: 20px;padding-top:0px">
                <center>{team2}</center>
            </div>
            <br>
            <div style="width: 100px; height: 100px; border-radius: 50%; background-color: #262730; display: flex;
                        justify-content: center; align-items: center; color: white; font-size: 80px;padding-top:0px">
                <center><h1> {t2}</h1></center>
            </div>
        </div>
    
    </div>
    ''',unsafe_allow_html=True)


col1,col2, col3 = st.columns(3,gap="medium")
 # Graph 5    

avg_list = []
for year in years[6:]:
    df = pd.read_csv("Bat_"+year+".csv")
    top10_avg = df.nlargest(10,'R')
    avg_data = top10_avg['Avg'].mean() 
    avg_list.append(avg_data)

col1.markdown('#### Cumulative average of top 10 batsman')

fig, ax = plt.subplots()
ax.plot(years[6:], avg_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Average')

col1.pyplot(fig)

# Graph 6    

centuries_list = []
for year in years[6:]:
    df = pd.read_csv("Bat_"+year+".csv")
    num_100 = df['100'].sum() 
    centuries_list.append(num_100)

col2.markdown('#### Number of Centuries')

fig, ax = plt.subplots()
ax.plot(years[6:], centuries_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Centuries')

col2.pyplot(fig)

# Graph 7

avg_list = []
for year in years[6:]:
    df = pd.read_csv("Bat_"+year+".csv")
    top10_avg = df.nlargest(10,'R')
    avg_data = top10_avg['SR'].mean() 
    avg_list.append(avg_data)

col3.markdown('#### Strike Rate of top 10 batsman')

fig, ax = plt.subplots()
ax.plot(years[6:], avg_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Strike Rate')

col3.pyplot(fig)

# Grapg 5, 6 and 7 completed

col1, col2, col3 = st.columns(3,gap="medium")

# Graph 8
avg_list = []
for year in years[6:]:
    df = pd.read_csv("Bowl_"+year+".csv")
    top10_avg = df.nlargest(10,'W')
    avg_data = top10_avg['Avg'].mean() 
    avg_list.append(avg_data)

col1.markdown('#### Cumulative average of top 10 bowlers')

fig, ax = plt.subplots()
ax.plot(years[6:], avg_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Average')

col1.pyplot(fig)

# # Graph 9

avg_list = []
for year in years[6:]:
    df = pd.read_csv("Bowl_"+year+".csv")
    top10_avg = df.nlargest(10,'W')
    avg_data = top10_avg['Econ'].mean() 
    avg_list.append(avg_data)

col2.markdown('#### Cumulative Economy of top 10 bowlers')

fig, ax = plt.subplots()
ax.plot(years[6:], avg_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Economy')

col2.pyplot(fig)

# Graph 10

dot_list = []
for year in years[6:]:
    df = pd.read_csv("Bowl_"+year+".csv")
    dots = df['Dots'].sum() 
    dot_list.append(dots)

col3.markdown('#### Number of Dot Balls')

fig, ax = plt.subplots()
ax.plot(years[6:], dot_list, label='Line Graph')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Dots')

col3.pyplot(fig)

#graph for comaprision of the two player

col1,col2 = st.columns(2,gap="large")

batsmans=[]
bowlers =[]

for year in years[6:]:
    bat_file="Bat_"+str(year)+".csv"
    bowl_file="Bowl_"+str(year)+".csv"
    
    #batsmans data from the diffreant file
    with open(bat_file) as bat_obj:
        bat_reader=csv.reader(bat_obj)
        bat_reader.__next__()
        
        for name in bat_reader:
            if(name[0] not in batsmans):
                batsmans.append(name[0])

    #bowlers data from the file
    with open(bowl_file) as bowl_obj:
        bowl_reader=csv.reader(bowl_obj)
        bowl_reader.__next__()
        
        for name in bowl_reader:
            if(name[0] not in bowlers):
                bowlers.append(name[0])
    
batsmans.sort()
bowlers.sort()
user_batsman=col1.multiselect("Select Batsman you want to Compare : ",batsmans)

#Preaparing data from the graph to display Comparision

year=years[6:]

runs = [[] for _ in range(len(user_batsman))]
for y in year:
    bat_file="Bat_"+str(y)+".csv"
    
    with open(bat_file) as bat_obj:
        bat_reader=csv.reader(bat_obj)
        bat_reader.__next__()
        #to check pericular yer batman played or not?
        check_avail = [0 for _ in range(len(user_batsman))]
        for batsdata in bat_reader:
            if(batsdata[0] in user_batsman):
                index=user_batsman.index(batsdata[0])
                runs[index].append(int(batsdata[2]))
                check_avail[index]=1
                print(batsdata[0])
        
        #if not then based on that put 0 in that year
        while (0 in check_avail):
            index=check_avail.index(0)
            check_avail[index]=1
            runs[index].append(0)  


fig, ax = plt.subplots(figsize=(7,4))

for i in range(len(user_batsman)):
    ax.plot(years[6:], runs[i], label=user_batsman[i])

ax.legend(loc=0)                
col1.pyplot(fig)


#Bowler To Bowler Comaprision

user_bowler=col2.multiselect("Select Bowler you want to Compare : ",bowlers)
wickets = [[] for _ in range(len(user_batsman))]
for y in year:
    bat_file="Bowl_"+str(y)+".csv"
    
    with open(bat_file) as bowl_obj:
        bowl_reader=csv.reader(bowl_obj)
        bowl_reader.__next__()
        #to check pericular yer bowler played or not?
        check_avail = [0 for _ in range(len(user_bowler))]
        for bowlerdata in bowl_reader:
            if(bowlerdata[0] in user_bowler):
                index=user_bowler.index(bowlerdata[0])
                wickets[index].append(int(bowlerdata[4]))
                check_avail[index]=1
        
        #if not then based on that put 0 in that year
        while (0 in check_avail):
            index=check_avail.index(0)
            check_avail[index]=1
            wickets[index].append(0)  


fig, ax = plt.subplots(figsize=(7,4))

for i in range(len(user_bowler)):
    ax.plot(years[6:], wickets[i], label=user_bowler[i])

ax.legend(loc=0)                
col2.pyplot(fig)

