from bs4 import BeautifulSoup
import unittest
import requests
import csv

######### PART 0 #########
try:
	gallery_data = open("gallery_data.html","r").text
except:
	gallery_data = requests.get("http://newmantaylor.com/gallery.html").text
	f = open("gallery_data.html","w")
	f.write(gallery_data)
	f.close()

soup = BeautifulSoup(gallery_data, 'html.parser')

img_list = soup.find_all("img")

for images in img_list:
	try:
		print(images['alt'])
	except:
		print("No alternative text provided!")

######### PART 1 #########

try:
  gov_data = open("gov_data.html",'r').read()
except:
  gov_data = requests.get("https://www.nps.gov/index.htm").text
  f = open("gov_data.html",'w')
  f.write(gov_data)
  f.close()

gov = BeautifulSoup(gov_data, 'html.parser')

links_ = gov.find_all('a')

state_part = gov.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"})

all_= state_part.find_all('a')

states = ['Michigan', 'Arkansas', 'California']
for item in all_:
  state_name = item.text
  if state_name in states:
    state_link = "https://www.nps.gov" + item.get('href')
    file_n = state_name.lower() + "_data.html"
    try:
      state_name_ = open(file_n, 'r').read()
    except:
      state_name_ = requests.get(state_link).text
      f = open(file_n,'w')
      f.write(state_name_)
      f.close()

michigan_data = open("michigan_data.html", "r").read()
michigan_soup = BeautifulSoup(michigan_data, 'html.parser')

arkansas_data = open("arkansas_data.html", "r").read()
arkansas_soup = BeautifulSoup(arkansas_data, 'html.parser')

california_data = open("california_data.html", "r").read()
california_soup = BeautifulSoup(california_data, 'html.parser')
