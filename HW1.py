import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import StringIO
import zipfile

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

Salaries.head()
Teams.head()