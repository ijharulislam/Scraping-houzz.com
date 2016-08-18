#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import urllib2
from bs4 import BeautifulSoup
import csv 

data =[]

for k in range(0,46,15):

	r = urllib2.urlopen("http://www.houzz.com/professionals/general-contractor/c/Eagle--CO/d/25/p/%s"%k)
	print k

	bs = BeautifulSoup(r, "lxml")
	url = bs.find_all("a", class_="pro-title")
	for u in url:
		output = {}
		link = u["href"]
		if link != "javascript:;":
			s = urllib2.urlopen(link)
			su = BeautifulSoup(s, "lxml")
			name = su.find("a", class_="profile-full-name")
			if name is not None:
				n = name.text.encode("utf-8")
				output["Name"] = n
			ph = su.find("span", class_="pro-contact-text")
			if ph is not None:
				phone = ph.text
				output["Phone"] = phone 
			web = su.find("a", class_="proWebsiteLink")
			if web is not None:
				website = web["href"]
				output["Website"] = website

			st_ad = su.find("span", attrs={"itemprop":"streetAddress"})
			if st_ad is not None:
				st_ad = st_ad.text
			else:
				st_ad = ""

			st_local = su.find("span", attrs={"itemprop":"addressLocality"})
			if st_local is not None:
				st_local = st_local.text
			else:
				st_local = ""
			st_reg = su.find("span", attrs={"itemprop":"addressRegion"})
			if st_reg is not None:
				st_reg = st_reg.text
			st_postal = su.find("span", attrs={"itemprop":"postalCode"})
			if st_postal is not None:
				st_postal = st_postal.text
			st_count = su.find("span", attrs={"itemprop":"addressCountry"})
			if st_count is not None:
				st_count = st_count.text

			location = "%s %s, %s %s %s " %(st_ad,st_local,st_reg,st_postal,st_count)
			output["Address"] = location

			over = su.find("div", class_="profile-about").find_all("div")
			over_view = []
			for o in over:
				ov = "%s" %o.text + "\n"
				ov = ov.encode("utf-8")
				over_view.append(ov)

			output["Overview"] = " ".join(over_view)
			print over_view
			followers = su.find("a", class_="followers")
			if followers is not None:
				f_l = followers.find("span").text
				output["Followers"] = f_l

			following = su.find("a", class_="following")
			if following is not None:
				f_ing = following.find("span").text
				output["Following"] = f_ing
			com = su.find_all("span", class_="discussion-body")
			if com is not None:
				comments = []
				for c in com:
					comments.append(c.text.encode("utf-8"))
					output["Comments"] = comments
			data.append(output)
			print output






def WriteDictToCSV(csv_columns,dict_data):
	with open("houzz.csv", 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for row in dict_data:
			print row
			writer.writerow(row)


csv_columns =[ 'Name','Address','Phone', 'Website','Followers', 'Following', 'Overview', 'Comments']

WriteDictToCSV(csv_columns,data)

### INserting Images ### 

# url = 'http://python.org/logo.png'
# image_data = io.BytesIO(urllib2.urlopen(url).read())

# worksheet.insert_image('B5', url, {'image_data': image_data})


