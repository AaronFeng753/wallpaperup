#coding=utf-8
import requests
import re
import os
import time
from bs4 import BeautifulSoup
import sys

page_num=1

while True:
	print('page_num = '+str(page_num))
	url = 'https://www.wallpaperup.com/resolution/8k/'+str(page_num)
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	r_url=requests.get(url,headers=headers)
	print('解析中.....')
	soup_a = BeautifulSoup(r_url.text,'lxml')
	wallpaper_pages=[]
	for links in soup_a.find_all(attrs={'title' : "View wallpaper"}):
		soup2 = BeautifulSoup(str(links),'lxml')
		wallpaper_pages.append('https://www.wallpaperup.com'+str(soup2.a.attrs['href']))
		
	wallpaper_imgaes_link = []
	for page in wallpaper_pages:
		r_page=requests.get(page,headers=headers)
		soup_page = BeautifulSoup(r_page.text,'lxml')
		div_img = str((soup_page.find_all(attrs={'class':'thumb-wrp'}))[0])
		soup_div_img = BeautifulSoup(div_img,'lxml')
		wallpaper_imgaes_link.append(str(soup_div_img.div.img.attrs['data-original']))
	
	
	current_dir = os.path.dirname(os.path.abspath(__file__))
	wallpapers_folder = current_dir + '\\8K_Wallpaper\\'
	if os.path.exists(wallpapers_folder) == False:
		os.mkdir(wallpapers_folder)
		
	p_split_name = re.compile(r'/')
	imageNumMax = len(wallpaper_imgaes_link)
	imageNumMin = 1
	print('解析完成.....')
	for image_link in wallpaper_imgaes_link:
		print('\n'+str(imageNumMin)+'/'+str(imageNumMax)+' '+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+image_link+'\n')
		r_image_link=requests.get(image_link,headers=headers)
		filename=p_split_name.split(image_link)[9]
		with open(wallpapers_folder+filename,'wb+') as f:
			f.write(r_image_link.content)
		imageNumMin=imageNumMin+1
	page_num=page_num+1
	
