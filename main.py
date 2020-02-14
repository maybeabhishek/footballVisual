import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt


from subprocess import check_output
print(check_output(["ls", "./input"]).decode("utf8"))
con = sqlite3.connect('./input/database.sqlite')
cursor = con.cursor()
table_names = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

player_table = pd.read_sql_query("SELECT * FROM Player", con)
player_att_table = pd.read_sql_query("SELECT * FROM Player_Attributes", con)
team_table = pd.read_sql_query("SELECT * FROM Team", con)
team_att_table = pd.read_sql_query("SELECT * FROM Team_Attributes", con)


fig1, ax1 = plt.subplots(nrows = 1, ncols = 2)
fig1.set_size_inches(14,4)
sns.boxplot(data = player_table.loc[:,["height",'weight']], ax = ax1[0])
ax1[0].set_xlabel('Player Table Features')
ax1[0].set_ylabel('')
sns.distplot(a = player_table.loc[:,["height"]], bins= 10, kde = True, ax = ax1[1], \
            label = 'Height')
sns.distplot(a = player_table.loc[:,["weight"]], bins= 10, kde = True, ax = ax1[1], \
            label = 'Weight')
ax1[1].legend()
sns.jointplot(x='height',y = 'weight',data = player_table,kind = 'scatter')
fig1.tight_layout()

plt.show(fig1)

np.unique(player_att_table.dtypes.values)
player_att_table.select_dtypes(include =['float64','int64']).head().loc[:,player_att_table.select_dtypes(include =['float64','int64']).columns[3:]].head()
corr2 = player_att_table.select_dtypes(include =['float64','int64']).loc[:,player_att_table.select_dtypes(include =['float64','int64']).columns[3:]].corr()

fig2,ax2 = plt.subplots(nrows = 1,ncols = 1)
fig2.set_size_inches(w=24,h=24)
sns.heatmap(corr2,annot = True,linewidths=0.5,ax = ax2)

plt.show(fig2)

fig3, ax3 = plt.subplots(nrows = 1, ncols = 3)
fig3.set_size_inches(12,4)
sns.countplot(x = player_att_table['preferred_foot'],ax = ax3[0])
sns.countplot(x = player_att_table['attacking_work_rate'],ax = ax3[1])
sns.countplot(x = player_att_table['defensive_work_rate'],ax = ax3[2])
fig3.tight_layout()
plt.show(fig3)

player_att_table_updated1 = player_att_table.iloc[(player_att_table['attacking_work_rate'].\
                                                  isin(['medium','high','low'])\
                       & player_att_table['defensive_work_rate'].isin(['medium','high','low'])),:]


fig4, ax4 = plt.subplots(nrows = 1, ncols = 3)
fig4.set_size_inches(12,3)
sns.barplot(x ='preferred_foot', y = 'preferred_foot', data = player_att_table_updated1,\
            estimator = lambda x: len(x)/len(player_att_table_updated1) * 100, ax = ax4[0],\
           orient = 'v')
ax4[0].set(ylabel = 'Percentage',title = 'Preferred Foot')
sns.barplot(x ='attacking_work_rate', y = 'attacking_work_rate', data = player_att_table_updated1,\
            estimator = lambda x: len(x)/len(player_att_table_updated1) * 100, ax = ax4[1],\
           orient = 'v')
ax4[1].set(ylabel = 'Percentage',title = 'Attacking Work Rate')
sns.barplot(x ='defensive_work_rate', y = 'defensive_work_rate', data = player_att_table_updated1,\
            estimator = lambda x: len(x)/len(player_att_table_updated1) * 100, ax = ax4[2],\
           orient = 'v')
ax4[2].set(ylabel = 'Percentage',title = 'Defensive Work Rate')
fig4.tight_layout()
plt.show(fig4)

pat = player_att_table_updated1.loc[:,player_att_table_updated1.columns.tolist()[3:]]

fig5, ax5 = plt.subplots(nrows=5,ncols=7)
fig5.set_size_inches(16,12)
for i,j in enumerate(player_att_table_updated1.select_dtypes(include = ['float64','int64']).columns[3:].tolist()):
    sns.distplot(pat.loc[:,j],kde = False,hist = True, ax = ax5[int(i/7)][i%7])
fig5.tight_layout()
plt.show(fig5)


fig6, ax6 = plt.subplots(nrows=5,ncols=7)
fig6.set_size_inches(16,12)
for i,j in enumerate(player_att_table_updated1.select_dtypes(include = ['float64','int64']).columns[3:].tolist()):
    sns.boxplot(x = "preferred_foot", y = j, data= pat, ax = ax6[int(i/7)][i%7])
fig6.tight_layout()

plt.show(fig6)


# team_table_updated = team_table[~team_table.loc[:,'team_fifa_api_id'].isnull()]
# team_att_table_updated1 = team_att_table.drop(['buildUpPlayDribbling'],axis = 1)

# my_team = dict()
# for i,j in list(team_table_updated.iloc[:,3:].groupby('team_short_name')):
#     my_team[i] = j.iloc[:,0].values.tolist()
# print({k:v for k,v in my_team.items() if len(v) > 1})

# tat = team_att_table_updated1.loc[:,team_att_table_updated1.columns.tolist()[3:]]
# sns.pairplot(tat)

# fig9, ax9 = plt.subplots(nrows=2,ncols=4)
# fig9.set_size_inches(12,6)
# for i,j in enumerate(team_att_table_updated1.select_dtypes(include = ['int64']).columns[3:].tolist()):
#     sns.distplot(tat.loc[:,j],kde =True,hist = True, ax = ax9[int(i/4)][i%4])
# fig9.tight_layout()
# plt.show(fig9)