import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import StringIO
import zipfile

# Problem 1a
req = requests.get("http://seanlahman.com/baseball-archive/statistics")
page = req.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(page, 'html.parser')

soup.find_all("a",href=True)
link_list = [l.get('href') for l in soup.findAll('a')]
my_list = []
for l in link_list:
    if l is not None and l[:4] == 'http':
        my_list.append(l)


matching = [s for s in my_list if "lahman-csv_2014-02-14" in s]
matching = [x.encode('ascii') for x in matching]

import urllib
filehandle, _ = urllib.urlretrieve('http://seanlahman.com/files/database/lahman-csv_2014-02-14.zip')
zip_file_object = zipfile.ZipFile(filehandle, 'r')
zip_list = zip_file_object.namelist()
file1_idx = zip_list.index("Salaries.csv")
file2_idx = zip_list.index("Teams.csv")

file1 = zip_file_object.open(zip_list[file1_idx])
file2 = zip_file_object.open(zip_list[file2_idx])

salaries = pd.read_csv(file1)
teams = pd.read_csv(file2)

salaries.head()
teams.head()

# Problem 1b
list(salaries)
sum_salaries = salaries.groupby(['yearID', 'teamID'], as_index=False).sum()
sum_salaries.head()

# Problem 1c
list(teams)
teams_subset = teams.loc[:,['yearID', 'teamID', 'W']]
merged_df = pd.merge(sum_salaries, teams_subset, how = 'inner', on = ['yearID', 'teamID'])
merged_df.head()

# Problem 1d
unique_years = merged_df['yearID'].unique()
f, axarr = plt.subplots(3, 10)
j = 1
for k in unique_years:
    yearly_df = merged_df[merged_df.yearID == k]
    yearly_oak_df = merged_df[(merged_df['teamID'] == "OAK") & (merged_df['yearID'] == k)]
    axarr[j/10, j%10].scatter(yearly_df['salary'], yearly_df['W'])
    axarr[j/10, j%10].set_title(k)
    axarr[j / 10, j % 10].scatter(yearly_oak_df['salary'], yearly_oak_df['W'])
    j += 1

plt.show()




