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
