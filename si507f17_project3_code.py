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

######### PART 2 #########

def get_park(s_soup):
  s_list = s_soup.find("ul", {"id":"list_parks"}).find_all("li", {"class":"clearfix"})
  return s_list

class NationalSite(object):
  def __init__(self, p_soup):
      self.location = p_soup.find("h4").get_text()
      self.name = p_soup.find("h3").get_text()
      links = p_soup.find_all('a')[2]
      self.url = links['href']
      self.type = p_soup.find("h2").get_text() or "None"
      self.description = p_soup.find("p").get_text().strip() or ""

  def __str__(self):
    return "{} | {}".format(self.name, self.location)

  def __contains__(self, astring):
    return astring in self.name

  def get_mailing_address(self):
    try:
      park_html = requests.get(self.url)
      info_soup = BeautifulSoup(park_html.content, 'html.parser')
      full_address_block = info_soup.find('div', {"itemprop": "address"})
      street = full_address_block.find('span', {"itemprop": "streetAddress"}).text.strip()
      city = full_address_block.find('span', {"itemprop": "addressLocality"}).text.strip()
      state = full_address_block.find('span', {"itemprop": "addressRegion"}).text.strip()
      zip_ = full_address_block.find('span', {"itemprop": "postalCode"}).text.strip()
      mailing_address = street + " / " + city + " / " + state + " / " + zip_
      return mailing_address
    except:
      return ""

sample_alcatraz = get_park(california_soup)[0]
sample_class = NationalSite(sample_alcatraz)

print(sample_class)
print(sample_class.url)
print(sample_class.get_mailing_address())

######### PART 3 #########

ak_list = get_park(arkansas_soup)
ca_list = get_park(california_soup)
mi_list = get_park(michigan_soup)

arkansas_natl_sites = []
for item in ak_list:
  x = NationalSite(item)
  arkansas_natl_sites.append(x)

california_natl_sites = []
for item in ca_list:
  x = NationalSite(item)
  california_natl_sites.append(x)

michigan_natl_sites = []
for item in mi_list:
  x = NationalSite(item)
  michigan_natl_sites.append(x)

  ######### PART 4 #########

  def write_csv(filename, site_list):
      with open(filename, 'w') as outfile:
          writer = csv.writer(outfile, delimiter=',')
          header = ["Name", "Location", "Type", "Address", "Description"]
          writer.writerow(header)

          for site in site_list:
              if site.type is None:
                  x = "None"
              else:
                  x = site.type
              row = [site.name, site.location, x, site.get_mailing_address(), site.description]
              writer.writerow(row)


  write_csv("arkansas.csv", arkansas_natl_sites)
  write_csv("california.csv", california_natl_sites)
  write_csv("michigan.csv", michigan_natl_sites)
