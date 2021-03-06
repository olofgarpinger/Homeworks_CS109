import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import zipfile

# Problem 1a
req = requests.get("http://seanlahman.com/baseball-archive/statistics")
page = req.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(page, 'html.parser')

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


# Problem 2a
req = requests.get("http://www.worldatlas.com/cntycont.htm")
page = req.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(page, 'html.parser')

link_data_list = [l for l in soup.findAll('a') if (l is not None)]
text_list = [l.contents[0] for l in link_data_list]
link_list = [str(l.get('href')) for l in link_data_list]

ID = [str(l).find("http://www.worldatlas.com/webimage/countrys/")>-1 for l in link_list]

countries_tmp = [text_list[j] for j in range(0,len(text_list)) if ID[j]]
countries_tmp = [x.encode('ascii').lower() for x in countries_tmp]

import re
links = [link_list[j] for j in range(0,len(text_list)) if ID[j]]
continents = [re.compile('countrys/(.*?)/').search(l).group(1) for l in links]

countries = pd.DataFrame({'country': countries_tmp, 'continent': continents})
d = {"continent": ["asia", "samerica", "namerica", "namerica", "namerica",
                   "asia", "asia", "namerica", "asia", "namerica"],
     "country": ["west bank and gaza", "aruba", "bermuda", "cayman islands",
                 "greenland", "hong kong, china", "macao, china",
                 "puerto rico", "taiwan", "turks and caicos islands"]}
df = pd.DataFrame(data=d)
countries = countries.append(df)
countries.country[countries.country=='burkina'] = 'burkina faso'
countries.country[countries.country=='congo, democratic republic of'] = 'congo, dem. rep.'
countries.country[countries.country=='congo'] = 'congo, rep.'
countries.country[countries.country=='saint kitts and nevis'] = 'st. kitts and nevis'
countries.country[countries.country=='saint lucia'] = 'st. lucia'
countries.country[countries.country=='saint vincent and the grenadines'] = 'st. vincent and the grenadines'
countries.country[countries.country=='slovakia'] = 'slovak republic'
countries.country[countries.country=="burma ("] = "myanmar"
countries.country[countries.country=='russian federation'] = 'russia'
countries.country[countries.country=='korea, south'] = 'south korea'
countries.country[countries.country=='korea, north'] = 'north korea'
countries.country[countries.country=='kyrgyzstan'] = 'kyrgyz republic'
countries.country[countries.country=='ivory coast'] = "cote d'ivoire"
countries.country[countries.country=="laos"] = "lao"
countries.country[countries.country=="macedonia"] = "macedonia, fyr"
countries.country[countries.country=="east timor"] = "timor-leste"
countries.country[countries.country=="micronesia"] = "micronesia, fed. sts."

gdp_per_capita_tmp = pd.read_csv("gdp_per_capita_ppp.csv").dropna()

gdp_per_capita = pd.melt(gdp_per_capita_tmp, id_vars=['GDP per capita'],var_name = "year", value_name="gdp_per_capita").rename(columns={'GDP per capita': 'country'})
gdp_per_capita.year=gdp_per_capita.year.apply(int)
gdp_per_capita['country'] = gdp_per_capita['country'].str.lower()


# unique_countries1 = countries.country.unique()
# unique_countries2 = gdp_per_capita.country.unique()

# unique_countries2[~np.isin(unique_countries2,unique_countries1)]
# unique_countries1[~np.isin(unique_countries1,unique_countries2)]

gdp_per_capita_merged = pd.merge(gdp_per_capita, countries, how = 'inner', on = ['country'])
gdp_per_capita_merged.head()

# Problem 2b
plt.hist(gdp_per_capita_merged[gdp_per_capita_merged.year==2000].gdp_per_capita, bins = 20)
plt.show()

# Problem 2c
def sliced_by_year(df, year):
    return gdp_per_capita_merged[gdp_per_capita_merged.year == year]

# Problem 2d
years = np.arange(1950,2011,10)
for ii in years:
    tmp = sliced_by_year(gdp_per_capita_merged, ii)
    tmp.boxplot(column="gdp_per_capita", by="continent")
    plt.yscale('log')

plt.show()

# Problem 3a
from scipy import stats

def ratioNormals(diff, a):
    X = stats.norm(loc=diff, scale=1)
    Y = stats.norm(loc=0, scale=1)
    PrX = X.sf(a)
    PrY = Y.sf(a)
    return PrX/PrY

x = np.linspace(0,5,51)
a2 = [ratioNormals(diff = i, a = 2) for i in x]
a3 = [ratioNormals(diff = i, a = 3) for i in x]
a4 = [ratioNormals(diff = i, a = 4) for i in x]
a5 = [ratioNormals(diff = i, a = 5) for i in x]

plt.yscale('log')
plt.plot(x, a2)
plt.plot(x, a3)
plt.plot(x, a4)
plt.plot(x, a5)

# Problem 3b
gdp_2012 = sliced_by_year(gdp_per_capita_merged, 2012)
gdp_2012_a_sa = gdp_2012[(gdp_2012.continent == "asia") | (gdp_2012.continent == "samerica")]
gdp_2012_a_sa.groupby("continent", as_index = False).mean()
gdp_2012_a_sa.boxplot('gdp_per_capita', by = "continent")

# Problem 3c
prop_greater_than_10000 = round(gdp_2012[gdp_2012.gdp_per_capita > 10000].shape[0]/float(gdp_2012.shape[0]),3)*100
prop_greater_than_10000

gdp_2012_ext = gdp_2012.assign(greater_than_10000 = gdp_2012.gdp_per_capita > 10000)
greater_than_10000_grouped = gdp_2012_ext.groupby(["continent","greater_than_10000"])["country"].count()
greater_than_10000_grouped.groupby(level=0).apply(lambda x: x/x.sum() * 100)















